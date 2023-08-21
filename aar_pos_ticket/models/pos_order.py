# -*- coding: utf-8 -*-
####################   AARSOL      ####################
#    AARSOL Pvt. Ltd.
#    Copyright (C) 2010-TODAY AARSOL(<http://www.aarsol.com>).
#    Author: Farooq Arif(<http://www.aarsol.com>)
#
#    It is forbidden to distribute, or sell copies of the module.
#
#    License:  OPL-1
####################   AARSOL      ####################

from odoo import api, fields, models, _
import base64
import json
import logging

_logger = logging.getLogger(__name__)

class pos_order(models.Model):
    _inherit = "pos.order"
    
    ean13 = fields.Char('Ean13')
    
    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(pos_order, self)._order_fields(ui_order)
        
        if ui_order.get('ean13', False):
            order_fields.update({
                'ean13': ui_order['ean13']
            })
            
        return order_fields

class ResUser(models.Model):
    _inherit = 'res.users'

    firstname = fields.Char()

    def _f_hola(self):
        return 'hola desde _f_hola'

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


class OrdersCard(models.AbstractModel):
    _name = 'report.odoo_qweb.report_orders'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'docs': [1,2],
            'data': {'saludos':'hola'},
            'company': self.env.user.company_id
        }
