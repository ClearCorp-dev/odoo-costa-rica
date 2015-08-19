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

from openerp import api, models

MODULE = 'l10n_cr_hr_payroll_pay_generator_promerica'
REPORT = 'report_payroll_promerica'


class PayrollPromericaReport(models.AbstractModel):

    _name = 'report' + '.' + MODULE + '.' + REPORT

    def compute_payslip_lines(self, cr, slip, salary_rule_id):
        cr.execute("""SELECT
CASE WHEN
    (SELECT SUM(LINE.amount)
    FROM hr_payslip_line AS LINE
    WHERE LINE.slip_id = PAYSLIP.id AND
      LINE.salary_rule_id = %s) IS NULL THEN 0.0
  ELSE
    (SELECT SUM(LINE.amount)
    FROM hr_payslip_line AS LINE
    WHERE LINE.slip_id = PAYSLIP.id AND
      LINE.salary_rule_id = %s)
  END AS amount
FROM hr_payslip as PAYSLIP
WHERE PAYSLIP.id = %s""", [salary_rule_id, salary_rule_id, slip.id])
        result = cr.dictfetchone()
        return result

    @api.cr_uid_ids_context
    def render_html(self, cr, uid, ids, data=None, context=None):
        report_obj = self.pool['report']
        report = report_obj._get_xls_report_from_name(
            cr, uid,
            'l10n_cr_hr_payroll_pay_generator_'
            'promerica.report_payroll_promerica')
        report_model_obj = self.pool[report.model]
        ids = data.get('ids', False)
        docs = report_model_obj.browse(cr, uid, ids, context=context)
        docargs = {
            'doc_ids': ids,
            'doc_model': report.model,
            'docs': docs,
            'salary_rule_id': data.get('salary_rule_id', False),
            'compute_payslip_lines': self.compute_payslip_lines,
        }
        return report_obj.render(
            cr, uid, [], report.report_name,
            docargs, context=context)
