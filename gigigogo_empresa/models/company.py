# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api

class ResCompany(models.Model):
    _inherit = "res.company"

    ruc = fields.Char(required=True, string="RUC")
    dv =  fields.Char(size=1,required=True, string="DV")
    nombrefantasia = fields.Char(string="Nombre de fantasia")
    razon_social = fields.Char(string="Razon Social")
    representante_legal = fields.Char(string="Representante Legal")
    ruc_representante = fields.Char(string="RUC del Rep. Legal")
    dv_representante = fields.Char(required=True, string="DV del Representante Legal")
    jornal = fields.Monetary(string="Jornal diario vigente")
    exportador = fields.Boolean(string="Es exportador?")

    diario_caja_chica = fields.Many2one('account.journal',string="Diario de Caja Chica")

