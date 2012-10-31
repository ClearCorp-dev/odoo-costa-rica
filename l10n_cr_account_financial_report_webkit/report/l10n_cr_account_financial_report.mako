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
<body>
    <div style="font-size: 25px; font-weight: bold; text-align: center; align=center;">${ data['form']['account_report_id'][1] }</div>
    <div class="act_as_table data_table">
        <div class="act_as_row labels">
            <div class="act_as_cell">${_('Chart of Account')}</div>
            <div class="act_as_cell">${_('Fiscal Year')}</div>
            <div class="act_as_cell">
                %if filter_form(data) == 'filter_date':
                    ${_('Dates Filter')}
                %elif filter_form(data) == 'filter_period':
                    ${_('Periods Filter')}
                %else:
                    ${_('None Filter')}
                %endif
            </div>
        </div>
        <div class="act_as_row">
            <div class="act_as_cell">${ get_account(data) }</div>
            <div class="act_as_cell">${ get_fiscalyear(data) if get_fiscalyear(data) else '-' }</div>
            <div class="act_as_cell">
                %if filter_form(data) == 'filter_date':
                    ${_('From:')}
                    ${formatLang(get_start_date(data), date=True) if get_start_date(data) else u'' }
                %elif filter_form(data) == 'filter_period':
                    ${_('From:')}
                    ${ get_start_period(data) if  get_start_period(data) else u''}
                %else:
                    ${ '-' }
                %endif
                
                %if filter_form(data) == 'filter_date':
                    ${_('To:')}
                    ${ formatLang(get_end_date(data), date=True) if get_end_date(data) else u'' }
                %elif filter_form(data) == 'filter_period':
                    ${_('To:')}
                    ${get_end_period(data) if get_end_period(data) else u'' }
                %endif
            </div>
        </div>
    </div>
    <%
    get_lines_report = get_lines(data)
    %>
    <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>      
    <div class="act_as_table list_table">
        <div class="act_as_thead" style="vertical-align: right;">
            <div class="act_as_row labels" style="font-weight: bold; font-size: 11x; vertical-align: right;">
                %if data['form']['debit_credit'] == 1: 
                    <div class="act_as_cell first_column" style="width: 200px;  vertical-align: right; align:right;">${_('Name')}</div>                
                    <div class="act_as_cell amount" style="width: 100px;  vertical-align: right; align:right;">${_('Debit')}</div>
                    <div class="act_as_cell amount" style="width: 100px;  vertical-align: right; align:right;">${_('Credit')}</div>
                    <div class="act_as_cell amount" style="width: 100px;  vertical-align: right; align:right;">${_('Balance')}</div>
                %endif
                %if not data['form']['enable_filter'] and not data['form']['debit_credit']:
                    <div class="act_as_cell first_column" style="width: 200px;  vertical-align: right; align:right;">${_('Name')}</div>  
                    <div class="act_as_cell amount" style="width: 100px;  vertical-align: right; align:right;">${_('Balance')}</div>
                %endif
                %if data['form']['enable_filter'] == 1 and not data['form']['debit_credit']:
                    <div class="act_as_cell first_column" style="width: 200px;  vertical-align: right; align:right;">${_('Name')}</div>  
                    <div class="act_as_cell amount" style="width: 100px;  vertical-align: right; align:right;">${_('Balance')}</div>
                    <div class="act_as_cell amount" style="width: 100px;  vertical-align: right; align:right;">${_(data['form']['label_filter'])}</div>
                %endif
            </div>
        </div>        
        <div class="act_as_tbody">
            %for line in get_lines_report:
                %if ((line['type'] == 'account' and line['account_type'] == 'account') or line['type'] == 'report'):
                    <%bold = True%>
                %else:
                    <%bold = False%>
                %endif
            <div class="act_as_row lines"> 
                %if data['form']['debit_credit'] == 1:
                    %if line['level'] > 0:
                        <div class="act_as_cell" style="padding-left:${line['level']*10}px">
                        %if bold: 
                            <div class="act_as_cell" ><b>${line['name']}</b></div>
                        %else:
                            <div class="act_as_cell" >${line['name']}</div>
                        %endif
                        </div>
                        <div class="act_as_cell amount" >${line['debit']}</div>
                        <div class="act_as_cell amount" >${line['credit']}</div>
                        <div class="act_as_cell amount" >${line['balance']}</div>                         
                    %else:                         
                        %if bold: 
                            <div class="act_as_cell" ><b>${line['name']}</b></div>
                        %else:
                            <div class="act_as_cell" >${line['name']}</div>
                        %endif
                        <div class="act_as_cell amount" >${line['debit']}</div>
                        <div class="act_as_cell amount" >${line['credit']}</div>
                        <div class="act_as_cell amount" >${line['balance']}</div>  
                    %endif
                %endif
                %if not data['form']['enable_filter'] and not data['form']['debit_credit']:
                    %if line['level'] > 0: 
                        <div class="act_as_cell" style="padding-left:${line['level']*10}px">
                            %if bold: 
                                <div class="act_as_cell" ><b>${line['name']}</b></div>
                            %else:
                                <div class="act_as_cell" >${line['name']}</div>
                            %endif
                        </div>
                        <div class="act_as_cell amount" >${line['balance']}</div>
                    %else:
                        %if bold: 
                            <div class="act_as_cell" ><b>${line['name']}</b></div>
                        %else:
                            <div class="act_as_cell" >${line['name']}</div>
                        %endif
                        <div class="act_as_cell amount" >${line['balance']}</div>
                    %endif
                %endif
                %if data['form']['enable_filter'] == 1 and not data['form']['debit_credit']:
                    %if line['level'] > 0:
                        <div class="act_as_cell" style="padding-left:${line['level']*10}px">
                            %if bold: 
                                <div class="act_as_cell" ><b>${line['name']}</b></div>
                            %else:
                                <div class="act_as_cell" >${line['name']}</div>
                            %endif
                        </div>
                        <div class="act_as_cell amount" >${line['balance']}</div>                            
                        <div class="act_as_cell amount" >${line['balance_cmp']}</div>   
                    %else:
                        %if bold: 
                            <div class="act_as_cell" ><b>${line['name']}</b></div>
                        %else:
                            <div class="act_as_cell">${line['name']}</div>
                        %endif
                        <div class="act_as_cell amount" >${line['balance']}</div>
                        <div class="act_as_cell amount" >${line['balance_cmp']}</div> 
                    %endif
                %endif 
            </div>
            %endfor  
        </div>
    </div>
</body>
</html>
