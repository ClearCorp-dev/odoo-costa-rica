# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Addons modules by CLEARCORP S.A.
#    Copyright (C) 2009-TODAY CLEARCORP S.A. (<http://clearcorp.co.cr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields
from openerp.report import report_sxw
from datetime import datetime, timedelta
import re
from openerp.exceptions import Warning

CURRENCY_NAMES = {
    'USD': {
        'en': 'Dollars',
        'es': 'DOLARES',
    },
    'EUR': {
        'en': 'Euros',
        'es': 'EUROS',
    },
    'CRC': {
        'en': 'Colones',
        'es': 'COLONES',
    }
}


class ReportSalaryCertificate(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(ReportSalaryCertificate, self).__init__(cr, uid, name,
                                                      context=context)
        self.localcontext.update(
            {
                'get_valid_contract': self._get_valid_contract,
                'get_currency_name': self._get_currency_name,
                'get_text_amount': self._get_text_amount,
                'get_payslip_employee': self._get_payslip_employee,
                'get_line_total': self._get_line_total,
                'get_line_total_group': self._get_line_total_group,
                'validate_contract': self._validate_contract,
                'context': context,
            })

    def _get_valid_contract(self, employee_id):
        contract_obj = self.pool.get('hr.contract')
        contract_id = contract_obj.search(
            self.cr, self.uid, [('employee_id', '=', employee_id),
                                ('date_start', '<=', fields.Date.today()), '|',
                                ('date_end', '>=', fields.Date.today()),
                                ('date_end', '=', False)], limit=1)
        contract = contract_obj.browse(self.cr, self.uid, contract_id)
        return contract

    def _validate_contract(self, contract):
        date = datetime.now() - timedelta(days=90)
        if not contract:
            return False
        if datetime.strptime(contract.date_start, '%Y-%m-%d') <= date:
            return True
        return False

    def _get_payslip_employee(self, employee_id, contract_id):
        payslip_obj = self.pool.get('hr.payslip')
        date = datetime.now() - timedelta(days=90)
        date_str = datetime.strftime(date, '%Y-%m-%d')
        payslip_ids = payslip_obj.search(
            self.cr, self.uid, [('date_from', '>=', date_str),
                                ('date_to', '<=', fields.Date.today()),
                                ('employee_id', '=', employee_id),
                                ('contract_id', '=', contract_id),
                                ('state', '=', 'done')])
        payslips = payslip_obj.browse(self.cr, self.uid, payslip_ids)
        res = {
            'payslips': payslips,
            'quantity': len(payslips),
            }
        return res

    def _get_line_total(self, payslips, code='BASE'):
        total = 0.00
        for payslip in payslips:
            for line in payslip.line_ids:
                if line.code == code:
                    if payslip.credit_note:
                        total -= line.total
                    else:
                        total += line.total
        return total

    def _get_line_total_group(self, payslips, code=['EXT', 'EXT-FE', 'FE']):
        total = 0.00
        for payslip in payslips:
            for line in payslip.line_ids:
                if line.code in code:
                    if payslip.credit_note:
                        total -= line.total
                    else:
                        total += line.total
        return total

    def _get_currency_name(self, currency_id, lang):
        currency_obj = self.pool.get('res.currency')
        currency = currency_obj.browse(self.cr, self.uid, currency_id)
        if currency.name in CURRENCY_NAMES:
            return CURRENCY_NAMES[currency.name][lang]
        raise Warning(_('Currency not supported by this report.'))

    def _get_text_amount(self, amount, currency_id, lang):
        es_regex = re.compile('es.*')
        en_regex = re.compile('en.*')
        if es_regex.match(lang):
            from openerp.addons.l10n_cr_amount_to_text import amount_to_text
            return amount_to_text.number_to_text_es(
                amount, self._get_currency_name(currency_id, 'es'),
                join_dec=' Y ', separator=',', decimal_point='.')
        elif en_regex.match(lang):
            from openerp.tools import amount_to_text_en
            return amount_to_text_en.amount_to_text(
                amount, lang='en', currency=self._get_currency_name(
                    currency_id, 'en'))


class report_salary_certificate(models.AbstractModel):
    _name = 'report.l10n_cr_hr_payroll_salary_certificate.report_salary_certificate'
    _inherit = 'report.abstract_report'
    _template = 'l10n_cr_hr_payroll_salary_certificate.report_salary_certificate'
    _wrapped_report_class = ReportSalaryCertificate
