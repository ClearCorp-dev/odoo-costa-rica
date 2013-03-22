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
                <div class="act_as_cell">
                    %if accounts(data):
                        ${', '.join([account.code for account in accounts(data)])}
                    %else:
                        ${_('All')}
                    %endif
                </div>
                <div class="act_as_cell">${ display_target_move(data) }</div>
                <div class="act_as_cell">${ initial_balance_text[initial_balance_mode] }</div>
            </div>
        </div>

        %for index, params in enumerate(comp_params):
            <div class="act_as_table data_table">
                <div class="act_as_row">
                    <div class="act_as_cell">${_('Comparison %s') % (index + 1,)} (${"C%s" % (index + 1,)})</div>
                    <div class="act_as_cell">
                        %if params['comparison_filter'] == 'filter_date':
                            ${_('Dates Filter:')}&nbsp;${formatLang(params['start'], date=True) }&nbsp;-&nbsp;${formatLang(params['stop'], date=True) }
                        %elif params['comparison_filter'] == 'filter_period':
                            ${_('Periods Filter:')}&nbsp;${params['start'].name}&nbsp;-&nbsp;${params['stop'].name}
                        %else:
                            ${_('Fiscal Year :')}&nbsp;${params['fiscalyear'].name}
                        %endif
                    </div>
                    <div class="act_as_cell">${_('Initial Balance:')} ${ initial_balance_text[params['initial_balance_mode']] }</div>
                </div>
            </div>
        %endfor

        
            <%
            last_child_consol_ids = []
            last_level = False
            
            bank_accounts = get_bank_accounts(cr, uid, objects)
            accounts_currency = accounts_by_currency(cr, uid, bank_accounts)
            total_balance = 0.0

            %>
            %for currency in accounts_currency:
            <%
                total_tefs_curr = 0.0
                total_checks_curr = 0.0
                total_deposit_curr = 0.0
                total_debit_curr = 0.0
                total_credit_curr = 0.0
                account_balance = 0.0
                total_balance_curr = 0.0
                total_inital_balance_curr = 0.0
            %>
                %if currency[0] != 'CRC':
                    <div class="account_title bg" style="margin-top: 20px; font-size: 12px; width: 700px;">${_('Account Bank Balance in ')} ${currency[0]}</div>
                %else:
                    <div class="account_title bg" style="margin-top: 20px; font-size: 12px; width: 700px;">${_('Account Bank Balance in ')} ${company.currency_id.name}</div>
                %endif
                <div class="act_as_table list_table" style="margin-top: 10px;">
                <div class="act_as_thead">
                    <div class="act_as_row labels" style="font-weight: bold;">
                        ## code
                        <div class="act_as_cell first_column" style="width: 40px;">${_('Code')}</div>
                        ## account name
                        <div class="act_as_cell" style="width: 80px;">${_('Account')}</div>
                        %if comparison_mode == 'no_comparison':
                            %if initial_balance_mode:
                                ## initial balance
                                <div class="act_as_cell amount" style="width: 50px;">${_('Initial Balance')}</div>
                            %endif
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
                        %endif
                        ## balance
                        <div class="act_as_cell amount" style="width: 50px;">
                        %if comparison_mode == 'no_comparison' or not fiscalyear:
                            ${_('Balance')}
                        %else:
                            ${_('Balance %s') % (fiscalyear.name,)}
                        %endif
                        </div>
                        %if comparison_mode in ('single', 'multiple'):
                            %for index in range(nb_comparison):
                                <div class="act_as_cell amount" style="width: 50px;">
                                    %if comp_params[index]['comparison_filter'] == 'filter_year' and comp_params[index].get('fiscalyear', False):
                                        ${_('Balance %s') % (comp_params[index]['fiscalyear'].name,)}
                                    %else:
                                        ${_('Balance C%s') % (index + 1,)}
                                    %endif
                                </div>
                                %if comparison_mode == 'single':  ## no diff in multiple comparisons because it shows too data
                                    <div class="act_as_cell amount" style="width: 50px;">${_('Difference')}</div>
                                    <div class="act_as_cell amount" style="width: 50px;">${_('% Difference')}</div>
                                %endif
                            %endfor
                        %endif
                    </div>
                </div>                   
                
                <div class="act_as_tbody">
                    %for account in sorted(currency[1], key=lambda account: account.name):
                        <%
                        move_lines = get_move_lines_account(cr, uid, filter_type, filter_data, account)

                        if currency[0] != 'CRC':
                            debit = get_debit_account(cr, uid, move_lines, account.report_currency_id.name)
                            credit = get_credit_account(cr, uid, move_lines, account.report_currency_id.name)
                            deposit = get_deposit_account(cr, uid, move_lines, account.report_currency_id.name, account)
                            tefs = get_tefs_account(cr, uid, move_lines, account.report_currency_id.name, account)
                            checks = get_checks_account(cr, uid, move_lines, account.report_currency_id.name, account)
                        else:
                            debit = get_debit_account(cr, uid, move_lines, company.currency_id.name)
                            credit = get_credit_account(cr, uid, move_lines, company.currency_id.name)
                            deposit = get_deposit_account(cr, uid, move_lines, company.currency_id.name, account)
                            tefs = get_tefs_account(cr, uid, move_lines, company.currency_id.name, account)
                            checks = get_checks_account(cr, uid, move_lines, company.currency_id.name, account)

                        total_tefs_curr += tefs
                        total_checks_curr += checks
                        total_deposit_curr += deposit
                        total_debit_curr += debit
                        total_credit_curr += credit
                        account_balance = debit - credit
                        total_balance_curr += account_balance
                        total_inital_balance_curr += account.init_balance

                        if not account.to_display:
                            continue

                        comparisons = account.comparisons

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

                        <div class="act_as_row lines ${level_class} ${"%s_account_type" % (account.type,)}">
                            ## code
                            <div class="act_as_cell first_column">${account.code}</div>
                            ## account name
                            <div class="act_as_cell">${account.name}</div>
                            %if comparison_mode == 'no_comparison':
                                %if initial_balance_mode:
                                    ## opening balance
                                    <div class="act_as_cell amount">${formatLang(account.init_balance) | amount}</div>
                                %endif
                                ## TEFS
                                <div class="act_as_cell amount">${formatLang(tefs) | amount}</div>
                                ## checks
                                <div class="act_as_cell amount">${formatLang(checks) | amount}</div>
                                ## deposit
                                <div class="act_as_cell amount">${formatLang(deposit) | amount}</div>
                                ## debit
                                <div class="act_as_cell amount">${formatLang(debit) | amount}</div>
                                ## credit
                                <div class="act_as_cell amount">${formatLang(credit) | amount}</div>
                            %endif
                            ## balance
                            <div class="act_as_cell amount">${formatLang(account_balance) | amount}</div>

                            %if comparison_mode in ('single', 'multiple'):
                                %for comp_account in comparisons:
                                    <div class="act_as_cell amount">${formatLang(comp_account['balance']) | amount}</div>
                                    %if comparison_mode == 'single':  ## no diff in multiple comparisons because it shows too data
                                        <div class="act_as_cell amount">${formatLang(comp_account['diff']) | amount}</div>
                                        <div class="act_as_cell amount"> 
                                        %if comp_account['percent_diff'] is False:
                                            ${ '-' }
                                        %else:
                                            ${int(round(comp_account['percent_diff'])) | amount} &#37;
                                        %endif
                                        </div>
                                    %endif
                                %endfor
                            %endif
                        </div>
                    %endfor
                </div>
                <div class="act_as_tfoot">
                    <div class="act_as_row labels"  style="font-weight: bold; font-size: 11x">
                        <div class="act_as_cell first_column">${_('Total')}</div>
                        <div class="act_as_cell">${' '}</div>
                        %if currency[0] != 'CRC':
                            <div class="act_as_cell amount">${account.report_currency_id.symbol}${formatLang(total_inital_balance_curr)}</div>
                            <div class="act_as_cell amount">${account.report_currency_id.symbol}${formatLang(total_tefs_curr)}</div>
                            <div class="act_as_cell amount">${account.report_currency_id.symbol}${formatLang(total_checks_curr)}</div>
                            <div class="act_as_cell amount">${account.report_currency_id.symbol}${formatLang(total_deposit_curr)}</div>
                            <div class="act_as_cell amount">${account.report_currency_id.symbol}${formatLang(total_debit_curr)}</div>
                            <div class="act_as_cell amount">${account.report_currency_id.symbol}${formatLang(total_credit_curr)}</div>
                            <div class="act_as_cell amount">${account.report_currency_id.symbol}${formatLang(total_balance_curr)}</div>
                        %else:
                            <div class="act_as_cell amount">${company.currency_id.symbol}${formatLang(total_inital_balance_curr)}</div>
                            <div class="act_as_cell amount">${company.currency_id.symbol}${formatLang(total_tefs_curr)}</div>
                            <div class="act_as_cell amount">${company.currency_id.symbol}${formatLang(total_checks_curr)}</div>
                            <div class="act_as_cell amount">${company.currency_id.symbol}${formatLang(total_deposit_curr)}</div>
                            <div class="act_as_cell amount">${company.currency_id.symbol}${formatLang(total_debit_curr)}</div>
                            <div class="act_as_cell amount">${company.currency_id.symbol}${formatLang(total_credit_curr)}</div>
                            <div class="act_as_cell amount">${company.currency_id.symbol}${formatLang(total_balance_curr)}</div>
                        %endif
                    </div>
                </div>
        </div>        
            %endfor
        
    </body>
</html>
