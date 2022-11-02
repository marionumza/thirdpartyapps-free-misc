# Copyright 2018, 2021 Heliconia Solutions Pvt Ltd (https://heliconia.io)

import calendar
import datetime

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class ResPartner(models.Model):
    """Partner with birth date in date format."""

    _inherit = "res.partner"

    birthdate_date = fields.Date("Birthdate", store=True)
    birth_year = fields.Integer("Birth Year", default=0)
    birth_month = fields.Char("Birth Month", default="No Birthdate")
    left_days = fields.Integer("Left Day's")
    month_filter = fields.Boolean("Is Current Month", default=False)
    day = fields.Char("Day", default=0)
    age = fields.Integer(string="Age", readonly=True, compute="_compute_age")

    @api.depends("birthdate_date")
    def _compute_age(self):
        for record in self:
            age = 0
            if record.birthdate_date:
                birth = record.birthdate_date
                today = datetime.date.today()
                if today.month == birth.month:
                    record.month_filter = True
                if (
                    today.month == birth.month
                    and today.day >= birth.day
                    or today.month > birth.month
                ):
                    next_birthday_year = today.year + 1
                else:
                    next_birthday_year = today.year

                next_birthday = datetime.date(
                    next_birthday_year, birth.month, birth.day
                )
                diff = next_birthday - today
                record.left_days = diff.days
                record.birth_year = birth.year
                record.day = birth.day
                record.birth_month = calendar.month_name[birth.month]
                age = relativedelta(fields.Date.today(), record.birthdate_date).years
            record.age = age
