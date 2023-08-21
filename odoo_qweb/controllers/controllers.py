# -*- coding: utf-8 -*-
import io
from odoo import models, fields, api, exceptions, _
from odoo.http import request

from odoo.exceptions import ValidationError
from odoo import fields, models, exceptions, api
from datetime import datetime, timedelta, time, date
from datetime import datetime
# -*- coding: utf-8 -*-
from odoo import http
# import certificados
# from django.http.response import JsonResponse, HttpResponse
from string import ascii_uppercase

# from openpyxl import Workbook
# from openpyxl.styles import Font, Border, Alignment, Side, PatternFill
# from openpyxl import Workbook

import xlwt
import base64
import xlsxwriter
from io import StringIO



from odoo.addons.web.controllers.main import serialize_exception,content_disposition

class Certificados2(http.Controller):
    @http.route('/excel/<string:desde>/<string:hasta>', auth='public')
    def index(self,desde=None,hasta=None, **kw):
        print('desde')
        print(desde)
        print('hasta')
        print(hasta)
        desde = datetime.strptime(desde,'%Y-%m-%d')
        hasta = datetime.strptime(hasta, '%Y-%m-%d')
        print('##')
        print(desde)
        print(hasta)

        posorder = http.request.env['pos.order'].search([('date_order', '>=', desde),('date_order', '<=', hasta)])
        print(posorder)




        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 0, 'Cedula')
        worksheet.write(0, 1, 'RUC')
        worksheet.write(0, 2, 'Nombre o Razon Social')
        worksheet.write(0, 3, 'Tipo de comprobante')
        worksheet.write(0, 4, 'Timbrado')
        worksheet.write(0, 5, 'Numero de comprobante')
        worksheet.write(0, 6, 'Condicion')
        worksheet.write(0, 7, 'Fecha de Emision')
        worksheet.write(0, 8, 'Importe total del comprobante')
        worksheet.write(0, 9, 'Importe exenta')
        worksheet.write(0, 10, 'Total gravada 5% (IVA incluido)')
        worksheet.write(0, 11, 'IVA 5%')
        worksheet.write(0, 12, 'Total gravada 10% (IVA incluido)')
        worksheet.write(0, 13, 'IVA 10%')

        row = 0
        for pos in posorder:
            pos_config = http.request.env['pos.config'].browse([pos.session_id.config_id.id])
            print(pos.id)
            pos_lines = http.request.env['pos.order.line'].search([('order_id', '=', pos.id)])
            iva5 = 0
            iva10 = 0
            grab5 = 0
            grab10 = 0
            subtotal5 = 0
            subtotal10 = 0

            for line in pos_lines:

                producto = http.request.env['product.template'].browse([line.product_id])

                sub = line.price_subtotal_incl - line.price_subtotal
                piva5 = line.price_subtotal_incl / 21
                piva10 = line.price_subtotal_incl / 11
                if sub == piva5:
                    subtotal5 = line.price_subtotal_incl
                elif sub == piva10:
                    subtotal10 = line.price_subtotal_incl
                else:
                    execta = line.price_subtotal_incl


            iva5 = subtotal5 / 21
            iva10 = subtotal10 / 11
            grab5 = iva5 * 20
            grab10 = iva10 * 10



            row = row + 1
            worksheet.write(row, 0, pos.partner_id.ci)
            worksheet.write(row, 1, pos.partner_id.rucdv)
            worksheet.write(row, 2, pos.partner_id.name)
            worksheet.write(row, 3, 'factura')
            worksheet.write(row, 4, pos_config.timbrado)
            worksheet.write(row, 5, pos.order_fact)
            worksheet.write(row, 6, 'Contado')
            worksheet.write(row, 7, str(pos.date_order))
            worksheet.write(row, 8, pos.amount_total)
            worksheet.write(row, 9, '0')
            worksheet.write(row, 10, subtotal5)
            worksheet.write(row, 11, iva5)
            worksheet.write(row, 12, subtotal10)
            worksheet.write(row, 13, iva10)



        workbook.close()
        output.seek(0)
        print (self)

        return request.make_response(output,
                                     [('Content-Type',
                                       'application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet'),
                                      ('Content-Disposition', content_disposition('libro_diario.xlsx'))])


# -*- coding: utf-8 -*-
# from odoo import http


# class OdooQweb(http.Controller):
#     @http.route('/odoo_qweb/odoo_qweb/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_qweb/odoo_qweb/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_qweb.listing', {
#             'root': '/odoo_qweb/odoo_qweb',
#             'objects': http.request.env['odoo_qweb.odoo_qweb'].search([]),
#         })

#     @http.route('/odoo_qweb/odoo_qweb/objects/<model("odoo_qweb.odoo_qweb"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_qweb.object', {
#             'object': obj
#         })
