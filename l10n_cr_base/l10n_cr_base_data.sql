/*		res.lang
		Update fields 
]*/

update res_lang		
	set name = 'Spanish / Español',
		active = 'True',
		translatable = 'True',
		grouping = '[3]',
		direction = 'ltr',
		date_format = '%d/%m/%Y',
		time_format = '%I:%M:%S %p',
		decimal_point = ',',
		thousands_sep = '.'
	where code = 'es_ES';
