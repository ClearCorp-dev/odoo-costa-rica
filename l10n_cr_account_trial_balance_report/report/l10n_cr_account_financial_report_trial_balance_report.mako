<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <link rel='stylesheet' href='addons/account_webkit_report_library/webkit_headers/main.css' />
        <style>
            ${css}
        </style>
    </head>
    <body>
        <%setLang(user.lang)%>
        <%
            fiscalyear = get_fiscal_year(data)    
        %>
         <div class="table header">
            <div class="table-row">
                <div class="table-cell logo">${helper.embed_logo_by_name('internal_reports_logo', height=80)|n}</div>
                <div class="table-cell text">
                    <p class="company">${fiscalyear.company_id.name}</p>
                    <p class="title">${_('Trial Balance Report')}</p>
                </div>
            </div>
        </div>
       <div class="table list">
            <div class="table-header">
                <div class="table-row labels no-wrap">
                    <div class="table-cell first-column" style="width: 70px">${_('Chart of Accounts: ')}<br/>${get_chart_account_id(data).name}</div>
                    <div class="table-cell first-column" style="width: 70px">${_('Fiscal Year')}<br/>${get_fiscal_year(data).name}</div>
                    <div class="table-cell first-column" style="width: 70px">
                        %if filter_form(data) == 'filter_date':
                            ${_('Dates Filter')}
                        %elif filter_form(data) == 'filter_period':
                            ${_('Periods Filter')}
                        %else:
                            ${_('No filters')}
                        %endif
                    <br/>
                    %if filter_form(data) != 'filter_no':
                        ${_('From:')}
                            %if filter_form(data) == 'filter_date':
                                ${formatLang(get_date_from(data), date=True)}
                            %else:
                                ${get_start_period(data).name}
                            %endif
                            ${_('To:')}
                            %if filter_form(data) == 'filter_date':
                                ${ formatLang(get_date_to(data), date=True)}
                            %else:
                                ${get_end_period(data).name}
                            %endif
                    %endif
                    </div>
                    <div class="table-cell first-column" style="width: 70px">${_('Accounts Filter')}<br/>${ get_chart_account_id(data).name }</div>
                    <div class="table-cell first-column" style="width: 70px">${_('Target Moves')}<br/>${ display_target_move(data) }</div>
                </div>
            </div>          
        </div>
        <br/><br/>
        <div class="table list">
            <div class="table-header">
                <div class="table-row labels no-wrap">
                    <div class="table-cell first-column" style="width: 100px">${_('Code')}</div>
                    <div class="table-cell" style="width: 300px">${_('Name')}</div>
                    <div class="table-cell" style="width: 100px">${_('Initial balance')}</div>
                    <div class="table-cell" style="width: 100px">${_('Debit')}</div>                    
                    <div class="table-cell" style="width: 100px">${_('Credit')}</div>
                    <div class="table-cell last-column" style="width: 70px">${_('Balance')}</div>
                </div>
            </div>
            <div class="table-body"> 
                <% row_even = False %>
                <%
                  accounts = get_accounts(cr, uid, data)
                  total_result = get_data(cr, uid, data)                                
                %>
                 %for account in accounts:
                     %if account.level == 0:
                        <div class="table-row bold ${row_even and 'even' or 'odd'}">
                     %elif account.child_id:
                        <div class="table-row bold ${row_even and 'even' or 'odd'}">
                     %else:
                        <div class="table-row ${row_even and 'even' or 'odd'}">
                    %endif             
                            <div class="table-cell first-column">${account.code}</div>
                            <div class="table-cell" style="padding-left:${account.level*10}px">${account.name}</div>
                            <div class="table-cell amount">${formatLang(total_result[account.id]['initial_balance'])}</div>         
                            <div class="table-cell amount">${formatLang(total_result[account.id]['debit'])}</div>
                            <div class="table-cell amount" >${formatLang(total_result[account.id]['credit'])}</div>
                            <div class="table-cell amount" >${formatLang(total_result[account.id]['balance'])}</div>
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
           signatures = get_signatures_report(cr, uid, 'Trial Balance Report')
           cont = 0
        %>
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
        <p style="page-break-after:always"></p>
    </body>
</html>
