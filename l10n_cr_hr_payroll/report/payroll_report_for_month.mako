<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <style type="text/css">
            .account_level_1 {
                text-transform: uppercase;
                font-size: 15px;
                background-color:#F0F0F0;
            }

            .account_level_2 {
                font-size: 12px;
                background-color:#F0F0F0;
            }

            .regular_account_type {
                font-weight: normal;
            }

            .view_account_type {
                font-weight: bold;
            }

            .account_level_consol {
                font-weight: normal;
                font-style: italic;
            }

            ${css}

            .list_table .act_as_row {
                margin-top: 10px;
                margin-bottom: 10px;
                font-size:10px;
            }
        </style>
    </head>
    <body class = "data">

        
        <div style="font-size: 20px; font-weight: bold; text-align: center;"> ${company.partner_id.name}</div>
        <div style="font-size: 25px; font-weight: bold; text-align: center;"> ${_('Payroll Report for Specific Dates')}</div>
        <div style="font-size: 16px; font-weight: bold; text-align: center;">${_('Payslips of:')} ${start_date} ${_('to')} ${end_date}</div>
        
        <%
        payslips_by_struct = get_payslips_by_struct(cr, uid, start_date, end_date)

        total_hn = 0.0
        total_he = 0.0
        total_basic = 0.0
        total_exs = 0.0
        total_gross = 0.0
        total_basic = 0.0
        total_rent = 0.0
        total_ccss = 0.0
        total_net = 0.0
        total_emp = 0
        %>

        %for struct in payslips_by_struct:
            <%
            total_hn_struct = 0.0
            total_he_struct = 0.0
            total_exs_struct = 0.0
            total_gross_struct = 0.0
            total_basic_struct = 0.0
            total_rent_struct = 0.0
            total_ccss_struct = 0.0
            total_net_struct = 0.0
            total_emp_struct = 0

            %>
            
            <div class="account_title bg" style="margin-top: 20px; font-size: 12px; width: 1080px;">${struct[0]}</div>
            <div class="act_as_table list_table">
                <div class="act_as_thead">
                    <div class="act_as_row labels" style="font-weight: bold; font-size: 11x;">
                        <div class="act_as_cell first_column" style="width: 85px;  vertical-align: middle">${_('Id card')}</div>
                        <div class="act_as_cell" style="width: 230px;  vertical-align: middle">${_('Name')}</div>
                        <div class="act_as_cell" style="width: 85px;  vertical-align: middle">${_('Bank account')}</div>
                        <div class="act_as_cell amount" style="width: 40px;">${_('Hrs.')}<br />${_('Nor')}</div>
                        <div class="act_as_cell amount" style="width: 40px;">${_('Hrs.')}<br />${_('Ext')}</div>
                        <div class="act_as_cell amount">${_('Ingr.')}<br />${_('Normal')}</div>
                        <div class="act_as_cell amount">${_('Ingr.')}<br />${_('Extra')}</div>
                        <div class="act_as_cell amount">${_('Salary')}<br />${_('Gross')}</div>
                        <div class="act_as_cell amount">${_('Deducc.')}<br />${_('CCSS/BP')}</div>
                        <div class="act_as_cell amount">${_('Tax')}<br />${_('Rent')}</div>
                        <div class="act_as_cell amount">${_('Salary')}<br />${_('Net')}</div>
                    </div>
                </div>
            
            
                <%
                payslips_by_employee = get_payslips_by_employee(cr, uid, struct[1])
                %>
            
                <div class="act_as_tbody">       
                %for payslips in payslips_by_employee:
                    <div class="act_as_row lines">
                        ## Id card
                        <div class="act_as_cell first_column" style="width: 85px;">${get_identification(cr, uid, payslips[1]) or ' '}</div>
                        ## name
                        <div class="act_as_cell">${payslips[0] or ' '}</div>
                        ## bank account
                        <div class="act_as_cell">${get_bank_account(cr, uid, payslips[1]) or ' '}</div>
                        ## hn
                        <div class="act_as_cell amount">${get_hn(cr, uid, payslips[1]) or '0'}</div>
                        ## he
                        <div class="act_as_cell amount">${get_he(cr, uid, payslips[1]) or '0'}</div>
                        ## basic
                        <div class="act_as_cell amount">${formatLang(get_basic(cr, uid, payslips[1])) or '0'}</div>
                        ## exs
                        <div class="act_as_cell amount">${formatLang(get_exs(cr, uid, payslips[1])) or '0'}</div>
                        ## gross
                        <div class="act_as_cell amount ">${formatLang(get_gross(cr, uid, payslips[1])) or '0'}</div>
                        ## ccss
                        <div class="act_as_cell amount">${formatLang(get_ccss(cr, uid, payslips[1])) or '0'}</div>
                        ## RENT
                        <div class="act_as_cell amount">${formatLang(get_rent(cr, uid, payslips[1])) or '0'}</div>
                        ## NET
                        <div class="act_as_cell amount">${formatLang(get_net(cr, uid, payslips[1])) or '0'}</div>
                        <%
                        ## Totals by Departament
                        total_hn_struct += get_hn(cr, uid, payslips[1])
                        total_he_struct += get_he(cr, uid, payslips[1])
                        total_basic_struct += get_basic(cr, uid, payslips[1])
                        total_exs_struct += get_exs(cr, uid, payslips[1])
                        total_gross_struct += get_gross(cr, uid, payslips[1])
                        total_rent_struct += get_rent(cr, uid, payslips[1])
                        total_ccss_struct += get_ccss(cr, uid, payslips[1])
                        total_net_struct += get_net(cr, uid, payslips[1])
                        total_emp_struct += 1

                        ## Totals
                        total_hn += get_hn(cr, uid, payslips[1])
                        total_he += get_he(cr, uid, payslips[1])
                        total_basic += get_basic(cr, uid, payslips[1])
                        total_exs += get_exs(cr, uid, payslips[1])
                        total_gross += get_gross(cr, uid, payslips[1])
                        total_rent += get_rent(cr, uid, payslips[1])
                        total_ccss += get_ccss(cr, uid, payslips[1])
                        total_net += get_net(cr, uid, payslips[1])
                        total_emp += 1
                        %>
                    </div>
                %endfor
                </div>
                <div class="act_as_tfoot">
                    <div class="act_as_row labels"  style="font-weight: bold; font-size: 11x">
                        <div class="act_as_cell first_column">${_('Total')}</div>
                        <div class="act_as_cell">${total_emp_struct} ${_('Employees')}</div>
                        <div class="act_as_cell"> </div>
                        <div class="act_as_cell amount">${total_hn_struct}</div>
                        <div class="act_as_cell amount">${total_he_struct}</div>
                        <div class="act_as_cell amount">${formatLang(total_basic_struct)}</div>
                        <div class="act_as_cell amount">${formatLang(total_exs_struct)}</div>
                        <div class="act_as_cell amount">${formatLang(total_gross_struct)}</div>
                        <div class="act_as_cell amount">${formatLang(total_ccss_struct)}</div>
                        <div class="act_as_cell amount">${formatLang(total_rent_struct)}</div>
                        <div class="act_as_cell amount">${formatLang(total_net_struct)}</div>
                    </div>
                </div>
            </div>
        %endfor
        <div class="act_as_table list_table " style="margin-top: 20px;">
            <div class="act_as_tfoot">
                <div class="act_as_row labels"  style="font-weight: bold; font-size: 11px;">
                    <div class="act_as_cell first_column" style="width: 85px; font-size: 12px; text-align: left">${_('TOTAL')}</div>
                    <div class="act_as_cell" style="width: 230px;">${total_emp} ${_('Employees')}</div>
                    <div class="act_as_cell"> </div>
                    <div class="act_as_cell amount" style="width: 40px;">${total_hn}</div>
                    <div class="act_as_cell amount" style="width: 40px;">${total_he}</div>
                    <div class="act_as_cell amount">${formatLang(total_basic)}</div>
                    <div class="act_as_cell amount">${formatLang(total_exs)}</div>
                    <div class="act_as_cell amount">${formatLang(total_gross)}</div>
                    <div class="act_as_cell amount">${formatLang(total_ccss)}</div>
                    <div class="act_as_cell amount">${formatLang(total_rent)}</div>
                    <div class="act_as_cell amount">${formatLang(total_net)}</div>
                </div>
            </div>
        </div>
        <div class="act_as_table data_table" style="margin-top:30px">
            <div class="act_as_tbody">
                <div class="act_as_row" style="vertical-align: bottom">
                    <div class="act_as_cell" style="padding-top:80px;padding-bottom:5px"> ${_('BY:')} </div>
                    <div class="act_as_cell" style="padding-top:80px;padding-bottom:5px"> ${_('REVIEWED BY:')} </div>
                    <div class="act_as_cell" style="padding-top:80px;padding-bottom:5px"> ${_('APPROVED BY:')} </div>
                </div>
            </div>
        </div>   
        <p style="page-break-after:always"></p>
    </body>
</html>
