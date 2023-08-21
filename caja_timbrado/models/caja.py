# -*- coding: utf-8 -*-

from odoo import models, fields, api

class caja_timbrado(models.Model):
    _inherit = 'pos.config'

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
    factura_para_imprimir = fields.Integer()

    _sql_constraints = [
        ('name_unique','UNIQUE(name)', 'El nombre de la caja debe ser unico'),
    ]

    # @api.depends('value')
    # def _value_pc(self):
    #     self.value2 = float(self.value) / 100