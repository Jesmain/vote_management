from odoo import models, fields, api

class District(models.Model):
    _name = 'vote_management.district'
    _description = 'Voting district'

    name = fields.Char(required=True)
    state_id = fields.Many2one('res.country.state', string='State', required=True)
    party_ids = fields.Many2many('vote_management.party', string="Participating parties")
    voting_center_ids = fields.Many2many('vote_management.voting_center', string='Voting centers')