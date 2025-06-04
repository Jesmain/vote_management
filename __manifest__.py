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
    'depends': ['base'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        # 'data/server_actions.xml',
        'views/election_views.xml',
        'views/district_views.xml',
        'views/voting_center_views.xml',
        'views/party_views.xml',
        'views/ballot_views.xml',
        'views/menu.xml',
    ],  
    'installable': True,
    'application': True,
}