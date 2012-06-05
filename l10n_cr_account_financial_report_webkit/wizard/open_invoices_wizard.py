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

from osv import fields, osv


class l10n_cr_AccountReportOpenInvoicesWizard(osv.osv_memory):
    """Will launch partner ledger report and pass required args"""

    _inherit = "open.invoices.webkit"
    _name = "open.invoices.webkit"
    _description = "Open Invoices Report"


    def pre_print_report(self, cr, uid, ids, data, context=None):
        data = super(l10n_cr_AccountReportOpenInvoicesWizard, self).pre_print_report(cr, uid, ids, data, context)
        if context is None:
            context = {}
        vals = self.read(cr, uid, ids,
                         ['until_date',],
                         context=context)[0]
        data['form'].update(vals)
        return data


    def _print_report(self, cursor, uid, ids, data, context=None):
        context = context or {}
        # we update form with display account value
        data = self.pre_print_report(cursor, uid, ids, data, context=context)
        return {'type': 'ir.actions.report.xml',
                'report_name': 'account_financial_report_webkit.account.account_report_open_invoices_webkit',
                'datas': data}

