from odoo import models, fields, api

class Party(models.Model):
    _name = 'vote_management.party'
    _description = 'Partido Político'

    name = fields.Char(string="Nombre del Partido", required=True)
    code = fields.Char(string="Código Interno", required=True)