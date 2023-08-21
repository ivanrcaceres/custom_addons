{
    'name': "Pos Kitchen Screen",
    'version': "12.0.3",
    'category': "Tools",
    'summary': "Pos Kitchen Screen",
    'author': "Javier Fernández",
    'website': "https://asdelmarketing.com",
    'license': 'OPL-1',
    'price': 16.99,
    'currency': 'EUR',
    'data': [
        'views/header_inherit_view.xml',
        'views/product_views.xml',
        'views/user_views.xml',
    ],
    'demo': [],
    'images': [
        'static/description/thumbnail.gif',
    ],
    'depends': [
        'web',
        'point_of_sale'
    ],
    'qweb' : [
        'static/src/xml/kitchen.xml',
    ],
    'installable': True,
}