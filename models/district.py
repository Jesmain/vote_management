from odoo import models, fields, api

class District(models.Model):
    _name = 'vote_management.circumscription'
    _description = 'Circunscripción Electoral'

    name = fields.Char(required=True)
    party_ids = fields.Many2many('vote_management.party', string="Partidos disponibles")
