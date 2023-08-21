from odoo import api, fields, models, _


class PosOrder(models.Model):
    _inherit = 'pos.order'

    product_id = fields.Many2one('product.product', 'Product', related='lines.product_id')

    @api.one
    def generate_picking(self):
        self.create_picking()
