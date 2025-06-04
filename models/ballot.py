import string
import random
import hmac
import hashlib
from odoo import models, fields, api
from odoo.exceptions import UserError

class Ballot(models.Model):
    _name = 'vote_management.ballot'
    _description = 'Ballot'

    # name ('Full token') is base_token + center_token
    name = fields.Char(string='Full token', readonly=True)
    base_token = fields.Char(string='Base token', readonly=True)
    voting_center_id = fields.Many2one('vote_management.voting_center', string='Voting center', readonly=True)
    center_token = fields.Char(string='Center token', related='voting_center_id.token')
    suffix_ids = fields.One2many('vote_management.party_suffix', inverse_name='token_id', string='Suffix', readonly=True)
    district_id = fields.Many2one('vote_management.district', related='voting_center_id.district_id', string='District')
    election_id = fields.Many2one('vote_management.election', string='Election')


class PartySuffix(models.Model):
    _name = 'vote_management.party_suffix'
    _description = 'Party suffix'

    token_id = fields.Many2one('vote_management.ballot', string='Ballot', required=True, ondelete='cascade' )
    party_id = fields.Many2one('vote_management.party', string='Party', required=True)
    suffix = fields.Char(string='Suffix', required=True)
