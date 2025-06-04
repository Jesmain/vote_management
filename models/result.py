from odoo import models, fields, api

class Result(models.Model):
    _name = 'vote_management.result'
    _description = 'Election result'
    # TODO Determine a way to have this model store data immutably