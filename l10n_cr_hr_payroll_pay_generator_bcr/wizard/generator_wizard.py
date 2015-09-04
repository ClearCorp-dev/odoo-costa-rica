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

from openerp import models, api


class PayGenerator(models.TransientModel):

    _inherit = 'hr.payroll.pay.generator.generator.wizard'

    @api.multi
    def generator_exectute(self):
        assert len(self) == 1, \
            'This option should only be used for a single id at a time.'

        if self.pay_type_id.code == 'bcr':
            # Filter payslips by pay type
            payslip_obj = self.env['hr.payslip']
            slip_ids = payslip_obj.search([
                ('payslip_run_id', '=', self.payslip_run_id.id),
                ('employee_id', 'in', self.employee_ids.ids)
            ])
            data = {
                'ids': slip_ids.ids,
                'salary_rule_id': self.salary_rule_id.id
            }
            # return bac report
            return self.env['report'].get_action(
                slip_ids,
                'l10n_cr_hr_payroll_pay_generator_bcr.report_payroll_bcr',
                data=data)
        return super(PayGenerator, self).generator_exectute()
