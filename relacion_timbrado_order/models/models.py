# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class RelacionTimbradoFact(models.Model):
    _name = 'relacion_timbrado_order.relaciontimbfact'
    _description = 'relaciontimbfact'

    # name = fields.Char(string='Venta POS')
    venta = fields.Char(string='Venta POS')
    factura = fields.Char(string='Nro de Fact.')

