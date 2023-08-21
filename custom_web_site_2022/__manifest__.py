# -*- coding: utf-8 -*-
{
    'name': "custom_web_site_2022",

    'summary': """
        Módulo personalizador de sitio web odoo""",

    'description': """
        Módulo personalizador de sitio web odoo..
    """,

    'author': "Curso Odoo",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views_ruc.xml',
        # 'views/template_odoo_borrar.xml',
        # 'views/template2.xml',
        # 'views/template3.xml',
        # 'reports/visit.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
