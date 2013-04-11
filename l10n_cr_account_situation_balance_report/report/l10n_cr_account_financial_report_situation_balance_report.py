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

class situationBalancereport(accountReportbase):
    
    def __init__(self, cr, uid, name, context):      
        super(situationBalancereport, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'cr': cr,
            'uid':uid,
            'get_fiscalyear': self.get_fiscalyear,
            'get_start_period': self.get_start_period,
            'get_data': self.get_data,
        })
       
    def get_data(self, cr, uid, data, context={}):
        account_account_obj = self.pool.get('account.account')
        account_period_obj = self.pool.get('account.period')
        library_obj = self.pool.get('account.webkit.report.library')
        
        account_chart = self.get_chart_account_id(data)        
        company_id = account_chart.company_id.id
        category_account_ids = library_obj.get_category_accounts(cr, uid, company_id)
        period = self.get_start_period(data)
        fiscal_year = self.get_fiscalyear(data)
        opening_period = account_period_obj.get_opening_period(cr, uid, period)
        
        #build account_ids list
        asset_account_ids = library_obj.get_account_child_ids(cr, uid, category_account_ids['asset'])
        liability_account_ids = library_obj.get_account_child_ids(cr, uid, category_account_ids['liability'])
        equity_account_ids = library_obj.get_account_child_ids(cr, uid, category_account_ids['equity'])
        income_account_id = category_account_ids['income'].id
        expense_account_id = category_account_ids['expense'].id
        
        #build accounts list
        asset_accounts = account_account_obj.browse(cr, uid, asset_account_ids)
        liability_accounts = account_account_obj.browse(cr, uid, liability_account_ids)
        equity_accounts = account_account_obj.browse(cr, uid, equity_account_ids)
        income_account = category_account_ids['income']
        expense_account = category_account_ids['expense']
        
        #build balances
        asset_period_balances =     library_obj.get_account_balance(cr, uid, asset_account_ids,  ['balance'], end_period_id=period.id, fiscal_year_id=fiscal_year.id)
        liability_period_balances = library_obj.get_account_balance(cr, uid, liability_account_ids, ['balance'], end_period_id=period.id, fiscal_year_id=fiscal_year.id)
        equity_period_balances =    library_obj.get_account_balance(cr, uid, equity_account_ids, ['balance'], end_period_id=period.id, fiscal_year_id=fiscal_year.id)
        income_period_balance =     library_obj.get_account_balance(cr, uid, [income_account_id],  ['balance'], end_period_id=period.id, fiscal_year_id=fiscal_year.id)
        expense_period_balance =    library_obj.get_account_balance(cr, uid, [expense_account_id], ['balance'], end_period_id=period.id, fiscal_year_id=fiscal_year.id)
        
        asset_fiscal_year_balances =     library_obj.get_account_balance(cr, uid, asset_account_ids,  ['balance'], start_period_id=opening_period.id, end_period_id=opening_period.id)
        liability_fiscal_year_balances = library_obj.get_account_balance(cr, uid, liability_account_ids, ['balance'], start_period_id=opening_period.id, end_period_id=opening_period.id)
        equity_fiscal_year_balances =    library_obj.get_account_balance(cr, uid, equity_account_ids, ['balance'], start_period_id=opening_period.id, end_period_id=opening_period.id)
        income_fiscal_year_balance =     library_obj.get_account_balance(cr, uid, [income_account_id],  ['balance'], start_period_id=opening_period.id, end_period_id=opening_period.id)
        expense_fiscal_year_balance =    library_obj.get_account_balance(cr, uid, [expense_account_id], ['balance'], start_period_id=opening_period.id, end_period_id=opening_period.id)
      
        
        
        #build total balances
        total_asset_balances = {
            'period':       asset_period_balances[category_account_ids['asset'].id]['balance'],
            'fiscal_year':  asset_fiscal_year_balances[category_account_ids['asset'].id]['balance'],
        }
        
        total_liability_balances = {
            'period':       liability_period_balances[category_account_ids['liability'].id]['balance'],
            'fiscal_year':  liability_fiscal_year_balances[category_account_ids['liability'].id]['balance'],
        }
        
        total_equity_balances = {
            'period':       equity_period_balances[category_account_ids['equity'].id]['balance'],
            'fiscal_year':  equity_fiscal_year_balances[category_account_ids['equity'].id]['balance'],
        }
        
        total_income_balance = {
            'period':       income_period_balance[category_account_ids['income'].id]['balance'],
            'fiscal_year':  income_fiscal_year_balance[category_account_ids['income'].id]['balance'],
        }
        total_expense_balance = {
            'period':       expense_period_balance[category_account_ids['expense'].id]['balance'],
            'fiscal_year':  expense_fiscal_year_balance[category_account_ids['expense'].id]['balance'],
        }

        return {
            'asset_accounts':                   asset_accounts,
            'liability_accounts':               liability_accounts,
            'equity_accounts':                  equity_accounts,
            'income_account':                   income_account,
            'expense_account':                  expense_account,
            'asset_accounts_ids':               asset_account_ids,
            'liability_account_ids':            liability_account_ids,
            'equity_account_ids':               equity_account_ids,
            'income_account_id':                income_account_id,
            'expense_account_id':               expense_account_id,
            'total_asset_balances':             total_asset_balances,
            'total_liability_balances':         total_liability_balances,
            'total_equity_balances':            total_equity_balances,
            'total_income_balance':             total_income_balance,
            'total_expense_balance':            total_expense_balance,
            'asset_period_balances':            asset_period_balances,
            'liability_period_balances':        liability_period_balances,
            'equity_period_balances':           equity_period_balances,
            'asset_fiscal_year_balances':       asset_fiscal_year_balances,
            'liability_fiscal_year_balances':   liability_fiscal_year_balances,
            'equity_fiscal_year_balances':      equity_fiscal_year_balances,
        }

report_sxw.report_sxw(
    'report.l10n_cr_situation_balance_report',
    'account.account',
    'addons/l10n_cr_account_situation_balance_report/report/l10n_cr_account_financial_report_situation_balance_report.mako',
    parser=situationBalancereport)
