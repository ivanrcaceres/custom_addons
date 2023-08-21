# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api
from datetime import datetime, timedelta
from lxml import etree
from odoo.exceptions import ValidationError


class BarcodeWizard(models.Model):
    _name = 'generate.picking.pos.wizard'

    @api.multi
    def generate_picking_action(self):
        ids = self._context['active_ids']
        data = self.env['pos.order'].browse(ids)
        for record in data:
            record.create_picking()
