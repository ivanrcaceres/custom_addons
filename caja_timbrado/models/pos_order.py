from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime

class PosOrder(models.Model):

    _inherit = "pos.order"

    order_fact = fields.Char()
    # timbrado = fields.Char()

    @api.model
    def get_order_fact(self):
        return self.order_fact

    @api.model
    def create(self, vals):
        rec = super(PosOrder, self).create(vals)
        pos_config = self.env['pos.config'].browse([rec.session_id.config_id.id])
        #print(aaaa[0])
        # hacer los calculos del los numero para la factura
        suc = str(pos_config.numero_sucursal)
        caj = str(pos_config.numero_caja)
        suc = '000' + str(suc)
        caj = '000' + str(caj)
        suc = suc[-3:]
        caj = caj[-3:]
        variable_actual = pos_config.factura_para_imprimir
        pos_config.ultimo_numero_impreso = variable_actual
        num_factura = str(variable_actual)
        num_factura = '00000000' + str(num_factura)
        num_factura = num_factura[-8:]
        aux = suc + '-' + caj + '-' + num_factura
        vals['order_fact'] = aux
        #ultimo hacer eso
        pos_config.factura_para_imprimir = variable_actual + 1
        pos_config.write({'ultimo_numero_impreso': variable_actual, 'ultimo_numero_completo': aux})
        rec.write({'order_fact': aux})
        return rec