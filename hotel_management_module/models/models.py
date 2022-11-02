from odoo import models, fields, api
from datetime import date, timedelta
from datetime import datetime
from odoo.exceptions import ValidationError


class hotel_management_module(models.Model):
    _name = 'hotel_management_module.users'
    _description = 'hotel_management_module.users'
    name = fields.Char(string="Name", required=True)
    phone = fields.Char(string="Contact", required=True)
    nationality = fields.Many2one('res.country', string='Nationality')
    coming_from = fields.Char(string="Coming From")
    adult_count = fields.Integer(string="Total Adults")
    children_count = fields.Integer(string="Total Childrens")
    total_count = fields.Integer(string="Total People Count", compute="_total_count", store=True)
    id_proof = fields.Binary(string='Identity upload', required=True)
    from_date = fields.Date(string="Booking from")
    to_date = fields.Date(string="To")
    number_of_rooms = fields.Integer(string="Total Rooms", compute="_number_of_rooms", store=True)
    per_day_price = fields.Integer(string="Per day price will be", compute="total_price")
    price = fields.Float(string="Price to Pay", compute="total_price", store=True)
    date_diff = fields.Integer(string="Total Days", compute="_date_difference", store=True)
    official_room_price = fields.Integer(string="Room Price", default=2000)
    room_price = fields.Integer(string="Room Price for Guest")

    status = fields.Selection([
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),

    ], string="Status", default="booked")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('done', 'Payment Completed'),
    ], required=True, default='draft')
    discount_on_room = fields.Integer(string="Discount", compute="_discount_on_room", store=True)
    description = fields.Text()

    join_id = fields.Char(string="ID", readonly=True, required=True, copy=False, default='1')

    @api.depends('status')
    def move_to_draft(self):
        for record in self:
            record.write({'state': 'draft'})
            record.write({'status': 'pending'})

    @api.depends('status')
    def booked(self):
        for record in self:
            record.write({'status': 'booked'})
            record.write({'state': 'draft'})

    @api.depends('status')
    def booking_cancelled(self):
        for record in self:
            record.write({'status': 'cancelled'})
            record.write({'state': 'cancelled'})

    @api.depends('status')
    def payment_collected(self):
        for record in self:
            record.write({'state': 'done'})
            record.write({'status': 'completed'})

    def stay_completed(self):
        for record in self:
            return {
                'name': ' Quick Edit Details ',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'hotel_management_module.users',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': self.id,
            }

    def print_pdf(self):
        # to access the recordset of particular model
        return self.env.ref('hotel_management_module.action_report_pdf').report_action(self)

    def test_function(self):
        view_id = self.env.ref('hotel_management_module.on_click_form').id
        context = self._context.copy()
        return {
            'name': 'Enter Price for the Room',
            'view_type': 'form',
            'view_mode': 'tree',
            'views': [(view_id, 'form')],
            'res_model': 'hotel_management_module.users',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new',
            'context': context,
        }

    @api.depends('from_date', 'to_date')
    def _date_difference(self):

        for record in self:
            fmt = '%Y-%m-%d'
            start_date = record.from_date
            end_date = record.to_date

            if start_date:
                if datetime.strptime(str(date.today()), fmt) == datetime.strptime(str(start_date),
                                                                                  fmt) or datetime.strptime(
                    str(date.today()), fmt) < datetime.strptime(str(start_date), fmt):
                    pass
                else:
                    raise ValidationError("Cannot book in the past!")
                pass

            if end_date:
                if datetime.strptime(str(date.today()), fmt) == datetime.strptime(str(end_date),
                                                                                  fmt) or datetime.strptime(
                    str(date.today()), fmt) < datetime.strptime(str(end_date), fmt):
                    pass
                else:
                    raise ValidationError("Cannot book in the past!")
                pass

            if start_date and end_date:
                fmt = '%Y-%m-%d'
                d1 = datetime.strptime(str(start_date), fmt)
                d2 = datetime.strptime(str(end_date), fmt)
                if d2 > d1:
                    record.date_diff = (d2 - d1).days

                else:
                    raise ValidationError('Cannot select date less than From Date')

    @api.depends('adult_count', 'children_count')
    def _total_count(self):
        for record in self:
            record.total_count = int(record.adult_count) + int(record.children_count)

    @api.depends('total_count')
    def _number_of_rooms(self):
        for record in self:
            record.number_of_rooms = 1
            total = record.total_count
            room_count = 0
            for i in range(0, total, 4):
                room_count = room_count + 1
            record.number_of_rooms = room_count

    @api.depends('number_of_rooms', 'date_diff', 'room_price', 'official_room_price')
    def total_price(self):
        for record in self:
            if record.room_price < 1:
                record.room_price = record.official_room_price

            record.per_day_price = record.room_price * record.number_of_rooms
            record.price = (record.room_price * record.number_of_rooms) * record.date_diff

    @api.depends('room_price', 'official_room_price')
    def _discount_on_room(self):
        for record in self:
            record.discount_on_room = record.official_room_price - int(record.room_price)
