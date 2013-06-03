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

class conciliationBankreportWizard(osv.osv_memory):

    _inherit = "account.report.wiz"
    _name = "conciliation.bank.report.wiz"
    _description = "Conciliation Bank Report Wizard"
    
    _columns = {
        'bank_balance': fields.float('Bank Balance'),
        'account_ids':fields.many2one('account.account', 'Bank Account', domain="[('user_type.code','=','BKVI')]", help="Bank Account"),
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