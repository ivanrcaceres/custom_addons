# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class Visit(models.Model):
    _name = 'custom_web_site.visit'
    _description = 'Visit'

    name = fields.Char(string='Descripción')
    customer = fields.Many2one(string='Cliente', comodel_name='res.partner')
    date = fields.Datetime(string='Fecha')
    type = fields.Selection([('P', 'Presencial'), ('W', 'WhatsApp'), ('T', 'Telefónico')], string='Tipo', required=True)
    done = fields.Boolean(string='Realizada', readonly=True)
    image = fields.Binary(string='Imagen')

    def toggle_state(self):
        self.done = not self.done

    #ORM
    def f_create(self):
        visit = {
            'name': 'ORM test',
            'customer': 1,
            'date': str(datetime.date(2020, 8, 6)),
            'type': 'P',
            'done': False
        }
        print(visit)
        self.env['custom_web_site.visit'].create(visit)

    def f_search_update(self):
        visit = self.env['custom_web_site.visit'].search([('name', '=', 'ORM test')])
        print('search()', visit, visit.name)

        visit_b = self.env['custom_web_site.visit'].browse([8])
        print('browse()', visit_b, visit_b.name)

        visit.write({
            'name': 'ORM test write'
        })

    def f_delete(self):
        visit = self.env['custom_web_site.visit'].browse([8])
        visit.unlink()


class VisitReport(models.AbstractModel):

    _name='report.custom_web_site.report_visit_card'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('custom_web_site.report_visit_card')
        return {
            'doc_ids': docids,
            'doc_model': self.env['custom_web_site.visit'],
            'docs': self.env['custom_web_site.visit'].browse(docids)
        }


class CustomSaleOrder(models.Model):

    _inherit = 'sale.order'

    zone = fields.Selection([('N', 'Norte'), ('C', 'Centro'), ('S', 'Sur')], string='Zona comercial')

class CustomResPartner(models.Model):
    _inherit = 'res.partner'
    ruc = fields.Char(string='Numero de documento')
    vat = fields.Char(string='Ruc o Num. de Doc.', index=True, required=True,
                      help="The Tax Identification Number. Complete it if the contact is subjected to government taxes. Used in some legal statements.")
#    @api.model
#    def create(self, vals):
#        # Consultar otros modelos
#        print('holaaa')
#        vals['ruc'] = self.vat
#        rec = super(CustomResPartner, self).create(vals)
#        return rec



#from odoo import models, fields, api
#
#class WebsiteSale(ProductConfiguratorController):
#    _inherit = 'website.WebsiteSale'
#
#    def _get_mandatory_billing_fields(self):
#        print("hola")
#        return ["name", "email", "street","vat", "city", "country_id"]
