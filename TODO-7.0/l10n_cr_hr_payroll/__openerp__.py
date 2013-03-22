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
    'name': 'l10n_cr_hr_payroll',
    'version': '1.0',
    'category': 'Human Resources',
    "sequence": 38,
    'complexity': "normal",
    'description': """
l10n_cr_hr_payroll.
=======================
    * Employee Contracts
    * Fortnightly Payroll Register
    * Payroll Report
    """,
    'author': 'CLEARCORP S.A.',
    'website': 'http://www.clearcorp.co.cr',
    'depends': [
        'hr',
        'hr_contract',
        'hr_payroll',
        'account',
        'account_financial_report_webkit',
        'account_voucher_payment_method',
        'base_currency_symbol',        
    ],
    'update_xml': [
                    'l10n_cr_hr_payroll_view.xml',
                    'report/report.xml',
                    'wizard/payroll_report_for_month_wizard_view.xml',
                    'report_menus.xml',
                    'payroll_report.xml',
                    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
