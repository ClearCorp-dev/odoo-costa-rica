# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AdimeAssigned(models.Model):

    _name = 'l10n.cr.adime.percentage'

    name = fields.Char('Name', size=64, required=True)
    percentage = fields.Float('Percentage', required=True)

    @api.multi
    def name_get(self):
        result = []
        for adime in self:
            result.append(
                (adime.id, '%s (%.2f%%)' % (adime.name, adime.percentage)))
        return result


"""class AdimeReport(osv.osv):

    _name = 'adime.report'

    def action_set_adime_state(self, cr, uid, ids, context=None):
        for report in self.browse(cr, uid, ids):
            for inv in report.invoice_adime:
                inv.write({'paid_adime': True})
        self.write(cr, uid, ids, {'state': 'done'}, context=context)
        return True

    _columns = {
        'name': fields.char('Nombre', size=64, readonly=True),
        'start': fields.date('Fecha Inicio', required=True),
        'end': fields.date('Fecha Fin', required=True),
        'total': fields.float('Total', readonly=True),
        'create_date': fields.datetime('Fecha Creacion', readonly=True),
        'state': fields.selection(
            [('draft', 'Borrador'), ('confirmed', 'Confirmado'),
             ('done', 'Procesado'), ('cancel', 'Cancelado')], 'Estado',
            required=True, readonly=True),
        'invoice_adime': fields.many2many(
            'account.invoice', 'adime_invoice', 'adime_report_id',
            'invoice_id', 'Facturas Adime'),
        'adime_line': fields.many2many(
            'adime.report.line', 'adime_line', 'adime_report_id',
            'line_id', 'Facturas Pagadas', readonly=True),
        'partner_assigned': fields.many2many(
            'adime.partner.line', 'adime_partner', 'adime_report_id',
            'partner_id', 'Analisis Socio', readonly=True),
    }

    def create(self, cr, uid, vals, context=None):
        adime_partner_list = []
        adime_line_list = []
        line_count = 0
        adime_total = 0
        invoice_obj = self.pool.get('account.invoice')
        line_obj = self.pool.get('adime.report.line')
        vals['name'] = self.pool.get(
            'ir.sequence').get(cr, uid, 'adime.report')

        inv_list = invoice_obj.search(
            cr, uid, [('date_invoice', '<=', vals['end']),
                      ('date_invoice', '>=', vals['start']),
                      ('state', '=', 'paid'),
                      ('type', '=', 'out_invoice'),
                      ('paid_ontime', '=', True),
                      ('is_adime', '=', True)], context=context)

        for invoice in self.pool.get('account.invoice').browse(
                cr, uid, inv_list, context=context):

            adime_total += invoice.adime_total
            adime_line_list.append(line_obj.create(cr, uid, {
                'name': vals['name'] + '-'+str(line_count),
                'inv_number': invoice.number,
                'inv_date': invoice.date_invoice,
                'subtotal': invoice.amount_untaxed,
                'adime_subtotal': invoice.adime_total,
                'date_due': invoice.date_due,
                'partner_id': invoice.partner_id.id,
                'currency_id': invoice.currency_id.id,
                'invoice_id': invoice.id,
            }, context=context))

            if invoice.partner_id.id in adime_partner_list:
                partner_total = adime_partner_list.pop(invoice.partner_id.id)
                adime_partner_list.insert(
                    invoice.partner_id.id, [
                        invoice.partner_id.id,
                        invoice.adime_total + partner_total[1]
                    ])
            else:
                adime_partner_list.insert(
                    invoice.partner_id.id, [
                        invoice.partner_id.id,
                        invoice.adime_total
                    ])

        vals['total'] = adime_total
        vals['invoice_adime'] = [[6, 0, inv_list]]
        vals['adime_line'] = [[6, 0, adime_line_list]]
        res = super(AdimeReport, self).create(cr, uid, vals, context=context)
        return res

    _defaults = {
        'state': lambda *args: 'draft',
    }


class AdimeReportLine(osv.osv):

    _name = 'adime.report.line'

    _columns = {
        'name': fields.char('Nombre', size=64, readonly=True),
        'inv_number': fields.char('Factura', size=64, readonly=True),
        'inv_date': fields.date('Fecha Factura'),
        'subtotal': fields.float('Subtotal', required=True),
        'adime_subtotal': fields.float('Aporte Adime', required=True),
        'date_paid': fields.date('Fecha Pago'),
        'date_due': fields.date('Fecha Vencimiento', required=True),
        'partner_id': fields.many2one('res.partner', 'Socio', required=True),
        'currency_id': fields.many2one(
            'res.currency', 'Divisa', required=True),
        'invoice_id': fields.many2one(
            'account.invoice', 'Factura', required=True),
        'inv_state': fields.related(
            'invoice_id', 'state', type='selection', selection=STATES,
            string='Estado', store=False, readonly=True),
    }


class adime_partner_line(osv.osv):
    _name = 'adime.partner.line'
    _columns = {
        'name': fields.char('Nombre', size=64, readonly=True),
        'partner_id': fields.many2one('res.partner', 'Socio', required=True),
        'subtotal': fields.float('Subtotal', required=True),
    }"""
