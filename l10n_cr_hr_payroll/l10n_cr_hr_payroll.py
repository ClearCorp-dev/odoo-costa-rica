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
    
class hrSalaryrule(orm.Model):
    _inherit = 'hr.salary.rule'

    _columns = {
        'rent_apply': fields.boolean('Apply rent', help="If this rule is for rent"),
    }
    
    _defaults = {
        'amount_python_compute': '''
# Available variables:
#----------------------
# payslip: object containing the payslips
# employee: hr.employee object
# contract: hr.contract object
# rules: object containing the rules code (previously computed)
# categories: object containing the computed salary rule categories (sum of amount of all rules belonging to that category).
# worked_days: object containing the computed worked days.
# inputs: object containing the computed inputs.
# hr_settings: hr.config.settings object where is, for example, rent limits. It is a browse record

# Note: returned value have to be set in the variable 'result'

result = contract.wage * 0.10''',
        'condition_python':
'''
# Available variables:
#----------------------
# payslip: object containing the payslips
# employee: hr.employee object
# contract: hr.contract object
# rules: object containing the rules code (previously computed)
# categories: object containing the computed salary rule categories (sum of amount of all rules belonging to that category).
# worked_days: object containing the computed worked days
# inputs: object containing the computed inputs
# hr_settings: hr.config.settings object where is, for example, rent limits. It is a browse record

# Note: returned value have to be set in the variable 'result'

result = rules.NET > categories.NET * 0.10''',
    }
    
    def satisfy_condition(self, cr, uid, rule_id, localdict, context=None):
        """
            Update dictionary 'localdict' to include hr.config.settings object
            and then, use this object to get rent limits in python code on 
            rule salary
        """
        
        company_obj = self.pool.get('res.company')
        company_id = company_obj._company_default_get(cr, uid, 'l10n.cr.hr.payroll', context=context) #module name
        hr_settings_id = self.pool.get('hr.config.settings').search(cr, uid, [('rent_company_id','=', company_id)], context=context)
        hr_settings = self.pool.get('hr.config.settings').browse(cr, uid, hr_settings_id, context=context)
        
        #Update localdict
        localdict.update({'hr_settings':hr_settings})
        
        super(hrSalaryrule, self).satisfy_condition(cr, uid, rule_id, localdict, context=context)
    