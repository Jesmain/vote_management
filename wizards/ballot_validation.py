from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class BallotValidationWizard(models.TransientModel):
    _name = 'vote_management.wizard_validate_ballots'
    _description = 'Ballot Validation Wizard'

    token = fields.Char(string="Ballot full token", required=True)
    suffix = fields.Char(string="Chosen suffix")

    def validate_vote(self):
        self.ensure_one()
        ballot = self.env['vote_management.ballot'].search([
            ('name', '=', self.token),
            ('checked', '=', False)
        ], limit=1)

        if not ballot:
            raise ValidationError("A ballot with that token couldn't be found or has already been used.")
        
        ballot.checked = True
        ballot.selected_suffix = self.suffix

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': "Registered vote",
                'message': f"The vote was {'valid' if ballot.valid else 'invalid'}.",
                'type': 'success' if ballot.valid else 'danger',
                'sticky': False,
            }
        }
