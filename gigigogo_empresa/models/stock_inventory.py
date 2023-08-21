from odoo import api, fields, models
from odoo.tools.float_utils import float_is_zero
from odoo.tools import float_utils


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    def action_generate_note_in_products(self):
        lines = self.line_ids
        for record in lines:
            record.generate_message_in_product(record)


class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    def _generate_moves(self):
        moves = self.env['stock.move']
        for line in self:
            diff = line.theoretical_qty - line.product_qty

            if float_utils.float_compare(line.theoretical_qty, line.product_qty,
                                         precision_rounding=line.product_id.uom_id.rounding) == 0:
                self.generate_message_in_product(line, diff)
                continue

            if diff < 0:  # found more than expected
                vals = line._get_move_values(abs(diff), line.product_id.property_stock_inventory.id,
                                             line.location_id.id, False)
            else:
                vals = line._get_move_values(abs(diff), line.location_id.id,
                                             line.product_id.property_stock_inventory.id, True)

            self.generate_message_in_product(line, diff)

            moves |= self.env['stock.move'].create(vals)
        return moves

    @staticmethod
    def generate_message_in_product(line, diff):
        # diff = line.theoretical_qty - line.product_qty
        date_format = fields.Datetime.from_string(line.inventory_id.date).date().strftime("%d/%m/%Y")
        product_template = line.product_id.product_tmpl_id

        variant = ""
        if product_template.product_variant_count > 1:
            for item in line.product_id.attribute_value_ids:
                variant = variant + "," + item.name

        if diff < 0:
            product_template.message_post(
                body=':party INV %s  <br> De: %s <br> cantidad (%s): +%s' % (
                    line.location_id.display_name, date_format, variant, -diff),
                message_type='comment', subtype='mt_note')
        elif diff > 0:
            product_template.message_post(
                body=':party INV %s <br> De: %s <br> cantidad (%s): %s' % (
                    line.location_id.display_name, date_format, variant, -diff),
                message_type='comment', subtype='mt_note')
        else:
            product_template.message_post(
                body=':party INV %s <br> De: %s <br> cantidad (%s): %s' % (
                    line.location_id.display_name, date_format, variant, diff),
                message_type='comment', subtype='mt_note')
