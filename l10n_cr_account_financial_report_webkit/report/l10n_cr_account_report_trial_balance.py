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
from report import report_sxw
from account_financial_report_webkit.report.common_reports import CommonReportHeaderWebkit
from account.report.account_balance import account_balance

class l10n_cr_account_report_trial_balance(report_sxw.rml_parse,CommonReportHeaderWebkit):

    def __init__(self, cr, uid, name, context=None):
        super(l10n_cr_account_report_trial_balance, self).__init__(cr, uid, name, context=context)
        account_balance = account_balance(cr,uid,name,context=context)
        
        self.lines = account_balance.lines
        self.localcontext.update({
            'lines': self.lines,           
        })
        self.context = context

#the parameters are the report name and module name 
report_sxw.report_sxw( 'report.account_report_trial_balance_webkit', 
                       'account.account',
                       'addons/l10n_cr_account_financial_report_webkit/report/account_report_trial_balance.mako', 
                        parser = l10n_cr_account_report_trial_balance)

