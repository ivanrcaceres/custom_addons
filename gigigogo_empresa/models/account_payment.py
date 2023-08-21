from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, UserError


class payment(models.Model):
    _inherit = 'account.payment'

    numero_transaccion = fields.Char(string="Nro de Cheque")
    banco = fields.Many2one('res.bank',string='Banco')
    librador = fields.Char(string="Librador")
    payment_subtype= fields.Selection(related="journal_id.payment_subtype",readonly=True)
    tipo_cheque= fields.Selection([('deferred','Diferido'),('current','Al dia - Corriente')], string='Tipo de Cheque')
    fecha_cheque_diferido=fields.Date(string="Fecha de cobro Cheque Diferido")
    fecha_emision_cheque = fields.Date(string="Fecha de emision del Cheque")

