from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class OrderManagement(models.Model):
    _name = 'order.management'
    _description = 'Order Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'order_date desc, id desc'

    name = fields.Char(
        string='Order Reference',
        required=True,
        copy=False,
        readonly=True,
        default='New',
        tracking=True
    )

    customer_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        tracking=True,
    )

    order_date = fields.Datetime(
        string='Order Date',
        required=True,
        default=fields.Datetime.now,
        tracking=True
    )

    item_ids = fields.One2many(
        'order.management.item',
        'order_id',
        string='Order Items',
        copy=True
    )

    total_amount = fields.Float(
        string='Total Amount',
        compute='_compute_total_amount',
        store=True,
        tracking=True
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('preparing', 'Preparing'),
        ('packing', 'Packing'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', required=True, tracking=True)

    user_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user,
        tracking=True
    )

    notes = fields.Text(string='Notes')

    item_count = fields.Integer(
        string='Item Count',
        compute='_compute_item_count'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='company_id.currency_id',
        readonly=True
    )

    @api.depends('item_ids.subtotal')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = sum(order.item_ids.mapped('subtotal'))

    @api.depends('item_ids')
    def _compute_item_count(self):
        for order in self:
            order.item_count = len(order.item_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('order.management') or 'New'
        return super().create(vals_list)

    @api.constrains('item_ids')
    def _check_order_items(self):
        for order in self:
            if order.state not in ['draft', 'cancelled'] and not order.item_ids:
                raise ValidationError(_('Order must have at least one item before moving to preparing state.'))

    @api.constrains('total_amount')
    def _check_total_amount(self):
        for order in self:
            if order.state not in ['draft', 'cancelled'] and order.total_amount <= 0:
                raise ValidationError(_('Order total amount must be greater than zero.'))

    def action_confirm(self):
        if not self.item_ids:
            raise UserError(_('Cannot move to preparing without items.'))
        self.write({'state': 'preparing'})
        self.message_post(body=_('Order moved to preparing'))
        return True

    def action_process(self):
        if self.state != 'preparing':
            raise UserError(_('Only preparing orders can be moved to packing.'))
        self.write({'state': 'packing'})
        self.message_post(body=_('Order is being packed'))
        return True

    def action_done(self):
        if self.state != 'packing':
            raise UserError(_('Only packing orders can be marked as ready.'))
        self.write({'state': 'ready'})
        self.message_post(body=_('Order is ready'))
        return True

    def action_deliver(self):
        if self.state != 'ready':
            raise UserError(_('Only ready orders can be delivered.'))
        self.write({'state': 'delivered'})
        self.message_post(body=_('Order delivered'))
        return True

    def action_cancel(self):
        if self.state in ['ready', 'delivered']:
            raise UserError(_('Cannot cancel ready or delivered orders.'))
        self.write({'state': 'cancelled'})
        self.message_post(body=_('Order cancelled'))
        return True

    def action_draft(self):
        if self.state in ['ready', 'delivered']:
            raise UserError(_('Cannot reset ready or delivered orders to draft.'))
        self.write({'state': 'draft'})
        self.message_post(body=_('Order reset to draft'))
        return True

    def unlink(self):
        for order in self:
            if order.state in ['ready', 'delivered']:
                raise UserError(_('You cannot delete orders that are ready or delivered.'))
        return super().unlink()
