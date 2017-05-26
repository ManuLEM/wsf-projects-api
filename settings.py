MONGO_HOST = 'ds151651.mlab.com'
MONGO_PORT = 51651

# Skip these if your db has no auth. But it really should.
MONGO_USERNAME = 'wsf-api'
MONGO_PASSWORD = 'RYHorcOysshazK2'

MONGO_DBNAME = 'heroku_5xjfsncr'
MONGO_AUTH_MECHANISM = 'SCRAM-SHA-1'

DOMAIN = {
	'projects': {
		'name': {
			'type': 'string',
			'required': True,
			'unique': True
		},
		'project_type': {
			'type': 'string',
			'required': True,
			'allowed': ['WEC','AMC','Free Time','PFA','Data']
		},
		'link': {
			'type': 'string',
			'required': True
		},
		'technos': {
			'type': 'list',
			'schema': {
				'type': 'string'
			}
		},
		'theme': {
			'type': 'string'
		},
		'client': {
			'type': 'string'
		},
		'year': {
			'type': 'integer',
			'min': 1,
			'max': 5
		},
		'students': {
			'type': 'list',
			'schema': {
				'type': 'dict',
				'schema': {
					'firstname': {
						'type': 'string'
					},
					'lastname': {
						'type': 'string'
					}
				}
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

