from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class OrderManagementItem(models.Model):
    _name = 'order.management.item'
    _description = 'Order Management Item'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)

    order_id = fields.Many2one(
        'order.management',
        string='Order',
        required=True,
        ondelete='cascade',
        index=True
    )

    product_id = fields.Many2one(
        'product.product',
        string='Product',
        domain=[('sale_ok', '=', True)]
    )

    product_name = fields.Char(
        string='Product Name',
        required=True
    )

    description = fields.Text(string='Description')

    quantity = fields.Float(
        string='Quantity',
        required=True,
        default=1.0,
        digits='Product Unit of Measure'
    )

    unit_price = fields.Float(
        string='Unit Price',
        required=True,
        default=0.0,
        digits='Product Price'
    )

    subtotal = fields.Float(
        string='Subtotal',
        compute='_compute_subtotal',
        store=True,
        digits='Product Price'
    )

    currency_id = fields.Many2one(
        'res.currency',
        related='order_id.currency_id',
        readonly=True
    )

    state = fields.Selection(
        related='order_id.state',
        string='Order Status',
        readonly=True,
        store=True
    )

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for item in self:
            item.subtotal = item.quantity * item.unit_price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_name = self.product_id.name
            self.description = self.product_id.description_sale or ''
            self.unit_price = self.product_id.list_price

    @api.constrains('quantity')
    def _check_quantity(self):
        for item in self:
            if item.quantity <= 0:
                raise ValidationError(_('Quantity must be greater than zero.'))
            if item.quantity > 100:
                raise ValidationError(_('Quantity cannot exceed 100 per item.'))

    @api.constrains('unit_price')
    def _check_unit_price(self):
        for item in self:
            if item.unit_price < 0:
                raise ValidationError(_('Unit price cannot be negative.'))