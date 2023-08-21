from odoo import api, fields, models, _


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    is_wholesale = fields.Boolean('Es Venta Mayorista')

    @api.onchange('type')
    def on_change_type(self):
        for record in self:
            if record.type != 'sale':
                record.is_wholesale = False


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    cashier_for_reference = fields.Char('Cajero', compute="_compute_cashier_by_reference")

    @api.depends('ref')
    def _compute_cashier_by_reference(self):
        cr = self._cr
        cont = 0
        for record in self:
            session = self.sudo().env['pos.session'].search([('name', '=', record.ref)], limit=1)
            if session:
                print(cont)
                record.cashier_for_reference = session.user_id.name
