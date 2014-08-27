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

from datetime import datetime
from openerp.tools.translate import _
from openerp.osv import fields,osv, orm

    
class hrRulesalary(osv.osv):
    _inherit = 'hr.salary.rule'

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
# hr_conf: object of hr.config.settings. It is a browse record
# hr_salary_rule: object for call hr_salary_rule functions

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
# hr_conf: object of hr.config.settings. It is a browse record
# hr_salary_rule: object for call hr_salary_rule functions

# Note: returned value have to be set in the variable 'result'

result = rules.NET > categories.NET * 0.10''',
    }
    
    """
        In this method we add a new BrowsableObject from hr.config settings.
        This is for use rent configuration for each company and compute the rent 
        amount in a standard way.  
    """
    def satisfy_condition(self, cr, uid, rule_id, localdict, context=None):
       
        #Get user's company and hr.config.settings associated to the company
        user_company = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id
        hr_conf_id = self.pool.get('hr.config.settings').search(cr, uid, [('rent_company_id', '=', user_company.id)], context=context)
        
        if not hr_conf_id:
            raise osv.except_osv(_('Error!'), _('There not exist a configuration for rent. Check company configuration in human resources section'))
        
        hr_conf_obj = self.pool.get('hr.config.settings').browse(cr, uid, hr_conf_id, context=context)[0]

        #Update localdict with new variable
        localdict.update({'hr_conf':hr_conf_obj})
        
        hr_salary_rule_obj = self.pool.get('hr.salary') #object from hr salary rule to use in python code
        localdict.update({'hr_salary_rule':hr_salary_rule_obj})
        
        result = super(hrRulesalary, self).satisfy_condition(cr, uid, rule_id, localdict, context=context)
        return result
    
    """
        This function is designed to be called from python code in the salary rule.
        It receive as parameters the variables that can be used by default in 
        python code on salary rule.
        
        It receive hr_conf, a parameter and it is a hr.conf.settings object, but also,
        it can be declare inside in function
    """
    def compute_rent_employee(self, cr, uid, hr_conf, inputs, employee, categories):
        range1 = 0.1
        range2 = 0.15            

        limit1 = hr_conf.first_limit #From hr.conf.settings, it's in company
        limit2 = hr_conf.second_limit

        spouse_amount = hr_conf.amount_per_spouse
        child_amount = hr_conf.amount_per_child

        if inputs.RENTA and inputs.RENTA.amount != 0:
            result = inputs.RENTA.amount
        else:
            if inputs.NPM and inputs.NPM.amount != 0:
                month_payments = inputs.NPM.amount
            else:
                month_payments = 2

        children_numbers = employee.report_number_child
        siblings_amount = 0
        
        if employee.report_spouse:
            siblings_amount += spouse_amount
        siblings_amount += children_numbers * child_amount

        if inputs.SBM and inputs.SBM.amount != 0:
            monthly_amount = inputs.SBM.amount
        else:
            monthly_amount = categories.BRUTO * month_payments

        range2_amount = monthly_amount - limit2
        if range2_amount < 0:
            range2_amount = 0
    
        range1_amount = monthly_amount - range2_amount - limit1
        if range1_amount < 0:
            range1_amount = 0
    
        rent = 0
        rent += range1_amount * range1
        rent += range2_amount * range2
        rent = rent - siblings_amount
        rent = rent / month_payments

        if rent > 0:
            result = rent
        else:
            result = 0
    
    def compute_total_rent(self, cr, uid, hr_conf, inputs, employee, categories, payslip):
        SBA = 0.0 #Previous Gross Salary
        SBP = 0.0 #Currently Gross Salary
        SBF = 0.0 #Future Gross Salary
        SBT = 0.0 #Gross Salary Total (this is SBA + SBP + SBF)
        rent_empl = 0.0
        temp_rent = 0.0
        total_rent = 0.0
        sbf_temp = 0.0        
        #objects
        payslip_obj = self.pool.get('hr.payslip')
                
        #1. Get number of payments
        payments = payslip_obj.payment_per_month(cr, uid, payslip)
        
        #2. Initialize variables
        SBA = payslip_obj.get_SBA(cr, uid, employee, payslip)
        SBP = categories.BRUTO
        SBF = categories.BASE
        rent_empl = self.compute_rent_employee(cr, uid, hr_conf, inputs, employee, categories)
        
        while (payments > 0):
            sbf_temp = SFB * payments - 1
            SBF += sbf_temp 
            temp_rent += rent_empl / payments
            SBT = SBA + SBP + SBF
            #only check last payment
            #if :
                #total_rent += SBT / temp_rent
            #else:
                
                
        
        
        
    