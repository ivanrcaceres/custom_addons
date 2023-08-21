# -*- coding: utf-8 -*-
import json
# from django.http import JsonResponse, HttpResponse
from odoo import http

import io
from odoo import models, fields, api, exceptions, _
from odoo.http import request

from odoo.exceptions import ValidationError
from odoo import fields, models, exceptions, api
from datetime import datetime, timedelta, time, date
# -*- coding: utf-8 -*-
from odoo import http
# import certificados
# from django.http.response import JsonResponse, HttpResponse
from string import ascii_uppercase


from odoo.http import Response
from reportlab.pdfgen import canvas
import time
#from relacion_timbrado_order.models.models import RelacionTimbradoFact


class FacturaController(http.Controller):
    @http.route("/check_method_get", auth='none', method=['GET'])
    def check_method_get(self, **values):
        output = {
            'results': {
                'code': 200,
                'message': 'OK'
            }
        }
        return 'hola'

    @http.route('/certificados', auth='public')
    def index(self, **kw):
        print('index')
        # return 'hola'
        try:
            return Response(json.dumps('hola', ensure_ascii=False).encode('utf-8'),
                            content_type='application/json;charset=utf-8', status=200)
        except Exception as e:
            return Response(json.dumps({'error': str(e)}),
                            content_type='application/json;charset=utf-8', status=505)


    @http.route('/prueba/<a>/<b>', auth='public', website=True)
    def prueba(self,a,b, **kw):
        # a = self[0].company_id.id

        aaa = http.request.env['res.company'].search([('id', '=', 1)])

        # datos = request.params['nombre']
        # datos2 = request.params['apellido']

        print('&&&&&&')
        # print(datos)
        # print(datos2)
        print(aaa[0].ultimo_numero_completo)


        print(a)
        print(b)

        relacionnn = {
            'venta': a,
            'factura': aaa[0].ultimo_numero_completo
        }
        print(relacionnn)
        aaa = http.request.env['relacion_timbrado_order.relaciontimbfact'].sudo().create(relacionnn)

        # datos = request.params['nombre']
        # datos2 = request.params['apellido']

        print('&&&&&&')
        # print(datos)
        # print(datos2)

        return "hola desde el controller"

    @http.route('/prueba4', auth='public', website=True)
    def prueba4(self, **kw):
        # a = self[0].company_id.id

        aaa = http.request.env['res.company'].search([('id', '=', 1)])

        # datos = request.params['nombre']
        # datos2 = request.params['apellido']

        print('&&&&&&')
        # print(datos)
        # print(datos2)
        print(aaa[0].ultimo_numero_completo)

        return aaa[0].ultimo_numero_completo

    @http.route('/prueba5', auth='public', website=True)
    def prueba5(self, **kw):
        # a = self[0].company_id.id

        aaa = http.request.env['res.company'].search([('id', '=', 1)])

        # datos = request.params['nombre']
        # datos2 = request.params['apellido']

        print('&&&&&&')
        # print(datos)
        # print(datos2)
        print(aaa[0].ultimo_numero_completo)

        return aaa[0].ultimo_numero_completo

    @http.route('/prueba2023/<a>', auth='public', website=True)
    def prueba5555(self,a, **kw):

        aaa = http.request.env['pos.order'].search([('pos_reference', '=', a)])
        print(aaa)
        return aaa.order_fact

    @http.route('/prueba20232/<a>', auth='public', website=True)
    def pruebaprueba20232(self, a, **kw):
        print('#########################')
        time.sleep(2)
        print(a)
        print(self)
        enlatabla = http.request.env['pos.order'].search([('pos_reference', '=', a)])
        print(enlatabla)
        print(enlatabla.order_fact)



        calculado = http.request.env['pos.config'].browse([enlatabla.session_id.config_id.id])
        # pos_config = self.env['pos.config'].browse([rec.session_id.config_id.id])
        print('&&&&&&')
        print(calculado)
        print(calculado.ultimo_numero_completo)

        data = {
            'enlatabla':enlatabla.order_fact,
            'calculado':calculado.ultimo_numero_completo
        }
        print(data)


        return Response(json.dumps(data),
                        content_type='application/json;charset=utf-8')


    @http.route('/puntomiles/<a>', auth='public', website=True)
    def puntomiles(self,a, **kw):
        print(a)
        a = int(a)
        b = round(a, 0)
        print(b)
        print("{:,}".format(b))
        print("{:,}".format(b).replace(',', '~').replace('.', ',').replace('~', '.'))
        return "{:,}".format(b).replace(',', '~').replace('.', ',').replace('~', '.')

    # @http.route('/imprimir_ticket/', auth='public', website=True)
    # def imprimir_ticket(self, **kw):
    #
    #     response = http.request(content_type='application/pdf')
    #
    #     fecha = datetime.now()
    #
    #     nombredelpdf = str(fecha.date()) + str(fecha.time()) + '.pdf'
    #
    #     response['Content-Disposition'] = 'attachment; filename= Factura ' + nombredelpdf
    #
    #     p = canvas.Canvas(response)
    #
    #     for i in range(0, 1):
    #         # p.drawString(400, 810, "1 Esto es un recibo. "+id)
    #         p.drawString(400, 810, "numerodeficha")
    #         p.drawString(485, 810, "carrera")
    #         p.drawString(15, 740, "nombre")
    #
    #         p.showPage()
    #
    #     p.save()
    #     return response



#     @http.route('/odoo_qweb/odoo_qweb/objects/<model("odoo_qweb.odoo_qweb"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_qweb.object', {
#             'object': obj
#         })

