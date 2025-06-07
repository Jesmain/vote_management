from odoo import models, fields, api

class DistrictResult(models.Model):
    _name = 'vote_management.district_result'
    _description = 'Election results for a single district'

    election_result_id = fields.Many2one(
        'vote_management.election_result',
        required=True,
        ondelete='cascade',
        readonly=True
    )
    district_id = fields.Many2one('vote_management.district', required=True, readonly=True)
    expected_votes = fields.Integer(string="Expected votes", readonly=True)
    received_votes = fields.Integer(string="Received votes", readonly=True)
    absent_votes = fields.Integer(string="Absent votes", readonly=True)
    invalid_votes = fields.Integer(string='Invalid votes', readonly=True)
    num_mps = fields.Integer(string="Number of members of parliament", readonly=True)
    voting_center_ids = fields.Many2many('vote_management.voting_center', string='Voting centers', relation='district_result_voting_center_rel')
    party_result_ids = fields.One2many(
        'vote_management.result_line',
        'district_result_id',
        string="Results per party",
        readonly=True
    )
