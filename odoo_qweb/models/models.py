# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OrdersReports(models.TransientModel):
    _name = 'odoo_qweb.orders_report'

    date_from = fields.Date(string='Fecha desde')
    date_to = fields.Date(string='Fecha hasta')

    def get_report(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to
        }
        return self.env.ref('odoo_qweb.report_orders').report_action(self, data=data)

    def excel(self):

        # palabra = str(self.format_date(self.date_from)) + 'fefe' + str(self.format_date(self.date_from))
        desde = str(self.date_from)
        hasta = str(self.date_to)
        return {
                'type': 'ir.actions.act_url',
                'url': '/excel/'+desde+'/'+hasta,
                'target': 'self'
                }
    def format_date(self, date):
        date_parts = date.split('-')
        return '{}/{}/{}'.format(date_parts[2], date_parts[1], date_parts[0])


class OrdersCard(models.AbstractModel):
    _name = 'report.odoo_qweb.report_orders'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'docs': self.env['sale.order'].search_read([('date_order', '>=', data['date_from']),
                                                        ('date_order', '<=', data['date_to'])],
                                                       ['name', 'date_order', 'amount_total']),
            'data': data,
            'company': self.env.user.company_id,
            'date_from': self.format_date(data['date_from']),
            'date_to': self.format_date(data['date_to'])
        }

    def format_date(self, date):
        date_parts = date.split('-')
        return '{}/{}/{}'.format(date_parts[2], date_parts[1], date_parts[0])