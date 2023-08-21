# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api
from datetime import datetime, timedelta
from lxml import etree
from odoo.exceptions import ValidationError


class Company(models.Model):
    _inherit = 'res.company'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    timbrado_id = fields.Many2one('timbrado.timbrado')

    timbrado = fields.Char(size=20, string="Timbrado")
    fecha_inicio = fields.Date()
    fecha_fin = fields.Date()
    numero_sucursal = fields.Integer()
    numero_caja = fields.Integer()
    numero_inicio = fields.Integer()
    numero_fin = fields.Integer()
    ultimo_numero_impreso = fields.Integer()
    fecha_ultimo_numero_impreso = fields.Integer()
    ultimo_numero_completo = fields.Char()
