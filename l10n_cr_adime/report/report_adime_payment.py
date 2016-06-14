# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models
from openerp.report import report_sxw


class ReportAdimePayment(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(ReportAdimePayment, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'get_amount_currency': self._get_amount_currency,
        })

    def _get_amount_currency(self, currency_from, currency_to, amount):
        currency_obj = self.pool.get('res.currency')
        amount2 = currency_obj.compute(
            self.cr, self.uid, currency_from.id, currency_to.id, amount,
            round=True, context=None)
        return amount2


class ReportAdimePaymenWrapper(models.AbstractModel):
    _name = 'report.l10n_cr_adime.report_adime_payment'
    _inherit = 'report.abstract_report'
    _template = 'l10n_cr_adime.report_adime_payment'
    _wrapped_report_class = ReportAdimePayment
