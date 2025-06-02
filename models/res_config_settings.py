from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    password = fields.Char(string="Calve oculta")

    @api.model
    def get_values(self):
        res = super().get_values()
        IrConfigParam = self.env['ir.config_parameter'].sudo()
        res.update(
            my_custom_field=IrConfigParam.get_param('vote_management.password', default=''),
        )
        return res

    def set_values(self):
        super().set_values()
        IrConfigParam = self.env['ir.config_parameter'].sudo()
        IrConfigParam.set_param('vote_management.password', self.password or '')
