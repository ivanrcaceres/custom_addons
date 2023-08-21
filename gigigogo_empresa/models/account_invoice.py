from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def invoice_validate(self):
        for invoice in self:
            fechas = datetime.strptime(invoice.date_invoice, '%Y-%m-%d')
            fecha = datetime.strftime(fechas, "%Y/%m/%d")
            if invoice.currency_id.id != invoice.env.user.company_id.currency_id.id:
                coti = self.env['res.currency.rate'].search(
                    [['name', '=', fecha], ['currency_id', '=', invoice.currency_id.id]])
                if not coti:
                    raise ValidationError(
                        'No se encuentra cotizacion para el dia %s . Verifique que la cotizacion se encuentre cargada ' % fecha)
        self._check_duplicate_supplier_reference()
        return self.write({'state': 'open'})



