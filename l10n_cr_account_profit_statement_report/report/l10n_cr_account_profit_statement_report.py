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

import pooler
from report import report_sxw
from tools.translate import _

from openerp.addons.account_report_lib.account_report_base import accountReportbase

class profitStatementreport(accountReportbase):
    def __init__(self, cr, uid, name, context):
        super(accountReportbase, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'cr': cr,
            'uid': uid,
            'get_fiscalyear': self.get_fiscalyear,
            'get_last_period': self.get_last_period,
            'get_start_period': self.get_start_period,
            'get_data': self.get_data,
        })
              
    def get_last_period(self, cr, uid, data):
        start_period = self.get_start_period(data)
        return self.pool.get('account.period').get_last_period(cr,uid,start_period)
    
    def get_data(self, cr, uid, data, context={}):
        account_account_obj = self.pool.get('account.account')
        account_period_obj = self.pool.get('account.period')
        library_obj = self.pool.get('account.webkit.report.library')
        
        account_chart = self.get_chart_account_id(data)   
        company_id = account_chart.company_id.id
        category_account_ids = library_obj.get_category_accounts(cr, uid, company_id)
        period = self.get_start_period(data)
        
        last_period = account_period_obj.get_last_period(cr, uid, period)
        fiscal_year = self.get_fiscalyear(data)
        
        #build account_ids list
        income_account_ids = library_obj.get_account_child_ids(cr, uid, category_account_ids['income'])
        expense_account_ids = library_obj.get_account_child_ids(cr, uid, category_account_ids['expense'])
        
        #build accounts list
        income_accounts = account_account_obj.browse(cr, uid, income_account_ids)
        expense_accounts = account_account_obj.browse(cr, uid, expense_account_ids)
        
        #build balances
        income_period_balances =        library_obj.get_account_balance(cr, uid, income_account_ids,  ['balance'], start_period_id=period.id, end_period_id=period.id)
        expense_period_balances =       library_obj.get_account_balance(cr, uid, expense_account_ids, ['balance'], start_period_id=period.id, end_period_id=period.id)
        income_last_period_balances =   library_obj.get_account_balance(cr, uid, income_account_ids,  ['balance'], start_period_id=last_period.id, end_period_id=last_period.id)
        expense_last_period_balances =  library_obj.get_account_balance(cr, uid, expense_account_ids, ['balance'], start_period_id=last_period.id, end_period_id=last_period.id)
        income_fiscal_year_balances =   library_obj.get_account_balance(cr, uid, income_account_ids,  ['balance'], end_period_id=period.id, fiscal_year_id=fiscal_year.id)
        expense_fiscal_year_balances =  library_obj.get_account_balance(cr, uid, expense_account_ids, ['balance'], end_period_id=period.id, fiscal_year_id=fiscal_year.id)
        
        #build total balances
        total_income_balances = {
            'period':       income_period_balances[category_account_ids['income'].id]['balance'],
            'last_period':  income_last_period_balances[category_account_ids['income'].id]['balance'],
            'fiscal_year':  income_fiscal_year_balances[category_account_ids['income'].id]['balance'],
        }
        total_expense_balances = {
            'period':       expense_period_balances[category_account_ids['expense'].id]['balance'],
            'last_period':  expense_last_period_balances[category_account_ids['expense'].id]['balance'],
            'fiscal_year':  expense_fiscal_year_balances[category_account_ids['expense'].id]['balance'],
        }
            
        return {
            'income_accounts':              income_accounts,
            'expense_accounts':             expense_accounts,
            'income_account_ids':           income_account_ids,
            'expense_account_ids':          expense_account_ids,
            'total_income_balances':        total_income_balances,
            'total_expense_balances':       total_expense_balances,
            'income_period_balances':       income_period_balances,
            'expense_period_balances':      expense_period_balances,
            'income_last_period_balances':  income_last_period_balances,
            'expense_last_period_balances': expense_last_period_balances,
            'income_fiscal_year_balances':  income_fiscal_year_balances,
            'expense_fiscal_year_balances': expense_fiscal_year_balances,
        }
        

report_sxw.report_sxw(
    'report.l10n_cr_profit_statement_report',
    'account.account',
    'addons/l10n_cr_account_profit_statement_report/report/l10n_cr_account_profit_statement_report.mako',
    parser=profitStatementreport)
