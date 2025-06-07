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
        if self.state != 'in_progress':
            raise ValidationError("Only elections in progress can be simulated.")

        ballots = self.env['vote_management.ballot'].search([
            ('election_id', '=', self.id),
            ('checked', '=', False),
            ('selected_suffix', '=', False),
        ])
        if not ballots:
            raise ValidationError("No available ballots to simulate.")

        party_ids = {p.id for d in self.district_ids for p in d.party_ids}
        if not party_ids:
            raise ValidationError("No parties found in this election.")

        winning_party_id = random.choice(list(party_ids))
        other_party_ids = [pid for pid in party_ids if pid != winning_party_id] or [winning_party_id]

        ballots_by_center = defaultdict(list)
        for b in ballots:
            ballots_by_center[b.voting_center_id.id].append(b)

        for ballots_in_center in ballots_by_center.values():
            total = len(ballots_in_center)
            if total == 0:
                continue

            random.shuffle(ballots_in_center)

            num_absent  = round(total * 0.10)
            num_invalid = round(total * 0.10)
            num_valid   = total - num_absent - num_invalid
            num_winner  = round(num_valid * 0.60)

            # Absent ballots aren't modified, since they already have checked = False

            start = num_absent

            for b in ballots_in_center[start:start + num_invalid]:
                b.checked = True
            start += num_invalid

            for b in ballots_in_center[start:start + num_winner]:
                suffixes = b.suffix_ids.filtered(lambda s: s.party_id.id == winning_party_id)
                if suffixes:
                    b.selected_suffix = random.choice(suffixes).value
                    b.checked = True
            start += num_winner

            for b in ballots_in_center[start:]:
                suffixes = b.suffix_ids.filtered(lambda s: s.party_id.id in other_party_ids)
                if suffixes:
                    b.selected_suffix = random.choice(suffixes).value
                    b.checked = True

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': "Simulation complete",
                'message': f"{len(ballots)} ballots have been used.",
                'type': 'success',
                'sticky': False,
            }
        }