# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class LandedCost(models.Model):
    _inherit = 'stock.valuation.adjustment.lines'

    final_cost_per_unit = fields.Float(
        'Costo Final Unitario', compute='_compute_final_cost_per_unit',
        digits=0, store=True)

    @api.one
    @api.depends('quantity', 'additional_landed_cost')
    def _compute_final_cost_per_unit(self):
        self.final_cost_per_unit = self.former_cost_per_unit + (self.additional_landed_cost / (self.quantity or 1.0))
