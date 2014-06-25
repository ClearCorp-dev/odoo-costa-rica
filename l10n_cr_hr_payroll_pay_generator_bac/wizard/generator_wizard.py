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

from openerp.osv import osv, fields

class PayGenerator(osv.TransientModel):

    _inherit = 'hr.payroll.pay.generator.generator.wizard'

    def generator_exectute(self, cr, uid, ids, context=None):
        res = super(PayGenerator, self).generator_exectute(cr, uid, ids, context=context)
        wizard = self.browse(cr, uid, ids[0], context=context)
        if wizard.pay_type_id.code == 'bac':
            # return bac report
            employee_ids = [employee.id for employee in wizard.employee_ids]
            data = {
                    'payslip_run_id': wizard.payslip_run_id.id,
                    'employee_ids': employee_ids,
                    'salary_rule_id': wizard.salary_rule_id.id,
            }
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'l10n_cr_hr_payroll_pay_generator_bac_report',
                'datas': data,
                'context': context
            }
        return res