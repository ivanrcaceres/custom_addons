# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api

from odoo.exceptions import ValidationError


class RefundPosOrder(models.Model):
    _name = 'refund.order.pos.wizard'

    @api.multi
    def refund_action(self):
        ids = self._context['active_ids']
        data = self.env['pos.order'].browse(ids)
        for record in data:
            record.refund()
            record.action_pos_order_paid()


    # @api.multi
    # def refund_paid_action(self):
    #     ids = self._context['active_ids']
    #     data = self.env['pos.order'].browse(ids)
    #     for record in data:
    #         record.action_pos_order_paid()