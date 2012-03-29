UPDATE res_users
    SET context_lang = 'es_CR',
        context_tz = 'America/Costa_Rica'
    WHERE id = 1;

UPDATE res_lang
    SET direction = 'ltr',
        decimal_point = ',',
        thousands_sep = '.',
        time_format = '%I:%M:%S %p',
        date_format = '%d/%m/%Y',
        grouping = '[3,3,3,3,3,-2]'
    WHERE code = 'es_CR';
