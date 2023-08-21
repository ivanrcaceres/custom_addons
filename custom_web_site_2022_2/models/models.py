# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class CustomResPartner(models.Model):
    _inherit = 'res.partner'
    ruc = fields.Char(string='RUC o CI')
    # vat = fields.Char(string='Ruc o Num. de Doc.', required='True')
    vat = fields.Char(index=True, required=True,
                      help="The Tax Identification Number. Complete it if the contact is subjected to government taxes. Used in some legal statements.")
    #@api.model
    #def create(self, vals):
     #   vals['ruc'] = vals['vat']
        # Consultar otros modelos
      #  rec = super(CustomResPartner, self).create(vals)
#
       # return rec

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
