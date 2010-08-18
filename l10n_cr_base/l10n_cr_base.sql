update res_users
    set context_lang = 'es_ES',
        context_tz = 'America/Costa_Rica'
    where id = 1;

update res_lang
    set direction = 'ltr',
        decimal_point = ',',
        thousands_sep = '.',
        time_format = '%I:%M:%S %p',
        date_format = '%d/%m/%Y',
        grouping = '[3,3,3,3,3]'
    where code = 'es_ES';
