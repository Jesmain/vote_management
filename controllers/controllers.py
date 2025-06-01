# -*- coding: utf-8 -*-
# from odoo import http


# class VoteManagement(http.Controller):
#     @http.route('/vote_management/vote_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vote_management/vote_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('vote_management.listing', {
#             'root': '/vote_management/vote_management',
#             'objects': http.request.env['vote_management.vote_management'].search([]),
#         })

#     @http.route('/vote_management/vote_management/objects/<model("vote_management.vote_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vote_management.object', {
#             'object': obj
#         })
