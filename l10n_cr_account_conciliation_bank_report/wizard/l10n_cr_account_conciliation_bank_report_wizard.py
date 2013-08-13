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
from openerp.tools.translate import _

class conciliationBankreportWizard(osv.osv_memory):

    _inherit = "account.report.wiz"
    _name = "conciliation.bank.report.wiz"
    _description = "Conciliation Bank Report Wizard"

    def _get_parent_accounts(self, cr, uid, context=None):
        
        if context is None:
            context = {}
                
        res = []
        account_obj = self.pool.get('account.account')

        #Search accounts that have in user_type checked include_conciliation_report attribute. Then, return a tuple list with name and id for
        #parent_id for this accounts
        #Include accounts with type == 'view'
        account_ids = account_obj.search(cr, uid, [('user_type.include_conciliation_report', '=', True)], context=context)
        
        if account_ids:
            accounts = account_obj.browse(cr, uid, account_ids, context)
            for account in accounts:   
                if account.parent_id:            
                    res.append((account.parent_id.id, account.parent_id.name)) #Append parent_id.id and parent_id.name for account.
                
        return res
    
    '''
        account_ids is define as a selection field, because with a domain can't obtain necessary data.
        account_ids are all accounts that their parents user_type have include_conciliation_report attribute mark as True.
        This configuration solves the problem of searching for a specific code in accounts and makes configurable the accounts that 
        you want in the bank reconciliation report
    '''
    _columns = {
        'bank_balance': fields.float('Bank Balance'),
        'filter': fields.selection([('filter_date', 'Date'), ('filter_period', 'Periods')], "Filter by"),
        'account_ids': fields.selection(_get_parent_accounts, 'Bank Account'),
    }
                 
    
    _defaults = {
        'filter': 'filter_period',
    }
    
    def pre_print_report(self, cr, uid, ids, data, context=None):
       
        if context is None:
            context = {}
            
        # read the bank_banlance, because this field don't belongs to the account.report.wiz
        # this field is added by conciliation.bank.report.wiz and add to data['form']                
        vals = self.read(cr, uid, ids,['bank_balance'], context=context)[0] #this method read the field and included it in the form (account.common.report has this method)
        
        data['form'].update(vals)
        
        return data
       
    def _print_report(self, cursor, uid, ids, data, context=None):

        context = context or {}
        # we update form with display account value
        
        data = self.pre_print_report(cursor, uid, ids, data, context=context)

        return {
                'type': 'ir.actions.report.xml',
                'report_name': 'conciliation_bank_report_webkit',
                'datas': data
                }