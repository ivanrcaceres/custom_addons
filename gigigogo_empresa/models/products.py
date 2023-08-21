# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision as dp


class products_custom(models.Model):
    _inherit = 'product.template'
    x_original_code = fields.Char(string='Original Code', help='Codigo de fabrica del producto')

    # _sql_constraints = [
    #     ('x_original_code_uniq', 'unique(x_original_code)', "El codigo del producto no puede repetirse !"),
    # ]

    lista_de_precios = fields.One2many('product.pricelist.item', 'product_tmpl_id', string='Precios')


class product_categry_custom(models.Model):
    _inherit = 'product.category'
    x_category_code = fields.Integer(string="Code", required="True", default="0")


class Products(models.Model):
    _inherit = 'product.product'

    x_unit_price = fields.Float('Unitario', compute='_compute_unit_cost_value')

    @api.multi
    @api.depends('standard_price')
    def _compute_unit_cost_value(self):
        to_date = self.env.context.get('to_date')
        for product in self:
            price_used = product.standard_price
            if to_date:
                price_used = product.get_history_price(
                    self.env.user.company_id.id,
                    date=to_date,
                )
            product.x_unit_price = price_used
#
#     qty_available = fields.Float(
#         'Quantity On Hand', compute='_compute_quantities', search='_search_qty_available',
#         digits=dp.get_precision('Product Unit of Measure'),
#         help="Current quantity of products.\n"
#              "In a context with a single Stock Location, this includes "
#              "goods stored at this Location, or any of its children.\n"
#              "In a context with a single Warehouse, this includes "
#              "goods stored in the Stock Location of this Warehouse, or any "
#              "of its children.\n"
#              "stored in the Stock Location of the Warehouse of this Shop, "
#              "or any of its children.\n"
#              "Otherwise, this includes goods stored in any Stock Location "
#              "with 'internal' type.", store=True)
