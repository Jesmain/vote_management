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
        # 'security/ir.model.access.csv',
        'views/res_config_settings_view.xml',
    ],
    'installable': True,
    'application': True,
}