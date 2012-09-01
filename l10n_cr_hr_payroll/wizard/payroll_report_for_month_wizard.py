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

from osv import osv


class PayrollReportForMonthWizard(osv.osv_memory):
    
    _inherit = "trial.balance.webkit"
    _name = "payroll.report.for.month"
    _description = "Payroll Report for Month"

    _defaults = {
            'fiscalyear_id': '',
            'filter': 'filter_date',
    }
    
    def pre_print_report(self, cr, uid, ids, data, context=None):
        data = super(PayrollReportForMonthWizard, self).pre_print_report(cr, uid, ids, data, context)
        if context is None:
            context = {}
        vals = self.read(cr, uid, ids,
                         ['date_from', 'date_to',],
                         context=context)[0]
        data['form'].update(vals)
        return data
        
    def _print_report(self, cursor, uid, ids, data, context=None):
        context = context or {}
        # we update form with display account value
        data = self.pre_print_report(cursor, uid, ids, data, context=context)
        
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_cr_hr_payroll.account.payroll_report_for_month',
            'datas': data}

PayrollReportForMonthWizard()
