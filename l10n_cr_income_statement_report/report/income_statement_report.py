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
from tools.translate import _
import pooler
from osv import fields,osv

from openerp.addons.account_financial_report_webkit.report.trial_balance import TrialBalanceWebkit
from openerp.addons.account_financial_report_webkit.report.webkit_parser_header_fix import HeaderFooterTextWebKitParser

def sign(number):
    return cmp(number, 0)

class IncomeStatementReport(TrialBalanceWebkit):
    def __init__(self, cr, uid, name, context):
        super(IncomeStatementReport, self).__init__(cr, uid, name, context=context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.cursor = self.cr
        #This line is to delete, the header of trial balance
        self.localcontext['additional_args'][4] = ('--header-left', '')
        self.localcontext.update({
            'cr': self.cr,
            'uid': self.uid,
            'get_accounts': self.get_accounts,
            'get_fiscalyear': self.get_fiscalyear,
            'get_last_period': self.get_last_period,
            'get_balance': self.get_balance,
        })
        
    def set_context(self, objects, data, ids, report_type=None):
        start_period = self._get_form_param('period_from', data)
        
        self.localcontext.update({
            'start_period': start_period,
            })

        return super(IncomeStatementReport, self).set_context(objects, data, ids, report_type=report_type)
    
    def get_child_ids(self, cr, uid, child_ids, childs_search):
        account_account_obj = self.pool.get('account.account')
        accounts = account_account_obj.browse(cr, uid, childs_search)
        for account in accounts:
            if account.child_id:
                new_childs = []
                for child in account.child_id:
                    new_childs.append(child.id)
                index = child_ids.index(account.id)
                cont = 1
                for child in new_childs:
                    child_ids.insert(index+cont,child)
                    cont += 1
                self.get_child_ids(cr, uid, child_ids, new_childs)
        return child_ids

    def get_expense_accounts(self, cr, uid):
        account_account_obj = self.pool.get('account.account')
        
        first_expense_account = account_account_obj.search(cr, uid, [('name', '=', 'GASTOS')])
        childs_search = first_expense_account
        expense_account_ids = self.get_child_ids(cr, uid, first_expense_account, childs_search)
        expense_accounts = account_account_obj.browse(cr, uid, expense_account_ids)
        
        return expense_accounts

    def get_asset_accounts(self, cr, uid):
        account_account_obj = self.pool.get('account.account')
        
        first_asset_account_id = account_account_obj.search(cr, uid, [('name', '=', 'ACTIVO')])
        childs_search = first_asset_account_id
        asset_account_ids = self.get_child_ids(cr, uid, first_asset_account_id, childs_search)
        asset_accounts = account_account_obj.browse(cr, uid, asset_account_ids)
        
        return asset_accounts

    def get_accounts(self, cr, uid):
         accounts = [self.get_asset_accounts(cr, uid), self.get_expense_accounts(cr, uid)]
         return accounts
    
    def get_last_period_fiscalyear(self, cr, uid, fiscalyear):
        account_period_obj = self.pool.get('account.period')
        period_ids = account_period_obj.search(cr, uid, [('fiscalyear_id', '=', fiscalyear.id), ('special', '=', False)])
        periods = account_period_obj.browse(cr, uid, period_ids)
        period_select = periods[0]
        for current_period in periods:
            if current_period.date_start > period_select.date_start:
                period_select = current_period
        return period_select
    
    def get_last_period(self, cr, uid, start_period):
        account_period_obj = self.pool.get('account.period')
        period_ids = account_period_obj.search(cr, uid, [('fiscalyear_id', '=', start_period.fiscalyear_id.id), ('special', '=', False)])
        periods = account_period_obj.browse(cr, uid, period_ids)
        period_select = start_period
        for period in periods:
            if (period.date_start < start_period.date_start and period.date_start > period_select.date_start) or (period.date_start < start_period.date_start and start_period == period_select):
                period_select = period
        if period_select == start_period:
            fiscalyear = self.get_fiscalyear(cr, uid, start_period)
            fiscalyear_select = fiscalyear
            account_fiscalyear_obj = self.pool.get('account.fiscalyear')
            all_fiscalyears_ids = account_fiscalyear_obj.search(cr, uid, [])
            all_fiscalyears = account_fiscalyear_obj.browse(cr, uid, all_fiscalyears_ids)
            for current_fiscalyear in all_fiscalyears:
                if (current_fiscalyear.date_start < fiscalyear.date_start and current_fiscalyear.date_start > fiscalyear_select.date_start) or (current_fiscalyear.date_start < fiscalyear.date_start and fiscalyear == fiscalyear_select):
                    fiscalyear_select = current_fiscalyear
            if fiscalyear_select == fiscalyear:
                raise osv.except_osv(_('Error fiscal year'),_('There is no previous period to compare'))
            period_select = self.get_last_period_fiscalyear(cr, uid, fiscalyear_select)
        return period_select
        
    def get_fiscalyear(self, cr, uid, start_period):
        fiscalyear = start_period.fiscalyear_id
        return fiscalyear
        
    def get_balance(self, cr, uid, account, filter, is_year=False):
        account_webkit_report_library_obj = self.pool.get('account.webkit.report.library')
        if is_year:
            balance = account_webkit_report_library_obj.get_account_balance(cr, uid, account, ['balance'], fiscal_year_id=filter)
        else:
            balance = account_webkit_report_library_obj.get_account_balance(cr, uid, account, ['balance'], start_period_id=filter, end_period_id=filter)
        return balance
        

HeaderFooterTextWebKitParser(
    'report.l10n_cr_income_statement_report.account.income_statement_report',
    'account.account',
    'addons/l10n_cr_income_statement_report/report/income_statement_report.mako',
    parser=IncomeStatementReport)
