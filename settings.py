MONGO_HOST = 'ds151651.mlab.com'
MONGO_PORT = 51651

# Skip these if your db has no auth. But it really should.
MONGO_USERNAME = 'wsf-api'
MONGO_PASSWORD = 'RYHorcOysshazK2'

MONGO_DBNAME = 'heroku_5xjfsncr'
MONGO_AUTH_MECHANISM = 'SCRAM-SHA-1'

DOMAIN = {
	'projects': {
		'project_type': {
			'type': 'string',
			'required': True,
			'allowed': ['WEC','AMC','Free Time','PFA','Data']
		},
		'tags': {
			'type': 'list',
			'schema': {
				'type': 'string'
			}
		},
		'technos': {
			'type': 'list',
			'schema': {
				'type': 'objectid'
			}
		},
		'theme': {
			'type': 'objectid'
		},
		'year': {
			'type': 'integer',
			'min': 1,
			'max': 5
		},
		'students': {
			'type': 'list',
			'required': True,
			'schema': {
				'type': 'objectid',
				'required': True
			}
		}
	},
	'students': {
		'firstname': {
			'type': 'string',
			'minlength': 1,
			'maxlength': 15,
			'required': True
		},
		'lastname': {
			'type': 'string',
			'minlength': 1,
			'maxlength': 25,
			'required': True
		},
		'promotion': {
			'type': 'integer',
			'min': 2017,
			'max': 2040
		}
	},
	'clients': {
		'name': {
			'type': 'string',
			'minlength': 1,
			'maxlength': 15,
			'required': True
		}
	},
	'technos': {
		'name': {
			'type': 'string',
			'required': True
		}
	},
	'themes': {
		'name': {
			'type': 'string',
			'required': True
		}
	}
}

