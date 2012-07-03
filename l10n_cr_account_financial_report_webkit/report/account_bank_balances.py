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
from datetime import datetime

from openerp.addons.account_financial_report_webkit.report.trial_balance import TrialBalanceWebkit
from openerp.addons.account_financial_report_webkit.report.webkit_parser_header_fix import HeaderFooterTextWebKitParser

def sign(number):
    return cmp(number, 0)

class account_bank_balances(TrialBalanceWebkit):

    def __init__(self, cursor, uid, name, context):
        super(account_bank_balances, self).__init__(cursor, uid, name, context=context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.cursor = self.cr   
        self.localcontext.update({
        'get_bank_accounts': self.get_bank_accounts, 
        'accounts_by_currency': self.accounts_by_currency,
        'get_move_lines_account':self.get_move_lines_account,
        'get_type_move_line':self.get_type_move_line,
        'get_debit_account':self.get_debit_account,
        'get_credit_account':self.get_credit_account,
        'get_deposit_account':self.get_deposit_account,
        'get_tefs_account':self.get_tefs_account,
        'get_checks_account':self.get_checks_account,
        })

    def get_bank_accounts(self, cr, uid, objects):
        bank_accounts = []
        for account in objects:
            account_usertype_id = account.user_type.id
            account_account_type_id = self.pool.get('account.account.type').search(cr, uid, [('name', '=' ,'Banco Saldo Real')])[0]
            if account_usertype_id == account_account_type_id:
                bank_accounts.append(account)
        return bank_accounts

    def accounts_by_currency(self, cr, uid, accounts):
        currency_names_list = []
        accounts_for_currency = []
        all_accounts_by_currency = []

        for current_account in accounts:
            current_name = current_account.report_currency_id.name
            if current_name not in currency_names_list:
                currency_names_list.append(current_name)

        for current_name in currency_names_list:
            account_currency = []
            for current_account in accounts:
                if current_account.report_currency_id.name == current_name:
                    account_currency.append(current_account)
            accounts_for_currency.append(account_currency)

        i = 0
        for current_name in currency_names_list:
            tup_temp = (current_name, accounts_for_currency[i])
            all_accounts_by_currency.append(tup_temp)
            i += 1

        return all_accounts_by_currency

    def get_move_lines_account(self, cr, uid, filter_type, filter_data, account):
        if filter_type == '':
            move_lines_id = self.pool.get('account.move.line').search(cr, uid, [('account_id', '=', account.id)])
            move_lines = self.pool.get('account.move.line').browse(cr, uid, move_lines_id)
        else:
            if filter_type == 'filter_period':
                periods_ids = self.pool.get('account.period').search(cr, uid, [('date_start', '>=', filter_data[0].date_start), ('date_stop', '<=', filter_data[1].date_stop)])
                move_lines_id = self.pool.get('account.move.line').search(cr, uid, [('account_id', '=', account.id)])
                all_move_lines = self.pool.get('account.move.line').browse(cr, uid, move_lines_id)
                move_lines = []
                for move_line in all_move_lines:
                    period_id = move_line.period_id.id
                    if period_id in periods_ids:
                        move_lines.append(move_line)
            elif filter_type == 'filter_date':
                move_lines_id = self.pool.get('account.move.line').search(cr, uid, [('account_id', '=', account.id), ('date', '>=', filter_data[0]), ('date', '<=', filter_data[1])])
                move_lines = self.pool.get('account.move.line').browse(cr, uid, move_lines_id)
        

        return move_lines

    def get_type_move_line(self, cr, uid, move_line):
        voucher_line_id = self.pool.get('account.voucher.line').search(cr, uid, [('move_line_id', '=', move_line.id)])
        voucher_line = self.pool.get('account.voucher.line').browse(cr, uid, voucher_line_id)
        voucher = self.pool.get('account.voucher').browse(cr, uid, voucher_line.voucher_id)
        
        type_move_line = voucher.type
        return type_move_line

    def get_debit_account(self, cr, uid, move_lines, currency):
        debit = 0.0

        for move_line in move_lines:
            if currency == 'CRC':
                debit += move_line.debit
            elif move_line.amount_currency > 0:
                debit += move_line.amount_currency

        return debit

    def get_credit_account(self, cr, uid, move_lines, currency):
        credit = 0.0

        for move_line in move_lines:
            if currency == 'CRC':
                credit += move_line.credit
            elif move_line.amount_currency < 0:
                credit += move_line.amount_currency*-1

        return credit

    def get_deposit_account(self, cr, uid, move_lines, currency, account):
        deposit = 0.0

        all_voucher_line_id = self.pool.get('account.voucher.line').search(cr, uid, [('account_id', '=', account.id)])
        all_voucher_line = self.pool.get('account.voucher.line').browse(cr, uid, all_voucher_line_id)

        for move_line in move_lines:
            for voucher_line in all_voucher_line:
                if move_line.id == voucher_line.move_line_id:
                    if currency == 'CRC':
                        deposit += move_line.debit
                    elif move_line.amount_currency > 0:
                        deposit += move_line.amount_currency

        return deposit

    def get_tefs_account(self, cr, uid, move_lines, currency, account):
        tefs = 0.0

        all_voucher_line_id = self.pool.get('account.voucher.line').search(cr, uid, [('account_id', '=', account.id)])
        all_voucher_line = self.pool.get('account.voucher.line').browse(cr, uid, all_voucher_line_id)
        vouchers = self.pool.get('account.voucher').browse(cr, uid, all_voucher_line_id)

        journal_TEF = self.pool.get('account.journal').search(cr, uid, [('code', 'like', 'TEF')])

        for move_line in move_lines:
            for voucher_line in all_voucher_line:
                if move_line.id == voucher_line.move_line_id:
                    for voucher in vouchers:
                        if voucher.journal_id in journal_TEF:
                            if currency == 'CRC':
                                tefs += move_line.credit
                            elif move_line.amount_currency > 0:
                                tefs += move_line.amount_currency*-1

        return tefs

    def get_checks_account(self, cr, uid, move_lines, currency, account):
        checks = 0.0

        all_voucher_line_id = self.pool.get('account.voucher.line').search(cr, uid, [('account_id', '=', account.id)])
        all_voucher_line = self.pool.get('account.voucher.line').browse(cr, uid, all_voucher_line_id)
        vouchers = self.pool.get('account.voucher').browse(cr, uid, all_voucher_line_id)

        journal_CK = self.pool.get('account.journal').search(cr, uid, [('code', 'like', 'CK')])

        for move_line in move_lines:
            for voucher_line in all_voucher_line:
                if move_line.id == voucher_line.move_line_id:
                    for voucher in vouchers:
                        if voucher.journal_id in journal_CK:
                            if currency == 'CRC':
                                checks += move_line.credit
                            elif move_line.amount_currency > 0:
                                checks += move_line.amount_currency*-1

        return checks

HeaderFooterTextWebKitParser(
    'report.l10n_cr_account_financial_report_webkit.account.account_report_account_bank_balances_webkit',
    'account.account',
    'addons/l10n_cr_account_financial_report_webkit/report/account_bank_balances.mako',
    parser=account_bank_balances)
    

