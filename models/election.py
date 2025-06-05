from odoo import models, fields, api

class Election(models.Model):
    _name = 'vote_management.election'
    _description = 'Elección'

    name = fields.Char(string='Election title', required=True)
    closing_date = fields.Date(string='Closing date')
    districts_ids = fields.Many2many('vote_management.district', string='Districts')
    result_id = fields.Many2one('vote_management.result', string='Result')
    key = fields.Char(string='Key', required=True)