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
    <body>
        <%!
        def amount(text):
            return text.replace('-', '&#8209;')  # replace by a non-breaking hyphen (it will not word-wrap between hyphen and numbers)
        %>

        <%setLang(user.context_lang)%>

        <%
        initial_balance_text = {'initial_balance': _('Computed'), 'opening_balance': _('Opening Entries'), False: _('No')}
        filter_type = ''
        filter_data = []
        t_m = target_move(data) 
        %>

        <div class="act_as_table data_table">
            <div class="act_as_row labels" style="font-weight: bold;">
                <div class="act_as_cell">${_('Chart of Account')}</div>
                <div class="act_as_cell">${_('Fiscal Year')}</div>
                <div class="act_as_cell">
                    %if filter_form(data) == 'filter_date':
                        ${_('Dates Filter')}
                    %else:
                        ${_('Periods Filter')}
                    %endif
                </div>
                <div class="act_as_cell">${_('Accounts Filter')}</div>
                <div class="act_as_cell">${_('Target Moves')}</div>
                <div class="act_as_cell">${_('Initial Balance')}</div>
            </div>
            <div class="act_as_row">
                <div class="act_as_cell">${ chart_account.name }</div>
                <div class="act_as_cell">${ fiscalyear.name if fiscalyear else '-' }</div>
                <div class="act_as_cell">
                    ${_('From:')}
                    %if filter_form(data) == 'filter_date':
                        ${formatLang(start_date, date=True) if start_date else u'' }
                        <% 
                            filter_data.append(start_date) 
                            filter_type = 'filter_date'
                        %>
                    %elif filter_form(data) == 'filter_period':
                        ${start_period.name if start_period else u''}
                        <% 
                            filter_data.append(start_period) 
                            filter_type = 'filter_period'
                        %>
                    %endif
                    ${_('To:')}
                    %if filter_form(data) == 'filter_date':
                        ${ formatLang(stop_date, date=True) if stop_date else u'' }
                        <% filter_data.append(stop_date) %>
                    %elif filter_form(data) == 'filter_period':
                        ${stop_period.name if stop_period else u'' }
                        <% filter_data.append(stop_period) %>
                    %endif
                </div>
                <div class="act_as_cell">${ display_target_move(data) }</div>
                <div class="act_as_cell">${ initial_balance_text[initial_balance_mode] }</div>
            </div>
        </div>

            <%
            last_child_consol_ids = []
            last_level = False
            
            bank_accounts = get_bank_accounts(cr, uid)
            accounts_currency = accounts_by_currency(cr, uid, bank_accounts)

            %>
            %for currency, accounts in accounts_currency.iteritems():
                <div class="account_title bg" style="margin-top: 20px; font-size: 12px; width: 700px;">${_('Account Bank Balance in ')} ${currency}</div>
                <div class="act_as_table list_table" style="margin-top: 10px;">
                <div class="act_as_thead">
                    <div class="act_as_row labels" style="font-weight: bold;">
                        ## code
                        <div class="act_as_cell first_column" style="width: 40px;">${_('Code')}</div>
                        ## account name
                        <div class="act_as_cell" style="width: 80px;">${_('Account')}</div>
                        ## initial balance
                        <div class="act_as_cell amount" style="width: 50px;">${_('Initial Balance')}</div>
                        ## TEFS
                        <div class="act_as_cell amount" style="width: 50px;">${_('Transfers')}</div>
                        ## Checks
                        <div class="act_as_cell amount" style="width: 50px;">${_('Checks')}</div>
                        ## Deposit
                        <div class="act_as_cell amount" style="width: 50px;">${_('Deposit')}</div>
                        ## debit
                        <div class="act_as_cell amount" style="width: 50px;">${_('Debit')}</div>
                        ## credit
                        <div class="act_as_cell amount" style="width: 50px;">${_('Credit')}</div>
                        ## balance
                        <div class="act_as_cell amount" style="width: 50px;">${_('Balance')}</div>                        
                    </div>
                </div>                  
                
                <div class="act_as_tbody">
                    %for account in sorted(set(accounts)):
                        <%
                            if account.id in last_child_consol_ids:
                                # current account is a consolidation child of the last account: use the level of last account
                                level = last_level
                                level_class = "account_level_consol"
                            else:
                                # current account is a not a consolidation child: use its own level
                                level = account.level or 0
                                level_class = "account_level_%s" % (level,)
                                last_child_consol_ids = [child_consol_id.id for child_consol_id in account.child_consol_ids]
                                last_level = account.level 
                        %>
                        <%
                            move_lines = get_move_lines_account(cr, uid, account.id,filter_type,filter_data,fiscalyear,t_m)
                            total_result = get_total_move_lines(cr, uid, move_lines, currency)
                        %>
                        <div class="act_as_row lines ${level_class} ${"%s_account_type" % (account.type,)}">
                            ## code
                            <div class="act_as_cell first_column">${account.code}</div>
                            ## account name
                            <div class="act_as_cell">${account.name}</div>
                            ##initial balance
                            <div class="act_as_cell amount">${formatLang(0.0)}</div>
                            ##transfer
                            <div class="act_as_cell amount">${total_result['amount_transf']}</div>
                            ##check
                            <div class="act_as_cell amount">${total_result['amount_check']}</div>
                            ##deposit
                            <div class="act_as_cell amount">${total_result['amount_deposit']}</div>
                            ##debit
                            <div class="act_as_cell amount">${total_result['amount_debit']}</div>
                            ##credit
                            <div class="act_as_cell amount">${total_result['amount_credit']}</div> 
                            ##balance
                            <div class="act_as_cell amount">${formatLang(0.0)}</div>
                       </div>
                    %endfor
                </div>
            </div>        
         %endfor        
    </body>
</html>
