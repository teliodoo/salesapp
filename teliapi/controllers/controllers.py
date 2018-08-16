# -*- coding: utf-8 -*-
from odoo import http

class Teliapi(http.Controller):
    @http.route('/teliapi/teliapi/', auth='public')
    def index(self, **kw):
        return "Hello, world"

#     @http.route('/teliapi/teliapi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('teliapi.listing', {
#             'root': '/teliapi/teliapi',
#             'objects': http.request.env['teliapi.teliapi'].search([]),
#         })

#     @http.route('/teliapi/teliapi/objects/<model("teliapi.teliapi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('teliapi.object', {
#             'object': obj
#         })
