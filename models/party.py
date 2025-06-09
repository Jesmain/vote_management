from odoo import models, fields, api

class Party(models.Model):
    _name = 'vote_management.party'
    _description = 'Partido Político'

    name = fields.Char(string="Party name", required=True)
    code = fields.Char(string="Internal code", readonly=True)

    _sql_constraints = [
        ("code_unique", "UNIQUE(code)", "A party's internal code must be unique"),
    ]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('vote_management.party') or 'PARTY000'
        return super().create(vals)