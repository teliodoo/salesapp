# -*- coding: utf-8 -*-
{
    'name': "teli_crm",

    'summary': "Extends the Odoo CRM to trigger lead conversions",

    'description': """
        When a new lead qualifies, during the conversion process, calls shall
        be made to the teli API to create the lead's account automagically.
    """,

    'author': "teli Inc.",
    'website': "http://www.teli.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Custom',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'crm',
        'teliapi'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/crm_view.xml',
        'views/templates.xml',
        'views/teli_invoice.xml',
        # 'views/teli_invoice_aggregate.xml',
        'wizard/lead_to_opportunity.xml',
        'data/teli_crm_lead_data.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
