# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class caja_timbrado(models.Model):
#     _name = 'caja_timbrado.caja_timbrado'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100