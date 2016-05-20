# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
import math
import logging
import re
from openerp.tools.translate import _


class product_product(osv.osv):
    _inherit = "product.template"
    _columns = {
        'adime_product': fields.boolean('Adime'),
    }
product_product()
