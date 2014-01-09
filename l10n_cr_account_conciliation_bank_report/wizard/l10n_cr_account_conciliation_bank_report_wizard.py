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
        
        list = []
        
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
                    list.append(account.parent_id.id)
                    
        # If read method isn't call, the value for out_format "dissapear",
        # the value is preserved, but disappears from the screen (a rare bug)
        res = account_obj.read(cr, uid, list, ['name'], context)
        #Append parent_id.id and parent_id.name for account.
        return [(str(r['id']), r['name']) for r in res]        
    
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
       
    def _print_report(self, cr, uid, ids, data, context=None):
        mimetype = self.pool.get('report.mimetypes')
        report_obj = self.pool.get('ir.actions.report.xml')
        report_name = ''
      
        context = context or {}
    
        # we update form with display account value
        data = self.pre_print_report(cr, uid, ids, data, context=context)
        
        #=======================================================================
        # onchange_in_format method changes variable out_format depending of 
        # which in_format is choosed. 
        # If out_format is pdf -> call record in odt format and if it's choosed
        # ods or xls -> call record in ods format.
        # ods and xls format are editable format, because they are arranged 
        # to be changed by user and, for example, user can check and change info.    
        #=======================================================================
       
        #=======================================================================
        # If mimetype is PDF -> out_format = PDF (search odt record)
        # If mimetype is xls or ods -> search ods record. 
        # If record doesn't exist, return a error.
        #=======================================================================
        
        #=======================================================================
        # Create two differents records for each format, depends of the out_format
        # selected, choose one of this records
        #=======================================================================
        
        #1. Find out_format selected
        out_format_obj = mimetype.browse(cr, uid, [int(data['form']['out_format'])], context)[0]

        #2. Check out_format and set report_name for each format
        if out_format_obj.code == 'oo-pdf':
            report_name = 'conciliation_bank_report_webkit_odt' 
           
        elif out_format_obj.code == 'oo-xls' or out_format_obj.code == 'oo-ods': 
            report_name = 'conciliation_bank_report_webkit_ods'
        
        # If there not exist name, it's because not exist a record for this format   
        if report_name == '':
            raise osv.except_osv(_('Error !'), _('There is no template defined for the selected format. Check if aeroo report exist.'))
                
        else:
            #Search record that match with the name, and get some extra information
            report_xml_id = report_obj.search(cr, uid, [('report_name','=', report_name)],context=context)
            report_xml = report_obj.browse(cr, uid, report_xml_id, context=context)[0]
            data.update({'model': report_xml.model, 'report_type':'aeroo', 'id': report_xml.id})
            
            #Write out_format choosed in wizard
            report_xml.write({'out_format': out_format_obj.id}, context=context)
           
            return {
                'type': 'ir.actions.report.xml',
                'report_name': report_name,
                'datas': data,
                'context':context
            }
        