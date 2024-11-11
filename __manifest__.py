# -*- coding: utf-8 -*-
{
    'name': "Allow sale order link on invoice",

    'summary': """
        This module allows to link invoice with sale order using the invoice_origin field""",

    'description': """
        This module allows to link invoice with sale order using the invoice_origin field
    """,

    'author': "OutsourceArg",
    'website': "http://www.outsourcearg.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale','account'],

}