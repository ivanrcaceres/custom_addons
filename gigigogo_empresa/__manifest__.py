# -*- coding: utf-8 -*-
{
    'name': "gigigogo_empresa",

    'summary': """
        Modulos para empresa gigi gogo
        """,

    'description': """
        Modulos para empresa gigi gogo 
    """,

    'author': "Gigi Gogo",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/res_currency_security.xml',
        # 'security/stock_security.xml',
        # 'security/ir.model.access.csv',
        # # 'views/views.xml',
        'views/templates.xml',
        # 'views/account_payment.xml',
        #
        # 'views/product_views.xml',
        # 'views/product_pricelist.xml',
        # 'views/currency_views.xml',
        # 'views/landed_cost_lines_views.xml',
        # 'views/company_view.xml',
        #
        # 'views/stock_picking.xml',
        # 'views/log_print_tag_view.xml',
        # 'views/sale_stock_view.xml',
        # 'views/account_journal.xml',
        # 'views/hidden_cost.xml',
        # 'views/purchase_views.xml',
        # 'views/stock_inventory_valuation.xml',
        # 'views/pos_order_view.xml',
        # 'wizard/generate_picking_pos_wizard.xml',
        # 'wizard/refund_selected_pos_wizard.xml',

        # 'views/stock_quant_views.xml',
    ],
    'qweb': ['static/src/xml/pos.xml'],

    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
