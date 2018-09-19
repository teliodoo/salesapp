# -*- coding: utf-8 -*-
{
    'name': "teliapi",

    'summary': "Facilitate communication with teli's API",

    'description': """
        A module built to communicate with the teli Customer API.
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
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
