from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError, ValidationError


class VendorAdjustmentRequest(models.Model):
    _name = 'vendor.adjustment.request'
    _description = 'Order Adjustment Request'
    _inherit = ['mail.thread']

    name = fields.Char(string="Reference", default="New", readonly=True)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', required=True)
    adjustment_detail = fields.Text(string='Adjustment Details')
    comment = fields.Text(string='Comments')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('cancel', 'Canceled'),
    ], string="State", default='draft', track_visibility='onchange', copy=False, )

    @api.model
    def create(self, values):
        '''Sequencing the records while creation'''
        values['name'] = self.env['ir.sequence'].get('vendor.adjustment.request.seq') or ' '
        res = super(VendorAdjustmentRequest, self).create(values)
        return res

    def send_submission_email(self):
        """ Open a window to compose an email, with the default template 'email_vendor_adjust_submission and
            message loaded to send Sale Order Adjustment Submission mail
        """
        self.ensure_one()
        default_template = self.env.ref('vendor_self_service_portal.email_vendor_adjust_submission')
        ctx = dict(
            default_model='vendor.adjustment.request',
            default_res_id=self.id,
            default_use_template=bool(default_template),
            default_template_id=default_template and default_template.id,
            default_composition_mode='comment',
            default_email_layout_xmlid='mail.mail_notification_light',
            force_email=True,
        )
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def cancel_request(self):
        self.state = 'cancel'
        return


class InheritMailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def _action_send_mail(self, auto_commit=False):
        '''validating for recepients as procurement team members and submit form after the mail is sent'''
        if self.model == 'vendor.adjustment.request':
            if not self.partner_ids:
                raise ValidationError(_('Please provide mail recepients!'))
        adj_record = self.env[self.model].browse(self.res_id).state = 'submit'
        return super(InheritMailComposeMessage, self)._action_send_mail(auto_commit=auto_commit)
