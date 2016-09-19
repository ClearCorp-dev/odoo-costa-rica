# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Attendance Payslip Overtime',
    'version': '8.0.1.0',
    'author': 'ClearCorp',
    'website': 'http://clearcorp.cr',
    'category': 'Human Resources',
    'summary': 'Extend functionality to hr_attendance_payslip',
    'sequence': 10,
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'active': False,
    'depends': [
        'hr_payroll_extended',
        'hr_attendance_payslip',
    ],
    'data': [
    ],
}
