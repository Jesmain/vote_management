from odoo import models, fields, api

class Election(models.Model):
    _name = 'vote_management.election'
    _description = 'Elección'

    name = fields.Char(string='Election title', required=True)
    district_ids = fields.Many2many('vote_management.district', string='Districts', required=True, readonly=True)
    result_id = fields.Many2one('vote_management.result', string='Result')
    key = fields.Char(string='Key', required=True, readonly=True)
    state = fields.Selection([
        ('in_progress', 'In progress'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
    ], string='Election state', readonly=True)

    _sql_constraints = [
        ("key_unique", "UNIQUE(key)", "The encryption key must be unique to each election"),
    ]