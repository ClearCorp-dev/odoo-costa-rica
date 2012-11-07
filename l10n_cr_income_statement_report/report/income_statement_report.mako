<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <style type="text/css">
            .overflow_ellipsis {
                text-overflow: ellipsis;
                overflow: hidden;
                white-space: nowrap;
            }
            ${css}
        </style>
    </head>
    <body class = "data">
        <%setLang(user.context_lang)%>
        <%
            last_period = get_last_period(cr, uid, start_period)
            fiscalyear = get_fiscalyear(cr, uid, start_period)
        %>
        <div style="font-size: 20px; font-weight: bold; text-align: center;"> ${company.partner_id.name}</div>
        <div style="font-size: 25px; font-weight: bold; text-align: center;"> ${_('Income Statement Report')}</div>
        <div style="font-size: 16px; font-weight: bold; text-align: center;">${_('Income Statement of:')} ${start_period.name}</div>
        <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
        <div class="act_as_table data_table">
            <div class="act_as_thead" style="vertical-align: right;">
                <div class="act_as_row labels" style="font-weight: bold; font-size: 11x; vertical-align: right;">
                    <div class="act_as_cell first_column" style="width: 200px;  vertical-align: right; align:right;">${_('Name')}</div>
                    <div class="act_as_cell first_column" style="width: 100px;  vertical-align: right; align:right;">${start_period.name}</div>
                    <div class="act_as_cell first_column" style="width: 100px;  vertical-align: right; align:right;">${_('%')}</div>
                    <div class="act_as_cell first_column" style="width: 100px;  vertical-align: right; align:right;">${last_period.name}</div>
                    <div class="act_as_cell first_column" style="width: 100px;  vertical-align: right; align:right;">${_('%')}</div>
                    <div class="act_as_cell first_column" style="width: 100px;  vertical-align: right; align:right;">${fiscalyear.name}</div>
                    <div class="act_as_cell first_column" style="width: 100px;  vertical-align: right; align:right;">${_('%')}</div>
                    <div class="act_as_cell first_column" style="width: 100px;  vertical-align: right; align:right;">${_('Variation')}</div>
                    <div class="act_as_cell first_column" style="width: 100px;  vertical-align: right; align:right;">${_('%')}</div>
                </div>
            </div>
            <div class="act_as_tbody">
                <% 
                    list_all = get_accounts(cr, uid)
                    
                    total_period = 0.00
                    total_percentage_period = 0.00
                    total_last_period = 0.00
                    total_percentage_last_period = 0.00
                    total_fiscalyear = 0.00
                    total_percentage_fiscalyear = 0.00
                    total_variation = 0.00
                    total_percentage_variation = 0.00
                
                    list_accounts_initial = list_all[0]
                    total_period_calculate = 0.00
                    total_last_period_calculate = 0.00
                    total_fiscalyear_calculate = 0.00
                    total_variation_calculate = 0.00
                %>
                %for account in list_accounts_initial:
                <%
                    total_period_calculate += get_balance(cr, uid, account, start_period)
                    total_last_period_calculate += get_balance(cr, uid, account, last_period)
                    total_fiscalyear_calculate += get_balance(cr, uid, account, fiscalyear)
                    #CORREGIR, QUITAR EL +1
                    total_variation_calculate += (get_balance(cr, uid, account, start_period) - get_balance(cr, uid, account, last_period)) + 1
                %>
                %endfor
                %for list_accounts in list_all:
                    <%
                        subtotal_period = 0.00
                        subtotal_percentage_period = 0.00
                        subtotal_last_period = 0.00
                        subtotal_percentage_last_period = 0.00
                        subtotal_fiscalyear = 0.00
                        subtotal_percentage_fiscalyear = 0.00
                        subtotal_variation = 0.00
                        subtotal_percentage_variation = 0.00
                    %>
                    <% sub_total_name = list_accounts[0].name %>
                    %for account in list_accounts:
                        <% subtotal_name = '' %>
                        <div class="act_as_row lines">
                            %if account.level > 0:
                                <div class="act_as_cell" style="padding-left:${account.level*10}px">
                                    %if account.child_id:
                                        <div class="act_as_row " ><b>${_(account.name)}</b></div>
                                    %else:
                                        <div class="act_as_row " >${_(account.name)}</div>
                                    %endif
                                </div>
                            %else:
                                <div class="act_as_cell " ><b>${_(account.name)}</b></div>
                            %endif
                            <div class="act_as_cell amount" >${formatLang(get_balance(cr, uid, account, start_period))}</div>
                            <div class="act_as_cell amount" >${formatLang((get_balance(cr, uid, account, start_period) * 100) / total_period_calculate)}</div>
                            <div class="act_as_cell amount" >${formatLang(get_balance(cr, uid, account, last_period))}</div>
                            <div class="act_as_cell amount" >${formatLang((get_balance(cr, uid, account, last_period) * 100) / total_last_period_calculate)}</div>
                            <div class="act_as_cell amount" >${formatLang(get_balance(cr, uid, account, fiscalyear))}</div>
                            <div class="act_as_cell amount" >${formatLang((get_balance(cr, uid, account, fiscalyear) * 100) / total_fiscalyear_calculate)}</div>
                            <div class="act_as_cell amount" >${formatLang((get_balance(cr, uid, account, start_period) - get_balance(cr, uid, account, last_period)))}</div>
                            <div class="act_as_cell amount" >${formatLang(((get_balance(cr, uid, account, start_period) - get_balance(cr, uid, account, last_period)) * 100) / total_variation_calculate)}</div>
                        </div>
                        <%
                            subtotal_period += get_balance(cr, uid, account, start_period)
                            subtotal_percentage_period += (get_balance(cr, uid, account, start_period) * 100) / total_period_calculate
                            subtotal_last_period += get_balance(cr, uid, account, last_period)
                            subtotal_percentage_last_period += (get_balance(cr, uid, account, last_period) * 100) / total_last_period_calculate
                            subtotal_fiscalyear += get_balance(cr, uid, account, fiscalyear)
                            subtotal_percentage_fiscalyear += (get_balance(cr, uid, account, fiscalyear) * 100) / total_fiscalyear_calculate
                            subtotal_variation += get_balance(cr, uid, account, start_period) - get_balance(cr, uid, account, last_period)
                            subtotal_percentage_variation += ((get_balance(cr, uid, account, start_period) - get_balance(cr, uid, account, last_period)) * 100) / total_variation_calculate
                        %>
                    %endfor
                    <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
                    <div class="act_as_row lines" style="font-weight: bold; font-size: 12px;">
                        <div class="act_as_cell" style="padding-left:0px">
                            <div class="act_as_row " ><b>${_('TOTAL')} ${sub_total_name}</b></div>
                        </div>
                        <div class="act_as_cell amount" >${formatLang(subtotal_period)}</div>
                        <div class="act_as_cell amount" >${formatLang(subtotal_percentage_period)}</div>
                        <div class="act_as_cell amount" >${formatLang(subtotal_last_period)}</div>
                        <div class="act_as_cell amount" >${formatLang(subtotal_percentage_last_period)}</div>
                        <div class="act_as_cell amount" >${formatLang(subtotal_fiscalyear)}</div>
                        <div class="act_as_cell amount" >${formatLang(subtotal_percentage_fiscalyear)}</div>
                        <div class="act_as_cell amount" >${formatLang(subtotal_variation)}</div>
                        <div class="act_as_cell amount" >${formatLang(subtotal_percentage_variation)}</div>
                    </div>
                    <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
                    <%
                        total_period += subtotal_period
                        total_percentage_period += subtotal_percentage_period
                        total_last_period += subtotal_last_period
                        total_percentage_last_period += subtotal_percentage_last_period
                        total_fiscalyear += subtotal_fiscalyear
                        total_percentage_fiscalyear += subtotal_percentage_fiscalyear
                        total_variation += subtotal_variation
                        total_percentage_variation += subtotal_percentage_variation
                    %>
                %endfor
                <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
                <div class="act_as_row lines" style="font-weight: bold; font-size: 13px;">
                    <div class="act_as_cell" style="padding-left:0px">
                        <div class="act_as_row " ><b>${_('TOTAL')}</b></div>
                    </div>
                    <div class="act_as_cell amount" >${formatLang(total_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(total_percentage_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(total_last_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(total_percentage_last_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(total_fiscalyear)}</div>
                    <div class="act_as_cell amount" >${formatLang(total_percentage_fiscalyear)}</div>
                    <div class="act_as_cell amount" >${formatLang(total_variation)}</div>
                    <div class="act_as_cell amount" >${formatLang(total_percentage_variation)}</div>
                </div>
                <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
            </div>
        </div>
        <p style="page-break-after:always"></p>
    </body>
</html>
