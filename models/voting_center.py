import string
import secrets
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class VotingCenter(models.Model):
    _name = 'vote_management.voting_center'
    _description = 'Voting center'

    name = fields.Char(string='Center name', required=True)
    token = fields.Char(string='Token', readonly=True) # Determined when the record is saved
    district_id = fields.Many2one('vote_management.district', string='District', required=True)
    state_id = fields.Many2one('res.country.state', string='State', related='district_id.state_id')
    # This is the amount of ballots to be created for this center in an election
    num_ballots = fields.Integer(string='Amount of ballots', required=True)

    @api.model
    def create(self, vals):
        district = self.env['vote_management.district'].search([('id', '=', vals['district_id'])])
        # The state's id's length must always be 3, padding or truncating as needed
        # Barring certain cases, like with the value 1000, the resulting token fragment should not be 000
        state_id_str = f"{int(district.state_id.id % 1000):03d}"
        random_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(4))
        token = state_id_str + random_part
        # The center's token must not changed once set for data congruence with previous ballots
        vals['token'] = token

        record = super(VotingCenter, self).create(vals)
        return record
    
    def write(self, vals):
        if 'district_id' in vals:
            for record in self:
                if record.district_id and vals['district_id'] != record.district_id.id:
                    raise ValidationError("You cannot change the voting center's district once it's set.")
        return super().write(vals)
    
    @api.constrains('num_ballots')
    def _check_values(self):
        for record in self:
            if record.num_ballots < 1:
                raise ValidationError('A voting center must print at least 1 ballot')