{
    'name': "Vote Management",

    'summary': """
        Manage voting process and vote validation.""",

    'description': """
        This module facilitates the process of voting by keeping track of voting areas, participating parties and allowing voters to check the validity of their vote.
    """,
    'author': "Jesmain",
    'website': "https://github.com/Jesmain/vote_management",
    'category': 'Extra Tools',
    'version': '0.1',
    'depends': ['base', 'website'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/server_actions.xml',
        'data/sequences.xml',
        'reports/vote_management_report_templates.xml',
        'reports/vote_management_report_actions.xml',
        'wizards/create_election_views.xml',
        'wizards/ballot_validation_views.xml',
        'wizards/create_districts_views.xml',
        'views/election_views.xml',
        'views/district_views.xml',
        'views/voting_center_views.xml',
        'views/party_views.xml',
        'views/ballot_views.xml',
        'views/homepage_inherit.xml',
        'views/ballot_verification_template.xml',
        'views/menu.xml',
    ],  
    'installable': True,
    'application': True,
}