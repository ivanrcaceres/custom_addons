# -*- coding: utf-8 -*-
{
'name': 'Timbrado',
'version': '1.0',
'category': 'Update',
'description': """Módulo de timbrado""",
'author': 'odoo',
'website': 'http://www.odoo.com',
'depends': ['base'],
'data': [
        # 'views/partner_view.xml',
        'views/timbrado.xml',
        'views/partner.xml',
        'views/company.xml',

        ],
'installable': True,
    'auto_install': False,
    'application': True,

}
