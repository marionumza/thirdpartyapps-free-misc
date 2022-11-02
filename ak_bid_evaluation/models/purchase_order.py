# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    show_eval_button = fields.Boolean(string='Allow Eval Creation', default=False, copy=False, compute="_compute_show_evaluation_button")
    has_evaluation = fields.Boolean(string='Has Evaluation', default=False, copy=False)
    evaluation_count = fields.Integer(compute="_compute_evaluations_count")

    def get_checklist_item_ids(self):
        checklist_list = []
        for item in self.requisition_id.eval_template_id.checklist_item_ids:
            checklist_list.append((0, 0, {'name': item.name, 'item_clear': 'no'}))
        return checklist_list

    def get_question_ids(self):
        questions_list = []
        for question in self.requisition_id.eval_template_id.question_ids:
            questions_list.append((0, 0, {'name': question.name}))
        return questions_list
    
    def get_bid_evaluation_record(self):
        self.ensure_one()
        bid_evaluation_record = self.env['bid.evaluation'].search([('purchase_order_id', '=', self.id)])
        if bid_evaluation_record:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Bid Evaluation',
                'view_mode': 'form',
                'res_model': 'bid.evaluation',
                'res_id': bid_evaluation_record.id,
                'domain': [('purchase_order_id', '=', self.id)],
            }
    
    def create_bid_evaluation(self):
        if not self.requisition_id.eval_template_id:
            raise UserError(_("You have not specified a a bid evaluation template on the requisition record. Please set the evaluation templateand retry."))
        
        bid_evaluation_record = self.env['bid.evaluation'].sudo().create({
            'name': f'Bid Evaluation - {self.requisition_id.name} - {self.partner_id.name}',
            'purchase_order_id': self.id,
            'requisition_id': self.requisition_id.id,
            'partner_id': self.partner_id.id,
            # user_id equals to current logged in user:
            'user_id': self.env.user.id,
            'date': fields.Date.today(),
            'evaluation_guidelines': self.requisition_id.evaluation_guidelines,
            'score_limit': self.requisition_id.eval_template_id.score_limit,
            'checklist_item_ids': self.get_checklist_item_ids(),
            'question_ids': self.get_question_ids()
          })
  
        self.write({'has_evaluation': True})
        return self.get_bid_evaluation_record()

    # update the selected bids field once an rfq is confirmed in an agreement
    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for po in self:
            if not po.requisition_id:
                continue
            if po.requisition_id.type_id.enable_evaluation:
                po.requisition_id.selected_bid_ids = [(4, po.id)]
        return res
    
    def _compute_evaluations_count(self):
        BidEvaluations = self.env['bid.evaluation']
        self.evaluation_count = BidEvaluations.search_count([('purchase_order_id', '=', self.id)])

    def _compute_show_evaluation_button(self):
        if not self.requisition_id or not self.requisition_id.type_id.enable_evaluation or self.has_evaluation:
            self.show_eval_button = False
        else:
            self.show_eval_button = True
