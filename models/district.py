from odoo import models, fields, api
from odoo.exceptions import ValidationError

class District(models.Model):
    _name = 'vote_management.district'
    _description = 'Voting district'

    name = fields.Char(related='state_id.name')
    state_id = fields.Many2one('res.country.state', string='State', required=True)
    party_ids = fields.Many2many('vote_management.party', string="Participating parties")
    voting_center_ids = fields.One2many('vote_management.voting_center', inverse_name='district_id', string='Voting centers')
    num_mps = fields.Integer(string="Number of member of parliament", required=True)

    _sql_constraints = [
        ("state_id_unique", "UNIQUE(state_id)", "There can only be 1 district per state or province"),
    ]

    @api.constrains('num_mps', 'num_senators')
    def _check_minimum_representatives(self):
        for rec in self:
            if rec.num_mps < 1:
                raise ValidationError("Each district must have at least 1 member of parliament.")