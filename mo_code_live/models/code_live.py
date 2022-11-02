import base64
from pytz import timezone

from odoo import models, fields, tools, Command
from odoo.tools.safe_eval import safe_eval
from odoo.tools.float_utils import float_compare


class CodeLive(models.Model):
    _name = 'code.live'
    _description = 'Code Live'

    DEFAULT_PYTHON_CODE = """Available variables:
- env: Odoo Environment on which the action is triggered
- model: Odoo Model of the record on which the action is triggered; is a void recordset
- record: record on which the action is triggered; may be void
- records: recordset of all records on which the action is triggered in multi-mode; may be void
- time, datetime, dateutil, timezone: useful Python libraries
- float_compare: Odoo function to compare floats based on specific precisions
- log: log(message, level='info'): logging function to record debug information in ir.logging table
- UserError: Warning Exception to use with raise
- Command: x2Many commands namespace"""

    # Python code
    model_id = fields.Many2one('ir.model', string="Model")
    code = fields.Text(string='Python Code',
                       help="Write Python code that the action will execute. Some variables are "
                            "available for use; help about python expression is given in the help tab.")
    result = fields.Char(string='Result', readonly=True)
    description = fields.Text(string='Description', default=DEFAULT_PYTHON_CODE, readonly=True)

    def _prepare_eval_context(self):
        """ evaluation context to pass to safe_eval """
        self.ensure_one()
        if self.model_id:
            self = self.env[self.model_id.model]
        return {
            'self': self,
            'env': self.env,
            'uid': self._uid,
            'user': self.env.user,
            'time': tools.safe_eval.time,
            'datetime': tools.safe_eval.datetime,
            'dateutil': tools.safe_eval.dateutil,
            'timezone': timezone,
            'float_compare': float_compare,
            'b64encode': base64.b64encode,
            'b64decode': base64.b64decode,
            'Command': Command,
            'result': None,
        }

    def action_execute(self):
        self.ensure_one()
        self = self.sudo()
        if self.code:
            eval_context = self._prepare_eval_context()
            code = 'result = ' + self.code
            safe_eval(code.strip(), eval_context, mode="exec", nocopy=True)
            self.result = 'result' in eval_context and eval_context['result'] or False

    def action_clear(self):
        self.ensure_one()
        self.write({
            'code': '',
            'result': '',
            'model_id': False,
        })
