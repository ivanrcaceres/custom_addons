# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api
from datetime import datetime, timedelta
from dateutil import relativedelta

from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class stockMove(models.Model):
    _inherit = 'stock.move'

    x_image_product = fields.Binary('Image Producto', compute='_get_image')

    x_quantity_of_not_proccess = fields.Integer('Cantidad no Procesado', compute="_compute_not_proccess")

    @api.multi
    def _compute_not_proccess(self):
        for record in self:
            record.x_quantity_of_not_proccess = self.quantity_last_tree_day(record)

    def quantity_last_tree_day(self, record):

        current_date = datetime.today()
        old_date = current_date - timedelta(days=10)

        cancel = self.search_count([('product_id', '=', record.product_id.id),
                                  ('state', '=', 'cancel'),
                                  ('location_id', '=', record.location_id.id),
                                  ('location_dest_id', '=', record.location_dest_id.id),
                                  ('create_date', '>=', old_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)),
                                  ('create_date', '<=', current_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT))
                                  ])

        confirmed = self.search_count([('product_id', '=', record.product_id.id),
                                  ('state', '=', 'done'),
                                  ('location_id', '=', record.location_id.id),
                                  ('create_date', '>=', old_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)),
                                  ('create_date', '<=', current_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT))
                                  ])

        result = cancel - confirmed

        if result > 0:
            return result
        return 0

    @api.one
    @api.depends('product_id')
    def _get_image(self):
        self.x_image_product = self.product_id.image_small

    # @api.multi
    # def _do_unreserve(self):
    #     for move in self:
    #         m = super(stockMove, move)._do_unreserve()
    #         if move.reserved_availability <= 0:
    #             move.unlink()

    def _action_confirm(self, merge=True, merge_into=False):
        """ Confirms stock move or put it in waiting if it's linked to another move.
        :param: merge: According to this boolean, a newly confirmed move will be merged
        in another move of the same picking sharing its characteristics.
        """
        move_create_proc = self.env['stock.move']
        move_to_confirm = self.env['stock.move']
        move_waiting = self.env['stock.move']

        to_assign = {}
        for move in self:
            # if the move is preceeded, then it's waiting (if preceeding move is done, then action_assign has been called already and its state is already available)
            if move.move_orig_ids:
                move_waiting |= move
            else:
                if move.procure_method == 'make_to_order':
                    move_create_proc |= move
                else:
                    move_to_confirm |= move
            if not move.picking_id and move.picking_type_id:
                key = (move.group_id.id, move.location_id.id, move.location_dest_id.id)
                if key not in to_assign:
                    to_assign[key] = self.env['stock.move']
                to_assign[key] |= move

        # create procurements for make to order moves
        for move in move_create_proc:
            values = move._prepare_procurement_values()
            origin = (move.group_id and move.group_id.name or (
                    move.rule_id and move.rule_id.name or move.origin or move.picking_id.name or "/"))
            self.env['procurement.group'].run(move.product_id, move.product_uom_qty, move.product_uom, move.location_id,
                                              move.rule_id and move.rule_id.name or "/", origin,
                                              values)

        move_to_confirm.sudo().write({'state': 'confirmed'})
        (move_waiting | move_create_proc).write({'state': 'waiting'})

        # assign picking in batch for all confirmed move that share the same details
        for moves in to_assign.values():
            moves._assign_picking()
        self._push_apply()
        if merge:
            return self._merge_moves(merge_into=merge_into)
        return self

    # def _push_apply(self):
    #     # TDE CLEANME: I am quite sure I already saw this code somewhere ... in routing ??
    #     Push = self.env['stock.location.path']
    #     for move in self:
    #         # if the move is already chained, there is no need to check push rules
    #         if move.move_dest_ids:
    #             continue
    #         # if the move is a returned move, we don't want to check push rules, as returning a returned move is the only decent way
    #         # to receive goods without triggering the push rules again (which would duplicate chained operations)
    #         domain = [('location_from_id', '=', move.location_dest_id.id)]
    #         # priority goes to the route defined on the product and product category
    #         routes = move.product_id.route_ids | move.product_id.categ_id.total_route_ids
    #         rules = Push.search(domain + [('route_id', 'in', routes.ids)], order='route_sequence, sequence', limit=1)
    #         if not rules:
    #             # TDE FIXME/ should those really be in a if / elif ??
    #             # then we search on the warehouse if a rule can apply
    #             if move.warehouse_id:
    #                 rules = Push.search(domain + [('route_id', 'in', move.warehouse_id.route_ids.ids)],
    #                                     order='route_sequence, sequence', limit=1)
    #             elif move.picking_id.picking_type_id.warehouse_id:
    #                 rules = Push.search(
    #                     domain + [('route_id', 'in', move.picking_id.picking_type_id.warehouse_id.route_ids.ids)],
    #                     order='route_sequence, sequence', limit=1)
    #         # Make sure it is not returning the return
    #         if rules and (
    #                 not move.origin_returned_move_id or move.origin_returned_move_id.location_dest_id.id != rules.location_dest_id.id):
    #             rules._apply(move)


class stockLocationPath(models.Model):
    _inherit = 'stock.location.path'

    def _apply(self, move):
        new_date = (datetime.strptime(move.date_expected, DEFAULT_SERVER_DATETIME_FORMAT) + relativedelta.relativedelta(
            days=self.delay)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        if self.auto == 'transparent':
            move.sudo().write({
                'date': new_date,
                'date_expected': new_date,
                'location_dest_id': self.location_dest_id.id})
            # avoid looping if a push rule is not well configured; otherwise call again push_apply to see if a next step is defined
            if self.location_dest_id != move.location_dest_id:
                # TDE FIXME: should probably be done in the move model IMO
                move._push_apply()
        else:
            new_move_vals = self._prepare_move_copy_values(move, new_date)
            new_move = move.sudo().copy(new_move_vals)
            move.sudo().write({'move_dest_ids': [(4, new_move.id)]})
            new_move._action_confirm()
