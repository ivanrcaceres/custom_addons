# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class CustomResPartner(models.Model):
    _inherit = 'res.partner'
    ruc = fields.Char(string='Numero de documento')
    # vat = fields.Char(string='Ruc o Num. de Doc.', index=True, required=True)
    vat = fields.Char(string='2Tax ID', index=True,
                      help="2The Tax Identification Number. Complete it if the contact is subjected to government taxes. Used in some legal statements.")

    @api.model
    def create(self, vals):
        if 'vat' in vals:
            print("vals['vat']")
            print(vals['vat'])
            vals['ruc'] = vals['vat']
        else:
            vals['var'] = 0
            vals['ruc'] = 0
        rec = super(CustomResPartner, self).create(vals)

        return rec