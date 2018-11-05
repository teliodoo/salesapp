# -*- coding: utf-8 -*-
from odoo import http

# class TeliUsers(http.Controller):
#     @http.route('/teli_users/teli_users/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/teli_users/teli_users/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('teli_users.listing', {
#             'root': '/teli_users/teli_users',
#             'objects': http.request.env['teli_users.teli_users'].search([]),
#         })

#     @http.route('/teli_users/teli_users/objects/<model("teli_users.teli_users"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('teli_users.object', {
#             'object': obj
#         })
