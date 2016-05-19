# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class ResCompany(models.Model):

    _inherit = 'res.company'

    rent_currency_id = fields.Many2one('res.currency')


class HrConfigSettings(models.TransientModel):

    _inherit = 'hr.config.settings'

    rent_currency_id = fields.Many2one('res.currency', string="Rent Currency",
                                       required=True)

    """Get the default rent currency"""
    def get_default_rent_currency_id(self, cr, uid, fields, context=None):
        company_obj = self.pool.get('res.company')
        company_id = company_obj._company_default_get(
            cr, uid, 'l10n_cr_hr_payroll_multicurrency', context=context)
        company = company_obj.browse(cr, uid, company_id, context=context)
        return {'rent_currency_id': company.rent_currency_id.id}

    """Set the default rent currency"""
    def set_rent_currency_id(self, cr, uid, ids, context=None):
        config = self.browse(cr, uid, ids[0], context)
        config.rent_company_id.write(
            {'rent_currency_id': config.rent_currency_id.id})


class HrRuleSalary(models.Model):

    _inherit = 'hr.salary.rule'

    def compute_rent_employee(self, company, employee, SBT, payslip):
        res = super(HrRuleSalary, self).compute_rent_employee(
            company, employee, SBT, payslip)

        if not employee.contract_id.currency_id:
            return res
        subtotal = 0.0
        exceed_2 = 0.0
        exceed_1 = 0.0
        total = 0.0

        limit1 = company.rent_currency_id.with_context(
            {'date': payslip.date_to}).compute(
                company.first_limit, employee.contract_id.currency_id)
        limit2 = company.rent_currency_id.with_context(
            {'date': payslip.date_to}).compute(
                company.second_limit, employee.contract_id.currency_id)

        spouse_amount = company.rent_currency_id.with_context(
            {'date': payslip.date_to}).compute(
                company.amount_per_spouse, employee.contract_id.currency_id)
        child_amount = company.rent_currency_id.with_context(
            {'date': payslip.date_to}).compute(
                company.amount_per_child, employee.contract_id.currency_id)

        children_numbers = employee.report_number_child

        if SBT >= limit2:
            exceed_2 = SBT - limit2
            subtotal += exceed_2 * 0.15
            limit_temp = (limit2 - limit1) * 0.10
            subtotal += limit_temp

        elif SBT >= limit1:
            exceed_1 = SBT - limit1
            subtotal += exceed_1 * 0.10

        if subtotal and employee.report_spouse:
            total = subtotal - spouse_amount -\
                (child_amount * children_numbers)
        elif subtotal:
            total = subtotal - (child_amount * children_numbers)
        return total
