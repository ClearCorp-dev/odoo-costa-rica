<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <link rel='stylesheet' href='addons/account_webkit_report_library/webkit_headers/main.css' />
        <style>
            ${css}
        </style>
    </head>
    <body class="data">
        <%setLang(user.lang)%>
        <%
            last_period = get_last_period(cr, uid, data)
            balance_data = get_data(cr, uid, data)
            fiscalyear = get_fiscal_year(data)  
        %>
        <div class="table header">
            <div class="table-row">
                <div class="table-cell logo">${helper.embed_logo_by_name('default_logo', height=80)|n}</div>
                <div class="table-cell text">
                    <p class="company">${fiscalyear.company_id.partner_id.name}</p>
                    <p class="title">${_('Statement Changes of Equity')}</p>
                    <p class="subtitle">${_('Fiscal Year:')} ${fiscalyear.name} - ${_('Until Period:')} ${get_start_period(data).name}</p>
                </div>
            </div>
        </div>
        <br/><br/>
        <div class="table list">
            <div class="table-header">
                <div class="table-row labels no-wrap">
                    <div class="table-cell first-column" style="width: 70px">${_('Account<br />Code')}</div>
                    <div class="table-cell" style="width: 430px">${_('Account<br />Name')}</div>
                    <div class="table-cell" style="width: 100px">${_('Previous period')}<br />${last_period.name}</div>
                    <div class="table-cell" style="width: 100px">${_('Selected period')}<br />${get_start_period(data).name}</div>
                    <div class="table-cell" style="width: 100px">${_('Variation')}<br />${_('Prev. vs Sel.')}</div>
                    <div class="table-cell last-column" style="width: 40px">${_('Var.')}<br />${_('%')}</div>
                </div>
            </div>
            <div class="table-body">
                 <% row_even = False %>
                 %for account in balance_data:
                     %if account['level'] == 0 or account['is_parent'] == 'True' :
                        <div class="table-row bold ${row_even and 'even' or 'odd'}">
                     %elif 'child' in account:
                        <div class="table-row bold ${row_even and 'even' or 'odd'}">
                     %else:
                        <div class="table-row ${row_even and 'even' or 'odd'}">
                    %endif             
                            <div class="table-cell first-column">${account['code']}</div>
                            <div class="table-cell" style="padding-left:${account['level']*10}px" >${account['name']}</div>
                            %if account['is_parent'] == False:
                                <div class="table-cell amount">${formatLang(account['balance_total_last_period'])}</div>         
                                <div class="table-cell amount" >${formatLang(account['balance_total_period'])}</div>
                                <div class="table-cell amount" >${formatLang(account['balance_total_variation'])}</div>
                                <div class="table-cell amount" >${formatLang(account['balance_total_percentage_variation'])}</div>
                           %else:
                                <div class="table-cell amount">${account['balance_total_last_period']}</div>         
                                <div class="table-cell amount" >${account['balance_total_period']}</div>
                                <div class="table-cell amount" >${account['balance_total_variation']}</div>
                                <div class="table-cell amount" >${account['balance_total_percentage_variation']}</div>                  
                           %endif
                                
                    <%
                        if row_even:
                            row_even = False
                        else:
                            row_even = True
                    %>
                    </div>
                %endfor
            </div>
        </div>
       <div class="table-row spacer">
            <div class="table-cell">&nbsp;</div>
        </div>
        <% 
           signatures = get_signatures_report(cr, uid, 'Profit Statement')
           cont = 0
        %>
        %if len(signatures) > 0:
            <div class="table header">
                <div class="table-row">
                    <div class="table-cell text">
                        <p class="title">${_('Authorized by: ')}</p>
                    </div>
                </div>
           </div>
           <br/><br/>
           <div class="table header">
                <div class="table-row">
                    <div class="table-cell text">
                    %for user_sign in signatures:
                        <div class="table-cell text">_________________________________________________________<br/>
                                                        <p class="subtitle">${user_sign.name}</p>
                                                        <p class="company"><i>${user_sign.job_id.name or ''}</i></p>
                        </div>
                        <br/><br/><br/>
                    </div>
                    %endfor                
                </div>
            </div>
        %endif
        <p style="page-break-after:always"></p>
    </body>
</html>
