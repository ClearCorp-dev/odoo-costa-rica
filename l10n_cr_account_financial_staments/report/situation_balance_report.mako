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
            balance_data = get_data(cr, uid, data)
        %>
        <div style="font-size: 20px; font-weight: bold; text-align: center;"> ${company.partner_id.name}</div>
        <div style="font-size: 25px; font-weight: bold; text-align: center;"> ${_('Situation Balance')}</div>
        <div style="font-size: 16px; font-weight: bold; text-align: center;">${_('Situation Balance of Period:')} ${start_period.name}</div>
        <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
        <div class="act_as_table data_table">
            <div class="act_as_thead">
                <div class="act_as_row labels no_wrap">
                    <div class="act_as_cell first_column" style="width: 500px">${_('Name')}</div>
                    <div class="act_as_cell amount" style="width: 100px">${start_period.name}</div>
                    <div class="act_as_cell amount" style="width: 100px">${fiscalyear.name}</div>
                    <div class="act_as_cell amount" style="width: 100px">${_('Variation')}</div>
                    <div class="act_as_cell last_column amount" style="width: 40px">${_('%')}</div>
                </div>
            </div>
            <div class="act_as_tbody">
                <%
                    asset_total_period = balance_data['total_asset_balances']['period']
                    asset_total_fiscalyear = balance_data['total_asset_balances']['fiscal_year']
                    asset_total_variation = asset_total_period - asset_total_fiscalyear
                    asset_total_percentage_variation = asset_total_fiscalyear != 0 and (100 * asset_total_variation / asset_total_fiscalyear) or 0
                    
                    liability_total_period = balance_data['total_liability_balances']['period']
                    liability_total_fiscalyear = balance_data['total_liability_balances']['fiscal_year']
                    liability_total_variation = liability_total_period - liability_total_fiscalyear
                    liability_total_percentage_variation = liability_total_fiscalyear != 0 and (100 * liability_total_variation / liability_total_fiscalyear) or 0
                    
                    equity_total_period = balance_data['total_equity_balances']['period']
                    equity_total_fiscalyear = balance_data['total_equity_balances']['fiscal_year']
                    equity_total_variation = equity_total_period - equity_total_fiscalyear
                    equity_total_percentage_variation = equity_total_fiscalyear != 0 and (100 * equity_total_variation / equity_total_fiscalyear) or 0
                    
                    total_period = asset_total_period + liability_total_period + equity_total_period
                    total_fiscalyear = asset_total_fiscalyear + liability_total_fiscalyear + equity_total_fiscalyear
                    total_variation = total_period - total_fiscalyear
                    total_percentage_variation = total_fiscalyear != 0 and (100 * total_variation / total_fiscalyear) or 0
                
                %>
                %for account in balance_data['asset_accounts']:
                    <%
                        account_total_period = balance_data['asset_period_balances'][account.id]['balance']
                        account_total_fiscalyear = balance_data['asset_fiscal_year_balances'][account.id]['balance']
                        account_total_variation = account_total_period - account_total_fiscalyear
                        account_total_percentage_variation = account_total_fiscalyear != 0 and (100 * account_total_variation / account_total_fiscalyear) or 0
                   %>
                    <div class="act_as_row lines">
                        %if account.level > 0:
                            <div class="act_as_cell" style="padding-left:${account.level*10}px">
                                %if account.child_id:
                                    <div class="act_as_row first_column" ><b>${account.code} ${_(account.name)}</b></div>
                                %else:
                                    <div class="act_as_row first_column" >${account.code} ${_(account.name)}</div>
                                %endif
                            </div>
                        %else:
                            <div class="act_as_cell first_column" ><b>${account.code} ${_(account.name)}</b></div>
                        %endif
                        <div class="act_as_cell amount" >${formatLang(account_total_period)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_fiscalyear)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_variation)}</div>
                        <div class="act_as_cell amount last_column" >${formatLang(account_total_percentage_variation)}</div>
                    </div>
                %endfor                        
                <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
                <div class="act_as_row lines">
                    <div class="act_as_cell first_column" ><b>${_('ASSET TOTAL')}</b></div>
                    <div class="act_as_cell amount" >${formatLang(asset_total_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(asset_total_fiscalyear)}</div>
                    <div class="act_as_cell amount" >${formatLang(asset_total_variation)}</div>
                    <div class="act_as_cell amount last_column" >${formatLang(asset_total_percentage_variation)}</div>
                </div>
                <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
                
                %for account in balance_data['liability_accounts']:
                    <%
                        account_total_period = balance_data['liability_period_balances'][account.id]['balance']
                        account_total_fiscalyear = balance_data['liability_fiscal_year_balances'][account.id]['balance']
                        account_total_variation = account_total_period - account_total_fiscalyear
                        account_total_percentage_variation = account_total_fiscalyear != 0 and (100 * account_total_variation / account_total_fiscalyear) or 0
                    %>
                    <div class="act_as_row lines">
                        %if account.level > 0:
                            <div class="act_as_cell" style="padding-left:${account.level*10}px">
                                %if account.child_id:
                                    <div class="act_as_row first_column" ><b>${account.code} ${_(account.name)}</b></div>
                                %else:
                                    <div class="act_as_row first_column" >${account.code} ${_(account.name)}</div>
                                %endif
                            </div>
                        %else:
                            <div class="act_as_cell first_column" ><b>${account.code} ${_(account.name)}</b></div>
                        %endif
                        <div class="act_as_cell amount" >${formatLang(account_total_period)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_fiscalyear)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_variation)}</div>
                        <div class="act_as_cell amount last_column" >${formatLang(account_total_percentage_variation)}</div>
                    </div>
                %endfor            
                <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
                <div class="act_as_row lines">
                    <div class="act_as_cell first_column" ><b>${_('LIABILITY TOTAL')}</b></div>
                    <div class="act_as_cell amount" >${formatLang(liability_total_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(liability_total_fiscalyear)}</div>
                    <div class="act_as_cell amount" >${formatLang(liability_total_variation)}</div>
                    <div class="act_as_cell amount last_column" >${formatLang(liability_total_percentage_variation)}</div>
                </div>
                <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
                
                %for account in balance_data['equity_accounts']:
                    <%
                        account_total_period = balance_data['equity_period_balances'][account.id]['balance']
                        account_total_fiscalyear = balance_data['equity_fiscal_year_balances'][account.id]['balance']
                        account_total_variation = account_total_period - account_total_fiscalyear
                        account_total_percentage_variation = account_total_fiscalyear != 0 and (100 * account_total_variation / account_total_fiscalyear) or 0
                    %>
                    <div class="act_as_row lines">
                        %if account.level > 0:
                            <div class="act_as_cell" style="padding-left:${account.level*10}px">
                                %if account.child_id:
                                    <div class="act_as_row first_column" ><b>${account.code} ${_(account.name)}</b></div>
                                %else:
                                    <div class="act_as_row first_column" >${account.code} ${_(account.name)}</div>
                                %endif
                            </div>
                        %else:
                            <div class="act_as_cell first_column" ><b>${account.code} ${_(account.name)}</b></div>
                        %endif
                        <div class="act_as_cell amount" >${formatLang(account_total_period)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_fiscalyear)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_variation)}</div>
                        <div class="act_as_cell amount last_column" >${formatLang(account_total_percentage_variation)}</div>
                    </div>
                %endfor            
                <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
                <div class="act_as_row lines">
                    <div class="act_as_cell first_column" ><b>${_(' TOTAL')}</b></div>
                    <div class="act_as_cell amount" >${formatLang(equity_total_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(equity_total_fiscalyear)}</div>
                    <div class="act_as_cell amount" >${formatLang(equity_total_variation)}</div>
                    <div class="act_as_cell amount last_column" >${formatLang(equity_total_percentage_variation)}</div>
                </div>
                <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
                                        
                <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
                <div class="act_as_row lines">
                    <div class="act_as_cell first_column" ><b>${_('ASSET TOTAL')}</b></div>
                    <div class="act_as_cell amount" >${formatLang(asset_total_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(asset_total_fiscalyear)}</div>
                    <div class="act_as_cell amount" >${formatLang(asset_total_variation)}</div>
                    <div class="act_as_cell amount last_column" >${formatLang(asset_total_percentage_variation)}</div>
                </div>
                <div class="act_as_row lines">
                    <div class="act_as_cell first_column" ><b>${_('LIABILITY TOTAL')}</b></div>
                    <div class="act_as_cell amount" >${formatLang(liability_total_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(liability_total_fiscalyear)}</div>
                    <div class="act_as_cell amount" >${formatLang(liability_total_variation)}</div>
                    <div class="act_as_cell amount last_column" >${formatLang(liability_total_percentage_variation)}</div>
                </div>
                <div class="act_as_row lines">
                    <div class="act_as_cell first_column" ><b>${_('EQUITY TOTAL')}</b></div>
                    <div class="act_as_cell amount" >${formatLang(equity_total_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(equity_total_fiscalyear)}</div>
                    <div class="act_as_cell amount" >${formatLang(equity_total_variation)}</div>
                    <div class="act_as_cell amount last_column" >${formatLang(equity_total_percentage_variation)}</div>
                </div>
                <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
                <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
                <div class="act_as_row lines">
                    <div class="act_as_cell first_column" ><b>${_('TOTAL')}</b></div>
                    <div class="act_as_cell amount" >${formatLang(total_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(total_fiscalyear)}</div>
                    <div class="act_as_cell amount" >${formatLang(total_variation)}</div>
                    <div class="act_as_cell amount last_column" >${formatLang(total_percentage_variation)}</div>
                </div>
            </div>
        </div>
        <p style="page-break-after:always"></p>
    </body>
</html>
