from odoo import models, fields, api
from odoo.exceptions import ValidationError

class FinishElectionWizard(models.TransientModel):
    _name = 'vote_management.wizard_finish_election'
    _description = 'Wizard to finalize an election'

    election_id = fields.Many2one('vote_management.election', required=True)
    result_method = fields.Selection([
        ('majority', 'Majority'),
        ('percentage', 'Percentage'),
    ], string="Result method", required=True)

    def _get_checked_ballots(self):
        return self.env['vote_management.ballot'].search([
            ('election_id', '=', self.election_id.id),
            ('checked', '=', True),
        ])

    def _get_district_ballots(self, district, checked_ballots):
        ballots = self.env['vote_management.ballot']
        for ballot in checked_ballots:
            if ballot.voting_center_id in district.voting_center_ids:
                ballots |= ballot
        return ballots

    def _get_participating_center_ids(self, district, checked_ballots):
        district_ballots = self._get_district_ballots(district, checked_ballots)
        centers = []
        for ballot in district_ballots:
            cid = ballot.voting_center_id.id
            if cid not in centers:
                centers.append(cid)
        return centers

    def _create_district_result(self, district, election_result, checked_ballots):
        ballots = self._get_district_ballots(district, checked_ballots)

        expected = sum(center.num_voters for center in district.voting_center_ids)
        received = len(ballots)

        invalid = 0
        for b in ballots:
            if not b.valid:
                invalid += 1

        absent = expected - received

        centers = self._get_participating_center_ids(district, checked_ballots)

        return self.env['vote_management.district_result'].create({
            'election_result_id': election_result.id,
            'district_id': district.id,
            'expected_votes': expected,
            'received_votes': received,
            'absent_votes': absent,
            'invalid_votes': invalid,
            'num_mps': district.num_mps,
            'voting_center_ids': [(6, 0, centers)],
        })

    def action_confirm_finish(self):
        election = self.election_id

        checked = self._get_checked_ballots()
        if not checked:
            raise ValidationError("At least one vote must be counted before finishing the election.")

        for district in election.district_ids:
            district_ballots = self._get_district_ballots(district, checked)
            if not district_ballots:
                raise ValidationError(
                    f"District '{district.name}' has no counted votes. "
                    "All districts must have at least one vote."
                )

        total_expected = sum(
            center.num_voters
            for d in election.district_ids
            for center in d.voting_center_ids
        )
        total_received = len(checked)
        total_invalid = sum(1 for b in checked if not b.valid)
        total_absent = total_expected - total_received
        total_mps   = sum(d.num_mps for d in election.district_ids)

        election_result = self.env['vote_management.election_result'].create({
            'election_id': election.id,
            'expected_votes': total_expected,
            'received_votes': total_received,
            'absent_votes': total_absent,
            'invalid_votes': total_invalid,
            'total_mps': total_mps,
            'result_method': self.result_method,
        })
        election.result_id = election_result.id

        party_global_votes = {}
        for district in election.district_ids:
            district_ballots = self._get_district_ballots(district, checked)
            dr = self._create_district_result(district, election_result, checked)

            participating_parties = district.party_ids

            votes_by_party = { p.id: 0 for p in participating_parties }

            for ballot in district_ballots:
                if not ballot.valid or not ballot.selected_suffix:
                    continue

                suffix = ballot.suffix_ids.filtered(
                    lambda s: s.value == ballot.selected_suffix
                )
                if not suffix or not suffix[0].party_id:
                    continue
                pid = suffix[0].party_id.id
                if pid in votes_by_party:
                    votes_by_party[pid] += 1
                    party_global_votes[pid] = party_global_votes.get(pid, 0) + 1

            total_votes = sum(votes_by_party.values())
            max_votes = max(votes_by_party.values(), default=0)

            district_lines = []
            assigned_mps = 0

            if self.result_method == 'majority' and max_votes > 0:
                winners = [pid for pid, v in votes_by_party.items() if v == max_votes]
                for pid, votes in votes_by_party.items():
                    if pid in winners:
                        mps = district.num_mps // len(winners)
                    else:
                        mps = 0
                    district_lines.append({
                        'district_result_id': dr.id,
                        'party_id': pid,
                        'votes': votes,
                        'num_mps': mps,
                    })
                    assigned_mps += mps

            elif self.result_method == 'percentage' and total_votes:
                distribution = {pid: 0 for pid in votes_by_party}
                remainders = []
                total_assigned = 0

                for pid, votes in votes_by_party.items():
                    proportion = (votes / total_votes) * district.num_mps
                    base = int(proportion)
                    remainder = proportion - base
                    distribution[pid] = base
                    remainders.append((remainder, pid))
                    total_assigned += base

                remaining = district.num_mps - total_assigned
                remainders.sort(reverse=True)
                for i in range(remaining):
                    _, pid = remainders[i]
                    distribution[pid] += 1

                for pid, mps in distribution.items():
                    district_lines.append({
                        'district_result_id': dr.id,
                        'party_id': pid,
                        'votes': votes_by_party[pid],
                        'num_mps': mps,
                    })
                    assigned_mps += mps

            if assigned_mps > district.num_mps:
                excess = assigned_mps - district.num_mps
                district_lines.sort(key=lambda L: L['num_mps'], reverse=True)
                for line in district_lines:
                    if line['num_mps'] >= excess:
                        line['num_mps'] -= excess
                        break

            for vals in district_lines:
                self.env['vote_management.result_line'].create(vals)


        party_global_mps = {pid: 0 for pid in party_global_votes}

        for dr in election_result.district_result_ids:
            for line in dr.party_result_ids:
                pid = line.party_id.id
                if pid in party_global_mps:
                    party_global_mps[pid] += line.num_mps

        for pid, votes in party_global_votes.items():
            self.env['vote_management.result_line'].create({
                'election_result_id': election_result.id,
                'district_result_id': False,
                'party_id': pid,
                'votes': votes,
                'num_mps': party_global_mps.get(pid, 0),
        })


        absent_ballots = self.env['vote_management.ballot'].search([
        ('election_id', '=', election.id),
        ('checked', '=', False),
        ])
        if absent_ballots:
            absent_ballots.unlink()

        election.state = 'finished'

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'vote_management.election_result',
            'view_mode': 'form',
            'res_id': election_result.id,
            'target': 'current',
        }