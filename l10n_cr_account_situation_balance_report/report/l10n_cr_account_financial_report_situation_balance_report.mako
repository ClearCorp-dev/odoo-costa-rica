<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <link rel='stylesheet' href='addons/report_webkit_lib/webkit_headers/main.css' />
        <style>
            ${css}
        </style>
    </head>
    <body class="data">
        <%setLang(user.lang)%>
        <%
            balance_data = get_data(cr, uid, data)
        %>
        <div class="table header">
            <div class="table-row">
                <div class="table-cell logo">${helper.embed_logo_by_name('default_logo', height=80)|n}</div>
                <div class="table-cell text">
                    <p class="company">${get_fiscal_year(data).company_id.partner_id.name}</p>
                    <p class="title">${_('Situation Balance at ')}${formatLang(get_start_period(data).date_stop, date=True)}</p>
                    <p class="subtitle">&nbsp;</p>
                </div>
            </div>
        </div>
        <br/><br/>
        <div class="table list">
            <div class="table-header">
                <div class="table-row labels no-wrap">
                    <div class="table-cell first-column" style="width: 70px">${_('Account<br />Code')}</div>
                    <div class="table-cell" style="width: 650px">${_('Account<br />Name')}</div>
                    <div class="table-cell" style="width: 100px">${_('Fiscal Year Opening')}<br />${get_fiscal_year(data).name}</div>
                    <div class="table-cell" style="width: 100px">${_('Selected period')}<br />${get_start_period(data).name}</div>\
                    <div class="table-cell" style="width: 100px">${_('Variation')}<br />${_('Per. vs. FY Open.')}</div>
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
                                <div class="table-cell amount">${formatLang(account['total_fiscal_year'])}</div>         
                                <div class="table-cell amount">${formatLang(account['total_period'])}</div>
                                <div class="table-cell amount" >${formatLang(account['total_variation'])}</div>
                                <div class="table-cell amount" >${formatLang(account['total_percent_variation'])}</div>
                           %else:
                                <div class="table-cell amount">${account['total_fiscal_year']}</div>         
                                <div class="table-cell amount">${account['total_period']}</div>
                                <div class="table-cell amount" >${account['total_variation']}</div>
                                <div class="table-cell amount" >${account['total_percent_variation']}</div>
                        
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
           signatures = get_signatures_report(cr, uid, 'Situation Balance Report')
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
