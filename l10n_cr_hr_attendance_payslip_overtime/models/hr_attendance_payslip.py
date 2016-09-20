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

import pytz
from datetime import datetime
import time
from datetime import timedelta
from openerp.osv import osv, fields
from openerp.tools.translate import _

class PaySlip(osv.Model):

    _inherit = 'hr.payslip'

    def get_attendances_dictionary(self, cr, uid, contract, context=None):
        input_value_obj = self.pool.get('hr.payroll.extended.input.value')
        
        input_hd_id = input_value_obj.search(cr, uid, [('code','=','HD'), ('type','=','worked_days')], context=context)
        input_hm_id = input_value_obj.search(cr, uid, [('code','=','HM'), ('type','=','worked_days')], context=context)
        input_hn_id = input_value_obj.search(cr, uid, [('code','=','HN'), ('type','=','worked_days')], context=context)
        input_hed_id = input_value_obj.search(cr, uid, [('code','=','HED'), ('type','=','worked_days')], context=context)
        input_hem_id = input_value_obj.search(cr, uid, [('code','=','HEM'), ('type','=','worked_days')], context=context)
        input_hen_id = input_value_obj.search(cr, uid, [('code','=','HEN'), ('type','=','worked_days')], context=context)
        
        if not input_hd_id or not input_hm_id or not input_hn_id or not input_hed_id \
            or not input_hem_id or not input_hen_id:
            raise osv.except_osv(
                            _('Error!'),
                            _('You need to create Input Values HD, HM, HN, HED, HEM, HEN'))
        input_hd_id = input_hd_id[0]
        input_hm_id = input_hm_id[0]
        input_hn_id = input_hn_id[0]
        input_hed_id = input_hed_id[0]
        input_hem_id = input_hem_id[0]
        input_hen_id = input_hen_id[0]

        attendances_day = {
            'name': _("Attendance Working Day Hours"),
            'sequence': 1,
            'work_code': input_hd_id,
            'code': 'HD',
            'number_of_days': 0.0,
            'number_of_hours': 0.0,
            'contract_id': contract.id,
        }
        attendances_mix = {
            'name': _("Attendance Working Mix Hours"),
            'sequence': 1,
            'work_code': input_hm_id,
            'code': 'HM',
            'number_of_days': 0.0,
            'number_of_hours': 0.0,
            'contract_id': contract.id,
        }
        attendances_night = {
            'name': _("Attendance Working Night Hours"),
            'sequence': 1,
            'work_code': input_hn_id,
            'code': 'HN',
            'number_of_days': 0.0,
            'number_of_hours': 0.0,
            'contract_id': contract.id,
        }
        attendances_extra_day = {
            'name': _("Attendance Working Extra Day Hours"),
            'sequence': 1,
            'work_code': input_hed_id,
            'code': 'HED',
            'number_of_days': 0.0,
            'number_of_hours': 0.0,
            'contract_id': contract.id,
        }
        attendances_extra_mix = {
            'name': _("Attendance Working Extra Mix Hours"),
            'sequence': 1,
            'work_code': input_hem_id,
            'code': 'HEM',
            'number_of_days': 0.0,
            'number_of_hours': 0.0,
            'contract_id': contract.id,
        }
        attendances_extra_night = {
            'name': _("Attendance Working Extra Night Hours"),
            'sequence': 1,
            'work_code': input_hen_id,
            'code': 'HEN',
            'number_of_days': 0.0,
            'number_of_hours': 0.0,
            'contract_id': contract.id,
        }
        return attendances_day, attendances_mix, attendances_night, attendances_extra_day, attendances_extra_mix, attendances_extra_night

    def datetime_difference(self, cr, uid, date_from, date_to, context=None):
        date_from = date_from.replace(tzinfo=None)
        date_to = date_to.replace(tzinfo=None)
        date_difference = date_to - date_from
        hours, remainder = divmod(date_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        seconds_difference = hours * 60 * 60 + minutes * 60 + seconds
        return seconds_difference

    def get_timezone_date(self, cr, uid, user_tz, date, context={}):
        utc = pytz.timezone('UTC')
        timezone = pytz.timezone(user_tz)
        date = utc.localize(date, is_dst=False)  # UTC = no DST
        date = date.astimezone(timezone)
        return date

    def get_attendance_hours(self, cr, uid, contract, working_hours, attendance_in, attendance_out, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid)
        attendance_in_date = datetime.strptime(attendance_in.name,"%Y-%m-%d %H:%M:%S")
        attendance_out_date = datetime.strptime(attendance_out.name,"%Y-%m-%d %H:%M:%S")
        mix_max_tolerance = 12600 #3.5 total hours. (3 * 60 * 60) + (30 * 60) = 12600
        attendances_day, attendances_mix, attendances_night, attendances_extra_day, attendances_extra_mix, attendances_extra_night \
            = self.get_attendances_dictionary(cr, uid, contract, context=context)
        
        if user.tz:  # Parse the date at 12 o'clock to UTC
            attendance_in_date = self.get_timezone_date(cr, uid, user.tz, attendance_in_date, context=context)
            attendance_out_date = self.get_timezone_date(cr, uid, user.tz, attendance_out_date, context=context)
        
        #Compare hours
        if attendance_in_date.hour >= 5 and attendance_out_date.hour <= 19:
            if attendance_in_date.day == attendance_out_date.day:
                #comes after 5 and leave before 19->day
                attendances_day['number_of_days'] += 1.0
                attendances_day['number_of_hours'] += working_hours
            else:
                attendances_night['number_of_days'] += 1.0
                attendances_night['number_of_hours'] += working_hours
        elif attendance_in_date.hour < 5:
            if attendance_out_date.hour <= 5:
                #comes before 5 and leave before 5->night
                attendances_night['number_of_days'] += 1.0
                attendances_night['number_of_hours'] += working_hours
            else: #attendance_out_date.hour > 5
                #comes before 5 and leave after 5->compare hours
                hours_difference = self.datetime_difference(cr, uid, attendance_in_date, attendance_out_date, context=context)
                if hours_difference > mix_max_tolerance:
                    #Is night
                    attendances_night['number_of_days'] += 1.0
                    attendances_night['number_of_hours'] += working_hours
                else:
                    #Is mix
                    attendances_mix['number_of_days'] += 1.0
                    attendances_mix['number_of_hours'] += working_hours
        elif attendance_in_date.hour >= 19:
            if attendance_out_date.hour < 5 or attendance_out_date.hour >= 19:
                #comes after 19 and leave before 5 or after 19->night
                attendances_night['number_of_days'] += 1.0
                attendances_night['number_of_hours'] += working_hours
            else:
                #comes after 19 and leave after 5 but before 19
                day_hour_limit = datetime(attendance_out_date.year, attendance_out_date.month, attendance_out_date.day, 05, 00, 00)
                hours_difference = self.datetime_difference(cr, uid, attendance_in_date, day_hour_limit, context=context)
                if hours_difference > mix_max_tolerance:
                    #Is night
                    attendances_night['number_of_days'] += 1.0
                    attendances_night['number_of_hours'] += working_hours
                else:
                    #Is mix
                    attendances_mix['number_of_days'] += 1.0
                    attendances_mix['number_of_hours'] += working_hours
        elif attendance_in_date.hour >= 5 and attendance_out_date.hour >= 19:
            #comes after 5 and leave after 19
            night_hour_limit = datetime(attendance_in_date.year, attendance_in_date.month, attendance_in_date.day, 19, 00, 00)
            hours_difference = self.datetime_difference(cr, uid, night_hour_limit, attendance_out_date, context=context)
            if hours_difference > mix_max_tolerance:
                #Is night
                attendances_night['number_of_days'] += 1.0
                attendances_night['number_of_hours'] += working_hours
            else:
                #Is mix
                attendances_mix['number_of_days'] += 1.0
                attendances_mix['number_of_hours'] += working_hours
        if attendances_day['number_of_hours'] > 8.0:
            attendances_extra_day['number_of_days'] += 1.0
            attendances_extra_day['number_of_hours'] += (attendances_day['number_of_hours'] - 8)
            attendances_day['number_of_hours'] = 8.0
        if attendances_mix['number_of_hours'] > 7.0:
            attendances_extra_mix['number_of_days'] += 1.0
            attendances_extra_mix['number_of_hours'] += (attendances_mix['number_of_hours'] - 7)
            attendances_mix['number_of_hours'] = 7.0
        if attendances_night['number_of_hours'] > 6.0:
            attendances_extra_night['number_of_days'] += 1.0
            attendances_extra_night['number_of_hours'] += (attendances_night['number_of_hours'] - 6)
            attendances_night['number_of_hours'] = 6.0
        return attendances_day, attendances_mix, attendances_night, attendances_extra_day, attendances_extra_mix, attendances_extra_night

    def get_worked_day_lines(self, cr, uid, contract_ids, date_from, date_to, context=None):
        res = []
        contract_obj = self.pool.get('hr.contract')
        attendance_obj = self.pool.get('hr.attendance')

        for contract in contract_obj.browse(cr, uid, contract_ids, context=context):
            if contract.is_attendance:
                day_from = datetime.strptime(date_from,"%Y-%m-%d")
                day_to = datetime.strptime(date_to,"%Y-%m-%d")
                nb_of_days = (day_to - day_from).days + 1
                attendances_day, attendances_mix, attendances_night, attendances_extra_day, attendances_extra_mix, attendances_extra_night = \
                    self.get_attendances_dictionary(cr, uid, contract, context=context)
                for day in range(0, nb_of_days):
                    had_work,attendance_hours = contract._attendance_normal_hours_on_day(day_from + timedelta(days=day), context=context)[0]
                    working_hours = contract._attendance_sum_hours_on_day(attendance_hours, context=context)[0]
                    if had_work:
                        for attendance_in_id in attendance_hours.keys():
                            attendance_in = attendance_obj.browse(cr, uid, attendance_in_id, context=context)[0]
                            
                            # Condition to find all sign_in from date day
                            domain_sign_out = [('employee_id','=',contract.employee_id.id),
                            ('action','=','sign_out'),
                            ('name','>=',attendance_in.name)]
                            attendance_out_ids = attendance_obj.search(cr, uid, domain_sign_out, limit=1, order='name asc', context=context)
                            # If there is no sign_out will skip
                            if not attendance_out_ids:
                                continue
                            attendance_out = attendance_obj.browse(cr, uid, attendance_out_ids[0], context=context)
                            attendances_day_t, attendances_mix_t, attendances_night_t, attendances_extra_day_t, attendances_extra_mix_t, \
                                attendances_extra_night_t = self.get_attendance_hours(cr, uid, contract, working_hours, attendance_in, attendance_out, context=context)
                            #Assign to general dictionarys
                            attendances_day['number_of_days'] += attendances_day_t['number_of_days']
                            attendances_day['number_of_hours'] += attendances_day_t['number_of_hours']
                            attendances_mix['number_of_days'] += attendances_mix_t['number_of_days']
                            attendances_mix['number_of_hours'] += attendances_mix_t['number_of_hours']
                            attendances_night['number_of_days'] += attendances_night_t['number_of_days']
                            attendances_night['number_of_hours'] += attendances_night_t['number_of_hours']
                            attendances_extra_day['number_of_days'] += attendances_extra_day_t['number_of_days']
                            attendances_extra_day['number_of_hours'] += attendances_extra_day_t['number_of_hours']
                            attendances_extra_mix['number_of_days'] += attendances_extra_mix_t['number_of_days']
                            attendances_extra_mix['number_of_hours'] += attendances_extra_mix_t['number_of_hours']
                            attendances_extra_night['number_of_days'] += attendances_extra_night_t['number_of_days']
                            attendances_extra_night['number_of_hours'] += attendances_extra_night_t['number_of_hours']

                if attendances_day['number_of_hours'] != 0.0:
                    res += [attendances_day]
                if attendances_mix['number_of_hours'] != 0.0:
                    res += [attendances_mix]
                if attendances_night['number_of_hours'] != 0.0:
                    res += [attendances_night]
                if attendances_extra_day['number_of_hours'] != 0.0:
                    res += [attendances_extra_day]
                if attendances_extra_mix['number_of_hours'] != 0.0:
                    res += [attendances_extra_mix]
                if attendances_extra_night['number_of_hours'] != 0.0:
                    res += [attendances_extra_night]
            else:
                if contract.employee_id.company_id.attendance_payslip_use_default:
                    normal_hours = contract.employee_id.company_id.attendance_payslip_normal_hours
                    if normal_hours:
                        attendances_day['number_of_hours'] = normal_hours
                        attendances_day['number_of_days'] = nb_of_days
                        res += [attendances_day]
                res += super(PaySlip, self).get_worked_day_lines(cr, uid, [contract.id], date_from, date_to, context=context)
        return res
