from odoo import models, fields, api
from odoo.exceptions import ValidationError

class VotingCenterGeneratorWizard(models.TransientModel):
    _name = 'vote_management.wizard_generate_voting_centers'
    _description = 'Wizard for generating voting centers'

    district_id = fields.Many2one('vote_management.district', string="District", required=True)
    num_centers = fields.Integer(string="Number of centers", required=True)
    num_voters = fields.Integer(string="Expected Voters per center", required=True)
    num_ballots = fields.Integer(string="Number of Ballots per center", required=True)

    @api.constrains('num_centers')
    def _check_positive_values(self):
        for record in self:
            if record.num_centers <= 0:
                raise ValidationError("Number of centers must be greater than zero.")

    def action_generate_centers(self):
        self.ensure_one()
        if not self.district_id:
            raise ValidationError("You must select a district.")

        centers = self.env['vote_management.voting_center']
        for i in range(1, self.num_centers + 1):
            name = f"Center {self.district_id.name} ({i})"
            centers.create({
                'name': name,
                'district_id': self.district_id.id,
                'num_voters': self.num_voters,
                'num_ballots': self.num_ballots,
            })
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }