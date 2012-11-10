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
    'name': 'Costa Rica Account Financial Statements',
    'version': '1.0',
    'category': 'Finance',
    "sequence": 38,
    'complexity': "normal",
    'description': """
Costa Rica Account Financial Statements
=======================================
    * Profit Statement Report
    * Situation Balance Statement Report
    """,
    'author': 'CLEARCORP S.A.',
    'website': 'http://www.clearcorp.co.cr',
    'depends': [
        'account',
        'account_financial_report_webkit',
        'account_voucher_payment_method',
        'base_currency_symbol',    
        'report_webkit',    
    ],
    'update_xml': [
                    'report/report.xml',
                    'wizard/profit_statement_report_wizard_view.xml',
                    'wizard/situation_balance_statement_report_wizard_view.xml',
                    'report_menus.xml',
                    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
