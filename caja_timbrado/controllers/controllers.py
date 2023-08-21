# -*- coding: utf-8 -*-
from odoo import http

# class CajaTimbrado(http.Controller):
#     @http.route('/caja_timbrado/caja_timbrado/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/caja_timbrado/caja_timbrado/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('caja_timbrado.listing', {
#             'root': '/caja_timbrado/caja_timbrado',
#             'objects': http.request.env['caja_timbrado.caja_timbrado'].search([]),
#         })

#     @http.route('/caja_timbrado/caja_timbrado/objects/<model("caja_timbrado.caja_timbrado"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('caja_timbrado.object', {
#             'object': obj
#         })