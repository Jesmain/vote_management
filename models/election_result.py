from odoo import models, fields, api

class ElectionResult(models.Model):
    _name = 'vote_management.election_result'
    _description = 'Global results for an election'

    name = fields.Char(string='Name', compute="_compute_name")
    election_id = fields.Many2one('vote_management.election', readonly=True, required=True)
    expected_votes = fields.Integer(string="Expected votes", readonly=True)
    received_votes = fields.Integer(string="Received votes", readonly=True)
    absent_votes = fields.Integer(string="Absent votes", readonly=True)
    invalid_votes = fields.Integer(string='Invalid votes', readonly=True)
    total_mps = fields.Integer(string="Total member of parliament", readonly=True)
    district_result_ids = fields.One2many(
        'vote_management.district_result',
        inverse_name='election_result_id',
        string="Results by district",
        readonly=True
    )
    party_result_ids = fields.One2many(
        'vote_management.result_line',
        inverse_name='election_result_id',
        string="Global result by parties",
        readonly=True
    )
    result_method = fields.Selection([
        ('majority', 'Majority'),
        ('percentage', 'Percentage'),
    ], string='Method used for calculation',
    readonly=True
    )

    @api.depends('election_id')
    def _compute_name(self):
        for record in self:
            if record.election_id:
                record.name = f"Result - {record.election_id.name}"