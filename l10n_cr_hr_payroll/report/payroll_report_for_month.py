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

class payroll_report_for_month(TrialBalanceWebkit):
    def __init__(self, cr, uid, name, context):
        super(payroll_report_for_month, self).__init__(cr, uid, name, context=context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.cursor = self.cr
        #This line is to delete, the header of trial balance
        self.localcontext['additional_args'][4] = ('--header-left', '')
        self.localcontext.update({
            'get_payslips_by_date': self.get_payslips_by_date,
            'get_payslips_by_struct': self.get_payslips_by_struct,
            'get_payslips_by_employee': self.get_payslips_by_employee,
            'get_identification': self.get_identification,
            'get_bank_account': self.get_bank_account,
            'get_hn': self.get_hn,
            'get_he': self.get_he,
            'get_basic': self.get_basic,
            'get_exs': self.get_exs,
            'get_gross': self.get_gross,
            'get_ccss': self.get_ccss,
            'get_rent': self.get_rent,
            'get_net': self.get_net,
        })
        
    def set_context(self, objects, data, ids, report_type=None):
        start_date = self._get_form_param('date_from', data)
        end_date = self._get_form_param('date_to', data)
        
        self.localcontext.update({
            'start_date': start_date,
            'end_date': end_date,
            })

        return super(payroll_report_for_month, self).set_context(objects, data, ids, report_type=report_type)
    
    def get_payslips_by_date(self, cr, uid, start_date, end_date):
        payslips_ids = self.pool.get('hr.payslip').search(cr, uid, [('date_from', '>=' , start_date), ('date_to', '<=' , end_date)])
        payslips = self.pool.get('hr.payslip').browse(cr, uid, payslips_ids)
        return payslips
        
    def get_payslips_by_struct(self, cr, uid, start_date, end_date):
        all_payslips = self.get_payslips_by_date(cr, uid, start_date, end_date)
        obj_by_struct = []
        struct_list = []
        payslip_by_struct = []

        for payslip in all_payslips:
            struct_name = payslip.struct_id.name
            if struct_name not in struct_list:
                struct_list.append(struct_name)
                
        for struct in struct_list:
            struct_payslip = []
            for payslip in all_payslips:
                if payslip.struct_id.name == struct:
                    struct_payslip.append(payslip)
            obj_by_struct.append(struct_payslip)
                
        i = 0
        for struct in struct_list:
            tup_temp = (struct, obj_by_struct[i])
            payslip_by_struct.append(tup_temp)
            i += 1
            

        return payslip_by_struct
        
    def get_payslips_by_employee(self, cr, uid, all_payslips):
        obj_by_employee = []
        payslip_by_employee = []
        employee_list = []
        for payslip in all_payslips:
            employee_name = payslip.employee_id.name
            if employee_name not in employee_list:
                employee_list.append(employee_name)
            
        for employee in employee_list:
            employee_payslip = []
            for payslip in all_payslips:
                if payslip.employee_id.name == employee:
                    employee_payslip.append(payslip)
            obj_by_employee.append(employee_payslip)
                
        i = 0
        for employee in employee_list:
            tup_temp = (employee, obj_by_employee[i])
            payslip_by_employee.append(tup_temp)
            i += 1
                
        return payslip_by_employee
        
    def get_identification(self, cr, uid, payslips):
        res = ' '
        for payslip in payslips:
            res = payslip.employee_id.identification_id
            return res
            
    def get_bank_account(self, cr, uid, payslips):
        res = ' '
        for payslip in payslips:
            res = payslip.employee_id.bank_account_id.acc_number
            return res
        
    def get_hn(self, cr, uid, payslips):
        code = 'HN'
        res = 0.00
        for payslip in payslips:
            for line in payslip.line_ids:
                if line.code == code:
                    res += line.number_of_hours
        return res
        
    def get_he(self, cr, uid, payslips):
        code = 'HE'
        res = 0.00
        for payslip in payslips:
            for line in payslip.line_ids:
                if line.code == code:
                    res += line.number_of_hours        
        return res
    
    def get_basic(self, cr, uid, payslips):
        code = 'BASE'
        res = 0.00
        for payslip in payslips:
            for line in payslip.line_ids:
                if line.code == code:
                    res += line.total
        return res
        
    def get_exs(self, cr, uid, payslips):
        code = 'EXS'
        res = 0.00
        for payslip in payslips:
            for line in payslip.line_ids:
                if line.code == code:
                    res += line.total
        return res
        
    def get_gross(self, cr, uid, payslips):
        code = 'BRUTO'
        res = 0.00
        for payslip in payslips:
            for line in payslip.line_ids:
                if line.code == code:
                    res += line.total
        return res
    
    def get_ccss(self, cr, uid, payslips):
        code = 'CCSS-EMP'
        code2 = 'Banco Popular-EMP'
        res = 0.00
        for payslip in payslips:
            for line in payslip.line_ids:
                if line.code == code:
                    res += line.total
                elif line.code == code2:
                    res += line.total
        return res
    
    
    def get_net(self, cr, uid, payslips):
        code = 'NETO'
        res = 0.00
        for payslip in payslips:
            for line in payslip.line_ids:
                if line.code == code:
                    res += line.total
        return res


    def get_rent(self, cr, uid, payslips):
        code = 'Renta'
        res = 0.00
        for payslip in payslips:
            for line in payslip.line_ids:
                if line.code == code:
                    res += line.total
        return res

HeaderFooterTextWebKitParser(
    'report.l10n_cr_hr_payroll.account.payroll_report_for_month',
    'account.account',
    'addons/l10n_cr_hr_payroll/report/payroll_report_for_month.mako',
    parser=payroll_report_for_month)
