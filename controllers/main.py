from odoo import http
from odoo.http import request

class VoteValidationController(http.Controller):

    @http.route(['/verify_vote'], type='http', auth='public', website=True)
    def verify_vote_form(self, **kwargs):
        return request.render('vote_management.verify_vote_template', {})

    @http.route(['/verify_vote/submit'], type='http', auth='public', website=True, csrf=False)
    def verify_ballot_submit(self, **post):
        token = post.get('token')
        result = None
        party_suffix = None
        party_name = None

        if token:
            ballot = request.env['vote_management.ballot'].sudo().search([('name', '=', token)], limit=1)
            if ballot:
                result = 'valid' if ballot.valid else 'not_valid'
                party_suffix = ballot.selected_suffix if ballot.valid else None
                if party_suffix:
                    for suffix in ballot.suffix_ids:
                        if party_suffix == suffix.value:
                            party_name = suffix.party_id.name
            else:
                result = 'not_found'

        return request.render('vote_management.verify_vote_template', {
            'token': token,
            'result': result,
            'party_suffix': party_suffix,
            'party_name': party_name
        })
