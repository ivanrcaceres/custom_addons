# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api
from datetime import datetime, timedelta
from lxml import etree
from odoo.exceptions import ValidationError

class resCurrency(models.Model):
    _inherit= 'res.currency'

    name = fields.Char(string='Currency', size=15, required=True, help="Currency Code (ISO 4217)")
    ambito = fields.Selection([('venta','Venta'),('compra','Compra')],string="Ámbito", default=False, required=True)
    rate = fields.Float(compute='_compute_current_rate', string='Current Rate', digits=(12, 12),
                        help='The rate of the currency to the currency of rate 1.')
    moneda_compania = fields.Boolean(compute='_get_currency_company')

    @api.multi
    def _get_currency_company(self):
        for moneda in self:
            if moneda.id == self.env.user.company_id.currency_id.id:
                moneda.moneda_compania = True




class cotizaciones(models.Model):
    _inherit = "res.currency.rate"

    cotizacion  = fields.Float(String='Cotizacion comercial')
#     set_compra = fields.Float(String='Cotizacion SET Compra')
    rate = fields.Float(digits=(12, 12), default=1.0, help='The rate of the currency to the currency of rate 1')
    set_venta = fields.Float(String='Cotizacion')
    name = fields.Date(string='Date', required=True, index=True,
                           default=lambda self: fields.Date.today())
    @api.onchange('set_venta')
    def _cambiar_rate(self):
        if self.set_venta:
            self.rate= 1 / self.set_venta