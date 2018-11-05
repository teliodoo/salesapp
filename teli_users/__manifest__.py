# -*- coding: utf-8 -*-
{
    'name': "teli_users",

    'summary': "Allows Sales Associates to set their teli API token",

    'description': """
        Extends the res.user model with a sales associate token which is needed
        for accessing the API.  This token needs to be configurable, so customers
        are connected to their sales contact.
    """,

    'author': "teli Inc.",
    'website': "http://www.teli.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Custom',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
