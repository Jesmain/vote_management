from odoo import models, fields, api

class CreateElectionWizard(models.TransientModel):
    _name = 'vote_management.wizard_create_election'
    _description = 'Wizard to create an election and its ballots'

    name = fields.Char(string="Election name", required=True)
    hmac_key = fields.Char(string="HMAC Key", required=True)
    district_ids = fields.Many2many('vote_management.district', string="Districts", required=True, relation='create_election_wizard_party_rel', domain="[('voting_center_ids', '!=', False)]")

    def action_create_election(self):
        election = self.env['vote_management.election'].create({
            'name': self.name,
            'key': self.hmac_key,
            'state': 'in_progress'
        })

        for district in self.district_ids:
            election.write({'district_ids': [(4, district.id)]})

            for center in district.voting_center_ids:
                for i in range(center.num_ballots):
                    self.env['vote_management.ballot'].create({
                        'election_id': election.id,
                        'voting_center_id': center.id,
                    })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'vote_management.election',
            'view_mode': 'form',
            'res_id': election.id,
            'target': 'current'
        }
