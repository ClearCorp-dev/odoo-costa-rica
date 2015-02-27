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


ADDRESS_FIELDS = ('county_id', 'district_id', 'region_id')


class Partner(osv.Model):

    _inherit = 'res.partner'

    def onchange_district(self, cr, uid, ids, district_id, context=None):
        res = {}
        if district_id:
            district_obj = self.pool.get('res.country.district')
            district = district_obj.browse(
                cr, uid, district_id, context=context)
            res['county_id'] = district.county_id.id
            res['region_id'] = district.region_id.id
        else:
            res['county_id'] = False
            res['region_id'] = False
        return {
            'value': res
        }

    def onchange_county(self, cr, uid, ids, county_id, context=None):
        res = {}
        if county_id:
            county_obj = self.pool.get('res.country.county')
            county = county_obj.browse(
                cr, uid, county_id, context=context)
            res['state_id'] = county.state_id.id
        else:
            res['state_id'] = False
        return {
            'value': res
        }

    def _address_fields(self, cr, uid, context=None):
        res = super(Partner, self)._address_fields(cr, uid, context=context)
        return res + list(ADDRESS_FIELDS)

    _columns = {
        'county_id': fields.many2one('res.country.county', string='County'),
        'district_id': fields.many2one(
            'res.country.district', string='District'),
        'region_id': fields.many2one(
            'res.country.region', string='Region'),
    }
