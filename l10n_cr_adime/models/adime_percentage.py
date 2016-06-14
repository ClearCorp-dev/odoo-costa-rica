# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AdimeAssigned(models.Model):

    _name = 'l10n.cr.adime.percentage'

    name = fields.Char('Name', size=64, required=True)
    percentage = fields.Float('Percentage', required=True)

    @api.multi
    def name_get(self):
        result = []
        for adime in self:
            result.append(
                (adime.id, '%s (%.2f%%)' % (adime.name, adime.percentage)))
        return result
