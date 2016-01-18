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

import werkzeug
from openerp import models, fields


def urlplus(url, params):
    return werkzeug.Href(url)(params or None)


class res_partner(models.Model):

    _inherit = "res.partner"

    def google_map_img(self, cr, uid, ids, zoom=17, width=298, height=298,
                       context=None):
        partner = self.browse(cr, uid, ids[0], context=context)
        marker = 'color:red'
        params = {
            'size': "%sx%s" % (height, width),
            'markers': '%s|%s,%s' % (marker, partner.partner_latitude or '',
                                     partner.partner_longitude or ''),
            'zoom': partner.partner_zoom,
            'sensor': 'false',

        }
        return urlplus('//maps.googleapis.com/maps/api/staticmap', params)

    def google_map_link(self, cr, uid, ids, zoom=8, context=None):
        partner = self.browse(cr, uid, ids[0], context=context)
        params = {
            'q': '%s,%s' % (
                partner.partner_latitude or '', partner.partner_longitude or
                 ''),
            'z': 8
        }
        if partner.maps_url:
            return urlplus(partner.maps_url, None)
        else:
            return urlplus('https://maps.google.com/maps', params)

    partner_latitude = fields.Float(digits=(16, 7))
    partner_longitude = fields.Float(digits=(16, 7))
    maps_url = fields.Char('Maps Url', size=512)
    partner_zoom = fields.Integer('Zoom')
