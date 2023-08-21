# -*- coding: utf-8 -*-

from psycopg2 import OperationalError, Error
from odoo import fields, models, exceptions, api, _

from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools.float_utils import float_compare, float_is_zero

import logging

_logger = logging.getLogger(__name__)



class Picking(models.Model):
    _inherit = "stock.picking"


    # validando que en un picking no halla mas de un numero x de productos
    @api.multi
    def limpiar_reserva_cero(self):
        moves = self.move_lines.filtered(lambda x : x.reserved_availability <= 0)
        # moves_cero = self.move_lines.filtered(lambda x : x.quantity_done <= 0)
        for m in moves:
            m.state = 'draft'
        moves.unlink()

        # for m in moves_cero:
        #     m.state = 'draft'
        #     m.unlink()
          


class quants(models.Model):
    _inherit = 'stock.quant'

    @api.multi
    def desreservar_todo(self):
        quants = self.env['stock.quant'].search([('reserved_quantity','!=',0)])
        for q in quants:
            q.reserved_quantity=0
        moves = self.env['stock.move'].search([('reserved_availability','!=',0),('state','not in',['done','cancel'])])
        for m in moves:
            m._do_unreserve()
            m._action_assign()

    @api.model
    def _update_reserved_quantity(self, product_id, location_id, quantity, lot_id=None, package_id=None, owner_id=None,
                                  strict=False):
        """ Increase the reserved quantity, i.e. increase `reserved_quantity` for the set of quants
        sharing the combination of `product_id, location_id` if `strict` is set to False or sharing
        the *exact same characteristics* otherwise. Typically, this method is called when reserving
        a move or updating a reserved move line. When reserving a chained move, the strict flag
        should be enabled (to reserve exactly what was brought). When the move is MTS,it could take
        anything from the stock, so we disable the flag. When editing a move line, we naturally
        enable the flag, to reflect the reservation according to the edition.

        :return: a list of tuples (quant, quantity_reserved) showing on which quant the reservation
            was done and how much the system was able to reserve on it
        """
        self = self.sudo()
        rounding = product_id.uom_id.rounding
        quants = self._gather(product_id, location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id,
                              strict=strict)
        reserved_quants = []

        if float_compare(quantity, 0, precision_rounding=rounding) > 0:
            # if we want to reserve
            available_quantity = self._get_available_quantity(product_id, location_id, lot_id=lot_id,
                                                              package_id=package_id, owner_id=owner_id, strict=strict)
            if float_compare(quantity, available_quantity, precision_rounding=rounding) > 0:
                raise UserError(_(
                    'It is not possible to reserve more products of %s than you have in stock.') % product_id.display_name)
        elif float_compare(quantity, 0, precision_rounding=rounding) < 0:
            # if we want to unreserve
            available_quantity = sum(quants.mapped('reserved_quantity'))
            # if float_compare(abs(quantity), available_quantity, precision_rounding=rounding) > 0:
            #     raise UserError(_('It is not possible to unreserve more products of %s than you have in stock.') % product_id.display_name)
        else:
            return reserved_quants

        for quant in quants:
            if float_compare(quantity, 0, precision_rounding=rounding) > 0:
                max_quantity_on_quant = quant.quantity - quant.reserved_quantity
                if float_compare(max_quantity_on_quant, 0, precision_rounding=rounding) <= 0:
                    continue
                max_quantity_on_quant = min(max_quantity_on_quant, quantity)
                quant.reserved_quantity += max_quantity_on_quant
                reserved_quants.append((quant, max_quantity_on_quant))
                quantity -= max_quantity_on_quant
                available_quantity -= max_quantity_on_quant
            else:
                max_quantity_on_quant = min(quant.reserved_quantity, abs(quantity))
                quant.reserved_quantity -= max_quantity_on_quant
                reserved_quants.append((quant, -max_quantity_on_quant))
                quantity += max_quantity_on_quant
                available_quantity += max_quantity_on_quant

            if float_is_zero(quantity, precision_rounding=rounding) or float_is_zero(available_quantity,
                                                                                     precision_rounding=rounding):
                break
        return reserved_quants
    # @api.multi
    # def button_validate(self):
    #     lines_to_check = self.move_line_ids
    #     number_of_register = 15
    #     groups = self.env.user.has_group('stock.group_stock_manager')
    #     if len(lines_to_check) > number_of_register and not groups:
    #         raise UserError(_('No puede Tener mas de %d productos en un mismo traslado' % number_of_register))
    #     return super(Picking, self).button_validate()
