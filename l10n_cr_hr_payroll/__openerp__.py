#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
    """,
    'author':'Ronald Rubi',
    'website':'http://www.clearcorp.co.cr',
    'depends': [
        'hr',
        'hr_contract',
        'hr_payroll',
    ],
    'init_xml': [
    ],
    'update_xml': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
