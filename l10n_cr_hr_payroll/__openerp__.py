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

{
    'name': 'Payroll Localization - Costa Rica',
    'version': '1.0',
    'category': 'Localization',
    "sequence": 38,
    'complexity': 'normal',
    'description': """
Payroll Localization - Costa Rica
=================================
Description
------------
This is the Costa Rica OpenERP localization and consists of:
* Salary Rule Structure
* Salary Rule Category
* Withholding tax structure
* Rent (Applied to Costa Rican's Law)
* Reports""",
    'author': 'ClearCorp',
    'website': 'http://www.clearcorp.co.cr',
    'depends': [
                'hr_payroll_extended',
                ],
    'data': [
             'data/l10n_cr_hr_payroll_salary_rule_category.xml',
             'data/l10n_cr_hr_payroll_salary_rule.xml',
             'data/report_paperformat.xml',
             'hr_config_settings.xml',
             'l10n_cr_hr_payroll_view.xml',
             'security/ir.model.access.csv',
             'views/report_payroll_periods.xml',
             'views/report_payroll_periods_employee.xml',
             'views/report_payslip_run.xml',
             'views/report_payslip.xml',
             'wizard/payroll_by_periods.xml',
             'wizard/payroll_by_periods_employee.xml',
             'l10n_cr_hr_payroll_report.xml',
             'l10n_cr_hr_payroll_menu.xml',
             ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
