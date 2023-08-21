from odoo import models, fields
class ResUsers(models.Model):

    _inherit = "res.users"
    
    kitchen_category_ids = fields.Many2many(comodel_name="pos.category", string="Kitchen categories")