# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResPartner(models.Model):

    _inherit = 'res.partner'

    adime_id = fields.Many2one('l10n.cr.adime.percentage', 'Adime Percentage')
    is_adime = fields.Boolean('Is Adime')
