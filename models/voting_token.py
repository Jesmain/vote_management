import string
import random
import hmac
import hashlib
from odoo import models, fields, api
from odoo.exceptions import UserError

class VotingToken(models.Model):
    _name = 'vote_management.voting_token'
    _description = 'Token de Papeleta'

    name = fields.Char(string="Token Base", required=True, default=lambda self: self._generate_token())
    suffix_ids = fields.One2many('vote_management.voting_suffix', 'token_id', string="Sufijos")
    district_id = fields.Many2one('vote_management.district', string="Circunscripción", required=True)

    def _generate_token(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def action_generate_suffixes(self):
        secret = self.env['ir.config_parameter'].sudo().get_param('vote_management.secret_key')
        if not secret:
            raise UserError("Debes definir una clave secreta en Configuración del sistema (vote_management.secret_key).")

        for record in self:
            # Limpiamos sufijos existentes si existen
            record.suffix_ids.unlink()

            for party in record.district_id.party_ids:
                raw = f"{record.name}{party.code}"
                suffix = hmac.new(
                    secret.encode(), raw.encode(), hashlib.sha256
                ).hexdigest()[:6]
                self.env['vote_management.voting_suffix'].create({
                    'token_id': record.id,
                    'party_id': party.id,
                    'suffix': suffix,
                })

class VotingSuffix(models.Model):
    _name = 'vote_management.voting_suffix'
    _description = 'Sufijo generado para partido'

    token_id = fields.Many2one('vote_management.voting_token', string="Token Base", required=True, ondelete="cascade")
    party_id = fields.Many2one('vote_management.party', string="Partido", required=True)
    suffix = fields.Char(string="Sufijo", required=True)
