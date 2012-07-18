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

import netsvc
from osv import fields, orm
import tools
from tools.translate import _

class AccountingReportLibrary(orm.Model):
    _name =  "accounting.report.library"
    _description = "Library for Accounting Reports"
        
    def get_move_lines(self, cr, uid, account_ids, filter_type='', filter_data=None, fiscalyear=None, target_move='all', unreconcile = False, context=None):
        account_obj = self.pool.get('account.account')
        move_line_obj = self.pool.get('account.move.line')
        move_lines_ids = []
        
        if unreconcile == False:
            if target_move == 'all':
                if filter_type == '' and filter_data == None and fiscalyear == None:
                    move_line_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids)], context=context)
                elif filter_type == 'filter_date':
                    date_stop = filter_data[1]
                    move_line_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('date', '<=', date_stop)], context=context)
                elif filter_type == 'filter_period':
                    periods_ids = self.pool.get('account.period').search(cr, uid, [('date_stop', '<=', filter_data[1].date_stop)])
                    move_line_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('period_id.id', 'in', periods_ids)], context=context)
                elif filter_type == '' and fiscalyear != None:
                    date_stop = fiscalyear.date_stop
                    move_line_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('date', '<=', date_stop)], context=context)
            elif target_move == 'posted':
                if filter_type == '' and filter_data == None and fiscalyear == None:
                    move_line_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('move_id.state', '=', 'posted')], context=context)
                elif filter_type == 'filter_date':
                    date_stop = filter_data[1]
                    move_line_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('date', '<=', date_stop), ('move_id.state', '=', 'posted')], context=context)
                elif filter_type == 'filter_period':
                    periods_ids = self.pool.get('account.period').search(cr, uid, [('date_stop', '<=', filter_data[1].date_stop)])
                    move_line_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('period_id.id', 'in', periods_ids), ('move_id.state', '=', 'posted')], context=context)
                elif filter_type == '' and fiscalyear != None:
                    date_stop = fiscalyear.date_stop
                    move_line_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('date', '<=', date_stop), ('move_id.state', '=', 'posted')], context=context)
        else:
            if target_move == 'all':
                if filter_type == '' and filter_data == None and fiscalyear == None:
                    move_line_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('reconcile_id', '=', False)], context=context)
                elif filter_type == 'filter_date':
                    date_stop = filter_data[1]
                    move_line_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('date', '<=', date_stop), ('reconcile_id', '=', False)], context=context)
                    move_line_ids = move_line_ids + self.get_move_lines_unconciled(cr, uid, account_ids, filter_type=filter_type, filter_data=filter_data, context=context)
                elif filter_type == 'filter_period':
                    periods_ids = self.pool.get('account.period').search(cr, uid, [('date_stop', '<=', filter_data[1].date_stop)])
                    move_line_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('period_id.id', 'in', periods_ids), ('reconcile_id', '=', False)], context=context)
                    move_line_ids = move_line_ids + self.get_move_lines_unconciled(cr, uid, account_ids, filter_type=filter_type, filter_data=filter_data, context=context)
                elif filter_type == '' and fiscalyear != None:
                    date_stop = fiscalyear.date_stop
                    move_line_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('date', '<=', date_stop), ('reconcile_id', '=', False)], context=context)
                    move_line_ids = move_line_ids + self.get_move_lines_unconciled(cr, uid, account_ids, fiscalyear=fiscalyear, context=context)
            elif target_move == 'posted':
                if filter_type == '' and filter_data == None and fiscalyear == None:
                    move_line_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('move_id.state', '=', 'posted'), ('reconcile_id', '=', False)], context=context)
                elif filter_type == 'filter_date':
                    date_stop = filter_data[1]
                    move_line_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('date', '<=', date_stop), ('move_id.state', '=', 'posted'), ('reconcile_id', '=', False)], context=context)
                    move_line_ids = move_line_ids + self.get_move_lines_unconciled(cr, uid, account_ids, filter_type=filter_type, filter_data=filter_data, context=context)
                elif filter_type == 'filter_period':
                    periods_ids = self.pool.get('account.period').search(cr, uid, [('date_stop', '<=', filter_data[1].date_stop)])
                    move_line_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('period_id.id', 'in', periods_ids), ('move_id.state', '=', 'posted'), ('reconcile_id', '=', False)], context=context)
                    move_line_ids = move_line_ids + self.get_move_lines_unconciled(cr, uid, account_ids, filter_type=filter_type, filter_data=filter_data, context=context)
                elif filter_type == '' and fiscalyear != None:
                    date_stop = fiscalyear.date_stop
                    move_line_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('date', '<=', date_stop), ('move_id.state', '=', 'posted'), ('reconcile_id', '=', False)], context=context)
                    move_line_ids = move_line_ids + self.get_move_lines_unconciled(cr, uid, account_ids, fiscalyear=fiscalyear, context=context)
            
        move_lines = move_line_ids and move_line_obj.browse(cr, uid, move_line_ids) or []
        
        
        return move_lines
    
    def get_move_lines_unconciled(self, cr, uid, account_ids, filter_type='', filter_data=None, fiscalyear=None, context=None):
        account_obj = self.pool.get('account.account')
        move_line_obj = self.pool.get('account.move.line')
        move_reconcile_obj = self.pool.get('account.move.reconcile')
        move_lines_conciled_ids = []
        move_lines_ids = []
                
        if filter_type == 'filter_date':
            date_stop = filter_data[1]
            move_lines_conciled_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('date', '<=', date_stop), ('reconcile_id', '!=', False)], context=context)
        elif filter_type == 'filter_period':
            periods_ids = self.pool.get('account.period').search(cr, uid, [('date_stop', '<=', filter_data[1].date_stop)])
            move_lines_conciled_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('period_id.id', 'in', periods_ids), ('reconcile_id', '!=', False)], context=context)
        elif filter_type == '' and fiscalyear != None:
            date_stop = fiscalyear.date_stop
            move_lines_conciled_ids = move_line_obj.search(cr, uid, [('account_id', 'in', account_ids), ('date', '<=', date_stop), ('reconcile_id', '!=', False)], context=context)
            
        move_lines_conciled = move_lines_conciled_ids and move_line_obj.browse(cr, uid, move_lines_conciled_ids) or []
        
        for move_line_conciled in move_lines_conciled:
            move_reconcile = move_line_conciled.reconcile_id
            for line in move_reconcile.line_id:
                if filter_type == 'filter_period':
                    if line.period_id.id not in periods_ids:
                        move_lines_ids.append(move_line_conciled.id)
                        break
                else:
                    if line.date >= date_stop:
                        move_lines_ids.append(move_line_conciled.id)
                        break
                    
        return move_lines_ids

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
