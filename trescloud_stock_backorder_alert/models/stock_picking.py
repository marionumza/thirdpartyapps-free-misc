# -*- coding:utf-8 -*-
from odoo import api, models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    @api.depends('backorder_ids','backorder_id')
    def _compute_alert_backorder(self):
        '''
        Este método realiza el conteo de los pickings sin validar del mismo pedido de venta y dependiendo a ello se le asigna
        la alerta de seguridad de total de pickings sin validar.
        '''
        for res in self:
            delivery_not_done = 0
            backorders = res.backorder_ids
            if res.backorder_id and len(backorders) == 0:
                backorders = res.backorder_id.backorder_ids
            elif res.backorder_id and len(backorders) > 0:
                backorders += res.backorder_id.backorder_ids
            for picking in backorders:
                if picking.state != 'done':
                    delivery_not_done +=1
            if delivery_not_done > 0:
                res.alert_backorder = '%s' % (delivery_not_done)
            else:
                res.alert_backorder = False
                
    def action_view_pickings(self):
        '''
        Este metodo dispara una acción para poder revisar un tree con los pickings de los backorders,
        incluyendo el despacho origen.
        '''
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
        pickings = self.backorder_ids
        if self.backorder_id:
            pickings = self.backorder_id.backorder_ids
            pickings += self.backorder_id
        else:
            pickings += self
        action['domain'] = [('id', 'in', pickings.ids)]
        action['context'] = dict(self._context, default_partner_id=self.partner_id.id)
        return action
    
    sale_name = fields.Char(
        related = 'sale_id.name',
        string = 'Name',
        help = u'Technical field to show the name to the alert.'
    )
    alert_backorder = fields.Char(
        string = 'Alert backorder',
        help = u'Technical field to show the alert.',
        compute = '_compute_alert_backorder'
    )