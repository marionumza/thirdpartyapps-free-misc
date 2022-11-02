# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class BidEvaluation(models.Model):
    _name = 'bid.evaluation'
    _description = 'Bid/Quotation Evaluation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Title")
    requisition_id = fields.Many2one('purchase.requisition', string="Purchase Requisition")
    purchase_order_id = fields.Many2one('purchase.order', 'RFQ')
    partner_id = fields.Many2one('res.partner',  string="Vendor")
    date = fields.Date(string="Date", default = lambda self: fields.Date.today())
    evaluation_guidelines = fields.Text('Evaluation Guidelines', readonly=True)
    score_limit = fields.Integer('Highest Score')
    score_avg = fields.Float('Average Score', compute="_compute_score_avg")
    notes = fields.Text('Notes')
    checklist_item_ids = fields.One2many('bid.evaluation.checklist','bid_evaluation_id', string="Evaluation Checklist")
    question_ids = fields.One2many('bid.evaluation.question', 'bid_evaluation_id', string="Bid Evaluation Questions")
    selection_justification = fields.Text('Selection Justification')
    # bid_approver_ids = fields.Many2many('bid.panel.members', string="Panel Members")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], default='draft', string="Status", tracking=True)
    user_id = fields.Many2one('res.users', string="Evaluation By", default=lambda self: self.env.user, tracking=True)

    def cancel_evaluation(self):
        self.write({'state': 'cancel'})

    def reset_to_draft(self):
        self.write({'state': 'draft'})
            
    def approve_evaluation(self):
        # check if total of question_ids.score is greater than 0:
        total_score = sum([question.score for question in self.question_ids])
        if total_score == 0:
            raise UserError(_('Please make sure that all evaluation criteria are scored properly and try again.'))
        else:
            self.write({'state': 'done'})


    @api.depends('question_ids.score')
    def _compute_score_avg(self):
        for rec in self:
            scores = rec.question_ids.mapped('score')
            if len(scores) != 0:
                rec.score_avg = sum(scores) / len(scores)
            else:
                rec.score_avg = 0
    
    def unlink(self):
        if self.state != 'draft':
            raise UserError(
                        'You can only delete bid evaluation records that are in a draft state.'
                    )
        else:
            if self.purchase_order_id:
                self.purchase_order_id.write({
                    'has_evaluation': False,
                })
        return super(BidEvaluation, self).unlink()
    
 
class BidEvaluationQuestion(models.Model):
    _name = 'bid.evaluation.question'
    _description = 'Bid Evaluation Question'

    name = fields.Char(string="Question / Factor")
    score = fields.Integer('Score')
    remarks = fields.Text('Remarks')
    bid_evaluation_id = fields.Many2one('bid.evaluation', string="Bid Evaluation")

    
    @api.constrains('score')
    def _check_max_score(self):
        if self.bid_evaluation_id.score_limit:
            if self.score > self.bid_evaluation_id.score_limit:
                raise ValidationError(
                    _(f"The maximum score limit you can provide on each question/factor is {self.bid_evaluation_id.score_limit}."))

class BidEvaluationChecklist(models.Model):
    _name = 'bid.evaluation.checklist'
    _description = 'Bid Evaluation Checklist'

    name = fields.Char(string="Item")
    item_clear = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
        ], string="Available", required=True)
    bid_evaluation_id = fields.Many2one('bid.evaluation', string="Bid Evaluation")

 