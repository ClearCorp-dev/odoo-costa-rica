# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'HR Payroll Rent C.R.',
    'summary': 'Multicurrency rent to payroll',
    'version': '8.0.1.0',
    'category': 'Extra-tools',
    'website': 'http://clearcorp.cr',
    'author': 'ClearCorp',
    'license': 'AGPL-3',
    'sequence': 10,
    'application': False,
    'installable': True,
    'auto_install': False,
    'depends': [
        'l10n_cr_hr_payroll',
    ],
    'data': [
        "views/l10n_cr_hr_payroll_rent_view.xml",
    ],
}
