import string
import random
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class VotingCenter(models.Model):
    _name = 'vote_management.voting_center'
    _description = 'Voting center'

    name = fields.Char(string='Center name', required=True)
    token = fields.Char(string='Token', readonly=True) # Determined when the record is saved
    district_id = fields.Many2one('vote_management.district', string='District', required=True)
    state_id = fields.Many2one('res.country.state', string='State', related='district_id.state_id', domain="[('country_id.name', '=', 'United States')]")

    @api.model
    def create(self, vals):
        # The center's token must not changed once set for data congruence with previous ballots
        # The state's id's length must always be 3, padding or truncating as needed
        # Barring certain cases, like with the value 1000, the resulting token fragment should not be 000
        state_id_str = f"{int(vals.get('state_id', 0) % 1000):03d}"
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        token = state_id_str + random_part
        vals['token'] = token

        record = super(VotingCenter, self).create(vals)
        return record