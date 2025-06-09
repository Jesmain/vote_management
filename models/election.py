import random
from collections import defaultdict
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Election(models.Model):
    _name = 'vote_management.election'
    _description = 'Election'

    name = fields.Char(string='Election title', required=True)
    district_ids = fields.Many2many('vote_management.district', string='Districts', required=True, readonly=True)
    result_id = fields.Many2one('vote_management.election_result', string='Result', readonly=True)
    key = fields.Char(string='Key', required=True, readonly=True)
    state = fields.Selection([
        ('in_progress', 'In progress'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
    ], string='Election state', readonly=True)

    simulated = fields.Boolean(string='simulated', default=False)

    _sql_constraints = [
        ("key_unique", "UNIQUE(key)", "The encryption key must be unique to each election"),
    ]
    def action_open_finalize_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'vote_management.wizard_finish_election',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_election_id': self.id}
        }

    def action_cancel_election(self):
        self.ensure_one()
        self.env['vote_management.ballot'].search([
            ('election_id', '=', self.id)
        ]).unlink()
        self.state = 'cancelled'

    def action_simulate_votes(self):
        self.ensure_one()
        if self.simulated:
            raise ValidationError("This election has already been simulated.")
        if self.state != 'in_progress':
            raise ValidationError("Only elections in progress can be simulated.")
        
        all_ballots = self.env['vote_management.ballot'].search([
            ('election_id', '=', self.id),
            ('checked', '=', False),
            ('selected_suffix', '=', False),
        ])
        if not all_ballots:
            raise ValidationError("No available ballots to simulate.")

        centers = [
            center
            for district in self.district_ids
            for center in district.voting_center_ids
        ]

        ballots_by_center = defaultdict(list)
        for b in all_ballots:
            ballots_by_center[b.voting_center_id.id].append(b)

        party_ids = {p.id for d in self.district_ids for p in d.party_ids}
        
        party_ids = list(party_ids)
        used_ballots = 0

        for center in centers:
            center_ballots = ballots_by_center.get(center.id, [])
            expected = center.num_voters

            selected_ballots = random.sample(center_ballots, expected)

            num_absent = round(expected * 0.10)
            num_invalid = round(expected * 0.10)

            start = num_absent
            for b in selected_ballots[start:start + num_invalid]:
                b.checked = True
            start += num_invalid

            for b in selected_ballots[start:]:
                random_party_id = random.choice(party_ids)
                suffix = b.suffix_ids.filtered(lambda s: s.party_id.id == random_party_id)
                if suffix:
                    b.selected_suffix = suffix[0].value
                    b.checked = True

            used_ballots += expected

        self.simulated = True

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': "Simulation complete",
                'message': f"{used_ballots} ballots have been used (based on expected voters).",
                'type': 'success',
                'sticky': False,
            }
        }
