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

import netsvc
import tools
from datetime import datetime
from datetime import date, timedelta
from openerp.tools.translate import _
from openerp.osv import fields,osv, orm

class hrContract(orm.Model):
    """
    Employee contract based on the visa, work permits
    allows to configure different Salary structure
    """

    _inherit = 'hr.contract'
    _description = 'Employee Contract'
    _columns = {
        'schedule_pay': fields.selection([
            ('fortnightly', 'Fortnightly'),
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('semi-annually', 'Semi-annually'),
            ('annually', 'Annually'),
            ('weekly', 'Weekly'),
            ('bi-weekly', 'Bi-weekly'),
            ('bi-monthly', 'Bi-monthly'),
            ], 'Scheduled Pay', select=True),
    }

    _defaults = {
        'schedule_pay': 'monthly',
    }

class hrPaysliprun(orm.Model):
    _inherit = 'hr.payslip.run'
    _columns = {
        'schedule_pay': fields.selection([
            ('fortnightly', 'Fortnightly'),
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('semi-annually', 'Semi-annually'),
            ('annually', 'Annually'),
            ('weekly', 'Weekly'),
            ('bi-weekly', 'Bi-weekly'),
            ('bi-monthly', 'Bi-monthly'),
            ], 'Scheduled Pay', select=True, readonly=True, states={'draft': [('readonly', False)]}),      
    }
    
class hr_employee(osv.osv):
    _name = "hr.employee"
    _description = "Employee"
    _inherit = "hr.employee"
    
    def _check_report_number_child(self, cr, uid, ids, context=None):
        for employee in self.browse(cr, uid, ids, context=context):
            if employee.report_number_child < 0:
                return False
        return True
    
    _columns = {
        'report_spouse': fields.boolean('Report Spouse', help="If this employee reports his spouse for rent payment"),
        'report_number_child': fields.integer('Number of children to report', help="Number of children to report for rent payment"),        
    }
    
    _defaults = {
        'report_number_child': 0,
    }
    
    _constraints = [
        (_check_report_number_child, 'Error! The number of child to report must be greater or equal to zero.', ['report_number_child'])
    ]

class hrPayslipinherit(osv.osv_memory):
    
    _inherit = 'hr.payslip'
    
    #Get the previous payslip for an employee. Return all payslip that are in
    #the same month than current payslip
    def get_previous_payslips(self, cr, uid, employee, actual_payslip, context=None):
        payslip_list = []
        date_to = datetime.strptime(payslip.date_to, '%Y-%m-%d')
        month_date_to = date_to.month
        payslips_ids = self.pool.get('hr.payslip').search(cr, uid, [('employee_id','=', employee.id), ('date_to','<', payslip.date_to)], context=context)
        
        for empl_payslip in self.pool.get('hr.payslip').browse(cr, uid, payslip_ids, context=context):
            temp_date = datetime.strptime(empl_payslip.date_to, '%Y-%m-%d')
            if (temp_date.month == month_date_to) and (temp_date.year == month_date_to.year):
                payslip_list.append(empl_payslip)
        
        return payslip_list
    
    #get SBA for employee (Gross salary for an employee)
    def get_SBA(self, cr, uid, employee, actual_payslip, context=None):
        SBA = 0.0
        payslip_list = self.get_previous_payslips(cr, uid, employee, actual_payslip, context=context) #list of previous payslips
        
        for payslip in payslip_list:
            for line in payslip.lines:
                 if line.code == 'BRUTO':
                     SBA += line.total        
        return SBA
    
    #Get quantity of days between two dates
    def days_between_days(self, cr, uid, date_from, date_to, context=None):
        d1 = datetime.strptime(date_from, "%Y-%m-%d")
        d2 = datetime.strptime(date_to, "%Y-%m-%d")
        return abs((d2 - d1).days)
    
    #Get number of payments per month
    def payment_per_month(self, cr, uid, payslip, context=None):
        payments = 0
        
        date_from = datetime.strptime(payslip.date_from, '%Y-%m-%d')
        date_to = datetime.strptime(payslip.date_to, '%Y-%m-%d')
        
        days = self.days_between_days(cr, uid, date_from, date_to, context=context)
        next_date = date_from + timedelta(days=days)
        
        month_date_to = date_to.month
        month_date_next = next_date.month
        
        while(month_date_to == month_date_next):
            payments += 1
            next_date = date_from + timedelta(days=days)
            month_date_next = next_date.month
        
        return payments