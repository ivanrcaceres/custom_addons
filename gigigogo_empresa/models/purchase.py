# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api
from datetime import datetime, timedelta
from lxml import etree
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"


    @api.multi
    def button_confirm(self):

        purchase = super(PurchaseOrder, self).button_confirm()
        lot = self.env['ir.sequence'].next_by_code('stock.lot.serial')

        for line in self.order_line:
            for m in line.move_ids:
                for move_line in m.move_line_ids:
                    move_line.lot_name = lot
                    move_line.qty_done = m.product_uom_qty
        return purchase

    # @api.multi
    # def button_approve(self, force=False):
    #     self.write({'state': 'purchase', 'date_approve': self.date_approve})
    #     self._create_picking()
    #     self.filtered(
    #         lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
    #     return {}


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    x_image_product = fields.Binary('Image Producto',compute = '_get_image')

    @api.one
    @api.depends('product_id')
    def _get_image(self):
        self.x_image_product = self.product_id.image_small



