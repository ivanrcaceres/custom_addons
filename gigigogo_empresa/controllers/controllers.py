# -*- coding: utf-8 -*-
from odoo import http

# class GigigogoEmpresa(http.Controller):
#     @http.route('/gigigogo_empresa/gigigogo_empresa/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gigigogo_empresa/gigigogo_empresa/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gigigogo_empresa.listing', {
#             'root': '/gigigogo_empresa/gigigogo_empresa',
#             'objects': http.request.env['gigigogo_empresa.gigigogo_empresa'].search([]),
#         })

#     @http.route('/gigigogo_empresa/gigigogo_empresa/objects/<model("gigigogo_empresa.gigigogo_empresa"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gigigogo_empresa.object', {
#             'object': obj
#         })