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


class Region(osv.Model):
    """Region"""

    _name = 'res.country.region'
    _description = __doc__

    _columns = {
        'name': fields.char('Name', required=True),
        'code': fields.char('Code'),
        'country_id': fields.many2one('res.country', string='Country',
                                      required=True),
    }


class County(osv.Model):
    """County"""

    _name = 'res.country.county'
    _description = __doc__

    _columns = {
        'name': fields.char('Name', required=True),
        'code': fields.char('Code', required=True),
        'state_id': fields.many2one('res.country.state', string='State',
                                    required=True),
    }


class District(osv.Model):
    """District"""

    _name = 'res.country.district'
    _description = __doc__

    _columns = {
        'name': fields.char('Name', required=True),
        'code': fields.char('Code', required=True),
        'county_id': fields.many2one('res.country.county', string='County',
                                     required=True),
        'region_id': fields.many2one('res.country.region', string='Region'),
    }
