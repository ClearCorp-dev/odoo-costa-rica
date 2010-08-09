# -*- encoding: utf-8 -*-
##############################################################################
#
#    l10n_cr_base.py
#    l10n_cr_base
#    First author: Carlos Vásquez <carlos.vasquez@clearcorp.co.cr> (ClearCorp S.A.)
#    Copyright (c) 2010-TODAY ClearCorp S.A. (http://clearcorp.co.cr). All rights reserved.
#    
#    Redistribution and use in source and binary forms, with or without modification, are
#    permitted provided that the following conditions are met:
#    
#       1. Redistributions of source code must retain the above copyright notice, this list of
#          conditions and the following disclaimer.
#    
#       2. Redistributions in binary form must reproduce the above copyright notice, this list
#          of conditions and the following disclaimer in the documentation and/or other materials
#          provided with the distribution.
#    
#    THIS SOFTWARE IS PROVIDED BY <COPYRIGHT HOLDER> ``AS IS'' AND ANY EXPRESS OR IMPLIED
#    WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#    FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR
#    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#    ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#    ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#    
#    The views and conclusions contained in the software and documentation are those of the
#    authors and should not be interpreted as representing official policies, either expressed
#    or implied, of ClearCorp S.A..
#    
##############################################################################

from osv import osv,fields
import pooler
from base.res.partner.partner import _lang_get

class res_partner_function(osv.osv):
    '''
    Inherits res.partner.function to add translation to code and name fields
    '''
    _inherit = 'res.partner.function'
    
    _columns = {
        'name': fields.char('Function Name', size=64, required=True, translate=True),
        'code': fields.char('Code', size=8, required=True, translate=True),
    }
res_partner_function()

class res_partner_title(osv.osv):
    '''
    Inherits res.partner.title to add translation to shortcut field
    '''
    _inherit = 'res.partner.title'
    
    _columns = {
        'shortcut': fields.char('Shortcut', required=True, size=16, translate=True),
    }
res_partner_title()

class res_partner(osv.osv):
    '''
    Inherits res.partner to add id_number field, and lang default value
    '''
    _inherit = 'res.partner'
    _columns = {
        'id_number': fields.char('ID Number', size=30,required=False, select=1),
        'lang': fields.selection(_lang_get, 'Language', size=5, required=True, help="If the selected language is loaded in the system, all documents related to this partner will be printed in this language. If not, it will be english."),
    }
    _defaults = {
        'lang': lambda *a: 'es_ES',
    }
    
    def lang_es_install(self, cr, uid):
        lang = 'es_ES'
        modobj = pooler.get_pool(cr.dbname).get('ir.module.module')
        mids = modobj.search(cr, uid, [('state', '=', 'installed')])
        modobj.update_translations(cr, uid, mids, lang)
        return {}
        
res_partner()

class res_users(osv.osv):
    '''
    Inherits res.users to add lang and tz default values
    '''
    _inherit = 'res.users'
    _defaults = {
        'context_lang': lambda *a: 'es_ES',
        'context_tz': lambda *a: 'America/Costa_Rica',
    }
res_users()
