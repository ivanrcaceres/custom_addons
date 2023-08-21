# -*- coding: utf-8 -*-
{
    'name': "ruc_cliente",

    'summary': """
        Módulo personalizador ruc_cliente""",

    'description': """
        Módulo personalizador ruc_cliente
    """,

    'author': "Odoo",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/ruc_cliente.xml',
        # 'views/template_odoo_borrar.xml',
        # 'views/template3.xml',
        # 'views/template4.xml',
        # 'reports/visit.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
