# -*- encoding: utf-8 -*-
##############################################################################
#
#
#    payment_receipt
#    First author: Mag Guevara <mag.guevara@clearcorp.co.cr> (ClearCorp S.A.)
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

import time
import pooler
from report import report_sxw
from amount_to_text import number_to_text_es
import locale

class hr_payslip_run_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(hr_payslip_run_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr' : cr,
            'uid': uid,
            'get_text':self.get_text,
            'get_hn':self.get_hn,
            'get_he':self.get_he,
            'get_fe':self.get_fe,
            'get_basic':self.get_basic,
            'get_exs':self.get_exs,
            'get_fes':self.get_fes,
            'get_gross':self.get_gross,
            'get_ccss':self.get_ccss,
            'get_net':self.get_net,
	    'get_rent':self.get_rent,
        })
    
    def get_prefix(self,currency,company_id):
        separator = ','
        decimal_point = '.'
        res = ''
        name_currency = currency.currency_name
        if name_currency == False:
            name_currency = company_id.currency_id.currency_name
            res = company_id.currency_id.symbol_prefix
        if name_currency == None:
            name_currency = company_id.currency_id.currency_name
            res = company_id.currency_id.symbol_prefix
        
        
        return res
        
    def get_hn(self,line_ids):
        code = 'HN'
        res = 0
        for line in line_ids:
            if line.code == code:
                res += line.number_of_hours
                
        return res
        
    def get_he(self,line_ids):
        code = 'HE'
        res = 0
        for line in line_ids:
            if line.code == code:
                res += line.number_of_hours        
        
        return res
        
        
    def get_fe(self,line_ids):
        code = 'FE'
        res = 0
        for line in line_ids:
            if line.code == code:
                res += line.number_of_hours        
        
        return res
    
    def get_basic(self,line_ids):
        code = 'BASIC'
        res = 0
        for line in line_ids:
            if line.code == code:
                res += line.total
        
        return res
        
    def get_exs(self,line_ids):
        code = 'EXS'
        res = 0
        for line in line_ids:
            if line.code == code:
                res += line.total
        
        
        return res
    
    
    def get_fes(self,line_ids):
        code = 'FES'
        res = 0
        for line in line_ids:
            if line.code == code:
                res += line.total
        
        
        return res
        
        
    def get_gross(self,line_ids):
        code = 'GROSS'
        res = 0
        for line in line_ids:
            if line.code == code:
                res += line.total
        
        
        return res
    
    def get_ccss(self,line_ids):
        code = 'CCSS-EMP'
        code2 = 'Banco Popular-EMP'
        res = 0
        for line in line_ids:
            if line.code == code:
                res += line.total
            elif line.code == code2:
                res += line.total
        
        return res
    
    
    def get_net(self,line_ids):
        code = 'NET'
        res = 0
        for line in line_ids:
            if line.code == code:
                res += line.total
            
        
        return round(res)


    def get_rent(self,line_ids):
        code = 'Renta'
        res = 0
        for line in line_ids:
            if line.code == code:
                res += line.total
        
        
        return res
    
    def get_text(self,amount,currency,lang,company_id):
        separator = ','
        decimal_point = '.'
        name_currency = currency.currency_name
        if name_currency == False:
            name_currency = company_id.currency_id.currency_name
        if name_currency == None:
            name_currency = company_id.currency_id.currency_name
        if lang:
            lang_pool = self.pool.get('res.lang')
            id_lang = lang_pool.search(self.cr,self.uid,[('code','=',lang)])
            obj_lang = lang_pool.browse(self.cr,self.uid,id_lang)[0]
            separator = obj_lang  and obj_lang.thousands_sep or separator
            decimal_point = obj_lang  and obj_lang.decimal_point or decimal_point
        res = number_to_text_es(amount,name_currency,separator=separator,decimal_point=decimal_point)
        return res
        
report_sxw.report_sxw(
    'report.hr.payslip.run.layout_ccorp',
    'hr.payslip.run',
    'addons/cr_hr_report/report/payment_receipt.mako',
    parser=hr_payslip_run_report)
