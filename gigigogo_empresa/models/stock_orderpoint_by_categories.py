from collections import defaultdict

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta


class StockOrderpointByCategories(models.Model):
    _name = 'stock.warehouse.orderpoint.categories'
    _description = "Minimum Inventory Rule By Categories"

    @api.model
    def default_get(self, fields):
        res = super(Orderpoint, self).default_get(fields)
        warehouse = None
        if 'warehouse_id' not in res and res.get('company_id'):
            warehouse = self.env['stock.warehouse'].search([('company_id', '=', res['company_id'])], limit=1)
        if warehouse:
            res['warehouse_id'] = warehouse.id
            res['location_id'] = warehouse.lot_stock_id.id
        return res

    name = fields.Char(
        'Name', copy=False, required=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('stock.orderpoint'))
    active = fields.Boolean(
        'Active', default=True,
        help="If the active field is set to False, it will allow you to hide the orderpoint without removing it.")
    warehouse_id = fields.Many2one(
        'stock.warehouse', 'Warehouse',
        ondelete="cascade", required=True)
    location_id = fields.Many2one(
        'stock.location', 'Location',
        ondelete="cascade", required=True)
    category_id = fields.Many2one(
        'product.category', 'Product Category', ondelete='cascade', required=True)

    category_min_qty = fields.Float(
        'Minimum Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True,
        help="When the virtual stock goes below the Min Quantity specified for this field, Odoo generates "
             "a procurement to bring the forecasted quantity to the Max Quantity.")
    category_max_qty = fields.Float(
        'Maximum Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True,
        help="When the virtual stock goes below the Min Quantity, Odoo generates "
             "a procurement to bring the forecasted quantity to the Quantity specified as Max Quantity.")
    qty_multiple = fields.Float(
        'Qty Multiple', digits=dp.get_precision('Product Unit of Measure'),
        default=1, required=True,
        help="The procurement quantity will be rounded up to this multiple.  If it is 0, the exact quantity will be used.")
    group_id = fields.Many2one(
        'procurement.group', 'Procurement Group', copy=False,
        help="Moves created through this orderpoint will be put in this procurement group. If none is given, the moves generated by procurement rules will be grouped into one big picking.")
    company_id = fields.Many2one(
        'res.company', 'Company', required=True,
        default=lambda self: self.env['res.company']._company_default_get('stock.warehouse.orderpoint'))
    lead_days = fields.Integer(
        'Lead Time', default=1,
        help="Number of days after the orderpoint is triggered to receive the products or to order to the vendor")
    lead_type = fields.Selection(
        [('net', 'Day(s) to get the products'), ('supplier', 'Day(s) to purchase')], 'Lead Type',
        required=True, default='supplier')

    _sql_constraints = [
        ('qty_multiple_check', 'CHECK( qty_multiple >= 0 )', 'Qty Multiple must be greater than or equal to zero.'),
    ]


    @api.onchange('warehouse_id')
    def onchange_warehouse_id(self):
        """ Finds location id for changed warehouse. """
        if self.warehouse_id:
            self.location_id = self.warehouse_id.lot_stock_id.id
