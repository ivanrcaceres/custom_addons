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
