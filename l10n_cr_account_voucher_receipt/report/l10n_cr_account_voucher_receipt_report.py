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

import re
from openerp.report import report_sxw
from openerp import models, _
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

class ReportMoneyReceipt(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(ReportMoneyReceipt, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_text_amount': self._get_text_amount,
        })

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
            return amount_to_text.number_to_text_es(amount,
                self._get_currency_name(currency_id,'es'), join_dec=' Y ',
                separator=',', decimal_point='.')
        elif en_regex.match(lang):
            from openerp.tools import amount_to_text_en
            return amount_to_text_en.amount_to_text(amount, lang='en',
                currency=self._get_currency_name(currency_id,'en'))
        else:
            raise Warning(_('Language not supported by this report.'))

class report_money_receipt(models.AbstractModel):
    _name = 'report.l10n_cr_account_voucher_receipt.report_money_receipt_trans'
    _inherit = 'report.abstract_report'
    _template = 'l10n_cr_account_voucher_receipt.report_money_receipt_trans'
    _wrapped_report_class = ReportMoneyReceipt
