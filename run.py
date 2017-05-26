# coding: utf-8
import os
from eve import Eve
from flask import jsonify
from flask import request

# Heroku support: bind to PORT if defined, otherwise default to 5000.
if 'PORT' in os.environ:
	port = int(os.environ.get('PORT'))
	# use '0.0.0.0' to ensure your REST API is reachable from all your
	# network (and not only your computer).
	host = '0.0.0.0'
else:
	host = '127.0.0.1'
	port = 5000

searchable_items = {
	'themes': 'Tu cherches un projet en particulier?',
	'technos': 'T’as une idée de techno en tête, ou pas encore?',
	'clients': 'Qui est ton client / le partenaire du projet?',
	'types': 'T’as un thème en particulier?'
}

app = Eve()

@app.route("/list/<string:type>", methods=['GET'])
def list_options(type):
	type = type if type[-1] == 's' else type.lower()+'s'
	if type == 'types':
		options = [{'name':'WEC'},{'name':'AMC'},{'name':'Free Time'},{'name':'PFA'},{'name':'Data'}]
	else:
		options = app.data.driver.db[type].find()

	if options.count() == 0:
		return jsonify({
			'messages': [{
				'text': 'Désolée :/ je n’ai aucun projet en stock qui corresponde à ta recherche...'
			},{
				'text': 'Tu veux réessayer ? :)',
				'buttons': [{
					'type': 'show_block',
					'block_name': 'Search',
					'title': 'Je cherche'
				}]
			}]
		})

	message = {
		'messages': [{
			'text': searchable_items[type],
			'quick_replies': []
		}]
	}
	for option in options:
		message['messages'][0]['quick_replies'].append({
			'content_type': 'text',
			'title': option['name'],
			'block_names':['Get Projects'],
			"set_attributes": {
				"filter_value": option['name']
			}
		})
	return jsonify(message)


@app.route("/add_project", methods=['POST'])
def add_project():
	'''name
	teammates
	technos
	theme
	client
	project_type
	link
	year'''
	def format_student(student):
		student = student.lstrip()
		array = student.split(' ')
		firstname = array[0]
		lastname = ' '.join(array[1:])
		return {
			'firstname': firstname,
			'lastname': lastname
		}

	req = request.json
	themes = app.data.driver.db['themes'].find({'name': req['theme']})
	clients = app.data.driver.db['clients'].find({'name': req['client']})
	tech_array = req['technos'].split(',')
	tech_array = map(lambda x: x.lstrip(), tech_array)
	students_array = req['teammates'].split(',')
	students_array = map(lambda x: format_student(x), students_array)

	if themes.count() == 0:
		app.data.driver.db['themes'].insert({
			'name': req['theme']
		})
	if clients.count() == 0:
		app.data.driver.db['clients'].insert({
			'name': req['client']
		})

	for tech in tech_array:
		items = app.data.driver.db['technos'].find({'name': tech})
		if items.count() == 0:
			app.data.driver.db['technos'].insert({
				'name': tech
			})
	for student in students_array:
		items = app.data.driver.db['students'].find({'firstname': student['firstname'], 'lastname': student['lastname']})
		if items.count() == 0:
			app.data.driver.db['students'].insert({
				'firstname': student['firstname'],
				'lastname': student['lastname']
			})

	app.data.driver.db['projects'].insert({
		'name': req['name'],
		'client': req['client'],
		'theme': req['theme'],
		'project_type': req['project_type'],
		'link': req['link'],
		'year': req['year'] if req['project_type'] != 'WEC' and req['project_type'] != 'AMC' else '',
		'technos': tech_array,
		'students': students_array

	})

	subtitle = [request.json['year']] if request.json['year'] else []
	subtitle.append(request.json['project_type'])
	subtitle.append(request.json['client'])
	subtitle.append(request.json['theme'])

	return jsonify({
		'messages': [{
			'text': 'Ton projet a bien été ajouté! Voilà le résulat'
		},{
			'attachment':{
				'type':'template',
				'payload':{
					'template_type':'generic',
					'elements':[{
						'title':request.json['name'],
						'subtitle':' - '.join(subtitle),
						'buttons':[
							{
							'type':'web_url',
							'url':request.json['link'],
							'title':'Voir le projet'
							}
						]
					}]
				}
			}
		}]
	})

@app.route("/get_projects", methods=['GET'])
def get_project():
	# request.args['filter_type']
	# request.args['filter_value']
	options = app.data.driver.db['projects'].find()

	# 'text': 'C\'est bien ce que tu cherchais ? :)'
	return jsonify({
		'messages': [{
			'text': 'Désolé, cette fonctionnalité est pas encore implémentée :/',
			'buttons': [{
				'type': 'show_block',
				'block_name': 'Search',
				'title': 'Nouvelle recherche'
			},{
				'type': 'show_block',
				'block_name': 'Add - 1',
				'title': 'Ajouter un projet'
			}]
		}]
	})

if __name__ == '__main__':
	app.run(host=host,port=port)
