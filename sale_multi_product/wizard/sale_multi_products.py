from odoo import models, fields, api, _

class sale_multi_products(models.TransientModel):
    _name='sale.multi.products'
    _description = 'Sale Multi Products Wizard'

    product_ids = fields.Many2many('product.product', string='Multi Products to Sale')
    do_replace = fields.Boolean('Replace the Order lines with new selection')

    def wizard_view(self):
        view = self.env.ref('sale_multi_product.view_sale_multi_products_wizard')

        return {
            'name': _('Multi Product Selection'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.multi.products',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
        }

    def sale_multi_products(self):
        sale_order_line = self.env['sale.order.line']
        active_model = self._context.get('active_model', False)
        active_id = self._context.get('active_id', False)
        if active_model and active_id:
            active_record = self.env[active_model].browse(active_id)
            if active_record:
                if self.do_replace:
                    active_record.order_line.unlink()
                order_line_vals = []
                for prod in self.product_ids:
                    order_line = {
                        'order_id': active_record.id,
                        'product_id': prod.id,
                    }
                    new_order_line = sale_order_line.new(order_line)
                    new_order_line.product_id_change()
                    order_line = sale_order_line._convert_to_write(
                            {name: new_order_line[name] for name in new_order_line._cache})
                    order_line_vals.append((0,0,order_line))
                active_record.write({'order_line':order_line_vals})
        return True
