import string
import secrets
import hmac
import hashlib
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Ballot(models.Model):
    _name = 'vote_management.ballot'
    _description = 'Ballot'

    # name ('Full token') is base_token + center_token
    name = fields.Char(string='Full token', readonly=True)
    base_token = fields.Char(string='Base token', readonly=True)
    voting_center_id = fields.Many2one('vote_management.voting_center', string='Voting center', readonly=True)
    center_token = fields.Char(string='Center token', related='voting_center_id.token')
    suffix_ids = fields.One2many('vote_management.party_suffix', inverse_name='ballot_id', string='Suffix', readonly=True)
    district_id = fields.Many2one('vote_management.district', related='voting_center_id.district_id', string='District', store=True)
    election_id = fields.Many2one('vote_management.election', string='Election', required=True, readonly=True)
    simulated = fields.Boolean(related='election_id.simulated', store=True)

    # These fields are for backend use
    checked = fields.Boolean(default=False, store=True, readonly=True)
    valid = fields.Boolean(default=False, compute="_compute_state", store=True, readonly=True)
    # This field is for vote counting
    selected_suffix = fields.Char(string='Chosen suffix', readonly=True)

    @api.model
    def create(self, vals):
        center = self.env['vote_management.voting_center'].browse(vals['voting_center_id'])
        election = self.env['vote_management.election'].browse(vals['election_id'])
        base_token = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(9))
        full_token = base_token + center.token

        vals.update({
            'base_token': base_token,
            'name': full_token,
        })
        record = super().create(vals)
        
        suffixes = record._generate_party_suffixes(center.district_id.party_ids, election.key)
        record.suffix_ids = [(4, suffix.id) for suffix in suffixes]
        return record

    def _generate_party_suffixes(self, parties, key):
        party_suffix = self.env['vote_management.party_suffix']
        suffixes = []
        for party in parties:
            message = (self.name + party.code).encode()
            coded_key = key.encode()
            suffix = hmac.new(coded_key, message, hashlib.sha256).hexdigest()[:6]
            suffixes.append(party_suffix.create({
                'ballot_id': self.id,
                'party_id': party.id,
                'value': suffix,
            }))
        return suffixes

    @api.depends('selected_suffix', 'suffix_ids.value')
    def _compute_state(self):
        for ballot in self:
            if ballot.selected_suffix:
                ballot.valid = ballot.selected_suffix in ballot.suffix_ids.mapped('value')
            else:
                ballot.valid = False

    def write(self, vals):
        if 'checked' in vals and vals['checked']:
            for record in self:
                if record.election_id.state == 'finished':
                    raise ValidationError("You can't change a ballot after the election is finished.")
        return super().write(vals)

    def unlink(self):
        for record in self:
            election = record.election_id
            if election.state == 'finished' and not record.simulated:
                raise ValidationError("You can't delete the ballots of a finished election.")
        return super().unlink()


class PartySuffix(models.Model):
    _name = 'vote_management.party_suffix'
    _description = 'Party suffix'

    ballot_id = fields.Many2one('vote_management.ballot', string='Ballot', required=True, ondelete='cascade' )
    party_id = fields.Many2one('vote_management.party', string='Party', required=True)
    value = fields.Char(string='Value', readonly=True)