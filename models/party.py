from odoo import models, fields, api

class Party(models.Model):
    _name = 'vote_management.party'
    _description = 'Partido Político'

    name = fields.Char(string="Party name", required=True)
    code = fields.Char(string="Internal code", required=True)