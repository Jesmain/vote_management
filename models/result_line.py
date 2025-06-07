from odoo import models, fields, api

class ResultLine(models.Model):
    _name = 'vote_management.result_line'
    _description = 'Votes for a party, global or per district'

    party_id = fields.Many2one('vote_management.party', string="Party", required=True)
    votes = fields.Integer(string="Votes received", required=True)
    num_mps = fields.Integer(string='Members of parliament electected')
    # One of these will always be empty
    election_result_id = fields.Many2one('vote_management.election_result')
    district_result_id  = fields.Many2one('vote_management.district_result')