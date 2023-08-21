from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime

class PosOrder(models.Model):

    _inherit = "pos.order"
    
    start_date = fields.Datetime(string="Start date")
    end_date = fields.Datetime(string="End date")
    kitchen_state = fields.Char(compute="compute_kitchen_state", store=True, default="pending")
    order_fact = fields.Char()

    @api.model
    def get_order_fact(self):
        return self.order_fact

    @api.depends('lines.kitchen_state')
    def compute_kitchen_state(self):
        print('holaaaaa mumumundooooo')
        print(self[0].company_id)
        self.calcularTimbrado(self[0].company_id.id)
        for order in self:
            order.kitchen_state = 'pending'
            if len(order.lines.filtered(lambda r: r.kitchen_state == 'in_progress')) > 0:
                order.kitchen_state = 'in_progress'
            if len(order.lines.filtered(lambda r: r.kitchen_state == 'done')) == len(order.lines):
                order.kitchen_state = 'done'

    def calcularTimbrado(self, a):
        company1 = self.env['res.company'].browse([a])
        company = self.env['res.company'].browse([a])
        print(company)
        variable_actual = company.ultimo_numero_impreso
        company.ultimo_numero_impreso = company.ultimo_numero_impreso + 1

        ult_imp = str(company.ultimo_numero_impreso)
        suc = str(company.numero_sucursal)
        caj = str(company.numero_caja)

        # ult_imp = '00000000' + ult_imp
        ult_imp = '00000000' + str(variable_actual)
        suc = '000'+str(suc)
        caj = '000'+str(caj)

        ult_imp = ult_imp[-8:]
        suc = suc[-3:]
        caj = caj[-3:]

        print(ult_imp)
        print(suc)
        print(caj)
        company.ultimo_numero_completo = suc + '-' + caj + '-' + ult_imp
        print(company.ultimo_numero_completo)
        company.write({'ultimo_numero_impreso': company.ultimo_numero_impreso, 'ultimo_numero_completo': company.ultimo_numero_completo})

    @api.model
    def create(self, vals):
        company = self.env['res.company'].browse([1])
        variable_actual = company.ultimo_numero_impreso - 1


        ult_imp = str(company.ultimo_numero_impreso)
        suc = str(company.numero_sucursal)
        caj = str(company.numero_caja)

        # ult_imp = '00000000' + ult_imp
        ult_imp = '00000000' + str(variable_actual)
        suc = '000'+str(suc)
        caj = '000'+str(caj)

        ult_imp = ult_imp[-8:]
        suc = suc[-3:]
        caj = caj[-3:]
        # self.order_fact = suc + '-' + caj + '-' + ult_imp
        vals['order_fact'] = suc + '-' + caj + '-' + ult_imp
        rec = super(PosOrder, self).create(vals)
        return rec


class PosOrderLine(models.Model):

    _inherit = "pos.order.line"
    
    start_date = fields.Datetime(string="Start date")
    end_date = fields.Datetime(string="End date")
    avg_completion_time = fields.Integer(related="product_id.avg_completion_time", string="Avg completion time")
    completion_time = fields.Integer(string="Completion time", compute="compute_kitchen_state", store=True)
    kitchen_state = fields.Selection(compute="compute_kitchen_state", store=True, selection=[('pending', 'Pending'), ('in_progress', 'In progres'), ('done', 'Done')], default="pending")

    @api.depends('start_date', 'end_date')
    def compute_kitchen_state(self):
        for line in self:
            line.kitchen_state = 'pending'
            if line.start_date:
                line.kitchen_state = 'in_progress'
            if line.end_date:
                line.kitchen_state = 'done'
            if line.start_date and line.end_date:
                time_delta = (line.end_date - line.start_date)
                total_seconds = time_delta.total_seconds()
                line.completion_time = total_seconds/60

    def write(self, values):
        print('holaaaaa muuuuunndoooo 1')
        result = super(PosOrderLine, self).write(values)
        if 'end_date' in values:
            for line in self:
                self.env.cr.execute('SELECT AVG(completion_time) FROM pos_order_line WHERE completion_time != 0 and product_id = %s' %(line.product_id.id))
                result = self._cr.fetchone()
                line.product_id.write({'avg_completion_time': result[0]})