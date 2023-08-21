from odoo.addons.sale.controllers.product_configurator import ProductConfiguratorController


from odoo import models, fields, api

class WebsiteSale(ProductConfiguratorController):
    _inherit = 'website.WebsiteSale'

    def _get_mandatory_billing_fields(self):
        print("hola")
        return ["name", "email", "street","vat", "city", "country_id"]