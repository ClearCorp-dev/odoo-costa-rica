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

import time

from osv import fields, osv

class l10n_cr_ConciliationBankWizard(osv.osv_memory):

    _inherit = "partners.ledger.webkit"
    _name = "conciliation.bank.webkit"
    _description = "Conciliation Bank Report"
    
    _columns = {
        'bank_account_ids': fields.many2one('account.account', 'Bank Account', domain="[('user_type.code','=','BKVI')]", help="Bank Account"),
        'bank_balance': fields.float('Bank Balance'),
        'filter': fields.selection([('filter_date', 'Date'), ('filter_period', 'Periods')], "Filter by", required=True),
    }
    
    _defaults = {
        'filter': 'filter_period',
    }
    
    def pre_print_report(self, cr, uid, ids, data, context=None):
        data = super(l10n_cr_ConciliationBankWizard, self).pre_print_report(cr, uid, ids, data, context)
        if context is None:
            context = {}
        # will be used to attach the report on the main account
        data['ids'] = [data['form']['chart_account_id']]
        vals = self.read(cr, uid, ids,
                         ['bank_account_ids', 'bank_balance',],
                         context=context)[0]
        data['form'].update(vals)
        return data

    def _print_report(self, cursor, uid, ids, data, context=None):
        context = context or {}
        # we update form with display account value
        data = self.pre_print_report(cursor, uid, ids, data, context=context)
        return {'type': 'ir.actions.report.xml',
                'report_name': 'account_financial_report_webkit.account.account_report_conciliation_bank_webkit',
                'datas': data}