from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CreateDistrictsWizard(models.TransientModel):
    _name = 'vote_management.wizard_create_districts'
    _description = 'Wizard to create districts by country'

    country_id = fields.Many2one('res.country', string='Country', required=True)
    party_ids = fields.Many2many('vote_management.party', string='Parties to assign to each district', relation='create_district_wizard_party_rel')
    num_mps = fields.Integer(string='Mebers of parliament per district', required=True, default=1)

    def action_create_districts(self):
        state = self.env['res.country.state']
        district = self.env['vote_management.district']

        states = state.search([('country_id', '=', self.country_id.id)])
        if not states:
            raise ValidationError("The selected country has no associated states.")

        existing = district.search([('state_id', 'in', states.ids)])
        if existing:
            raise ValidationError("There's already districts created for this country.")

        for state in states:
            district.create({
                'name': state.name,
                'state_id': state.id,
                'num_mps': self.num_mps,
                'party_ids': [(6, 0, self.party_ids.ids)],
            })

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }