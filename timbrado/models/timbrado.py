# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api
from datetime import datetime, timedelta
from lxml import etree
from odoo.exceptions import ValidationError


class Timbrado(models.Model):
    _name = 'timbrado.timbrado'
    _description = 'timbrado'

    name = fields.Char(size=20, string="Timbrado")
    fecha_inicio = fields.Date()
    fecha_fin = fields.Date()
    numero_sucursal = fields.Integer()
    numero_caja = fields.Integer()
    numero_inicio = fields.Integer()
    numero_fin = fields.Integer()
    ultimo_numero_impreso = fields.Integer()
    fecha_ultimo_numero_impreso = fields.Integer()
    ultimo_numero_completo = fields.Char()

    # def name_get(self):
    #     result = []
    #     for c in self:
    #         name = '%s' % (c.name)
    #         result.append(name)
    #     return result

