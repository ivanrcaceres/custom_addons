from odoo import api, fields, models, _


# class SaleOrder(models.Model):
#     _inherit = "sale.order"
#
#     @api.model
#     def _default_warehouse_id(self):
#         user_id = self.env.user.id
#         warehouse_ids = self.env['stock.warehouse'].search(
#             [('user_ids', 'child_of', user_id)], limit=1)
#         return warehouse_ids
#
#     warehouse_id = fields.Many2one(
#         'stock.warehouse', string='Warehouse',
#         required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
#         default=_default_warehouse_id)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    x_image_product = fields.Binary('Image Producto', compute='_get_image')

    @api.one
    @api.depends('product_id')
    def _get_image(self):
        self.x_image_product = self.product_id.image_small
