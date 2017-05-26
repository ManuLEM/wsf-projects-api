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
	'themes': 'Quelle est la thématique de ton projet?',
	'technos': 'De quelle techno as-tu besoin?',
	'clients': 'Quel est le client de ton projet?',
	'types': 'Quelle typologie cherches-tu?'
}

app = Eve()

@app.route("/list/<string:type>", methods=['GET'])
def list_options(type):
	if type == 'types':
		options = [{'name':'WEC'},{'name':'AMC'},{'name':'Free Time'},{'name':'PFA'},{'name':'Data'}]
	else:
		options = app.data.driver.db[type].find()

	if options.count() == 0:
		return jsonify({
			'messages': [{
				'text': 'Désolé, je n\'ai aucun projet en réserve qui corresponde à ta recherche :/'
			},{
				'text': 'Tu veux retenter une recherche?',
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
			'title': option['name']
		})
	return jsonify(message)


@app.route("/add_project", methods=['POST'])
def add_project():
	'''name
	teammates
	technos
	theme
	tags
	client
	project_type
	link
	year'''

	app.data.driver.db['themes'].get_or_create({
		'name': request.json['theme']
	})

	subtitle = [request.json['year']] if request.json['year'] else []
	subtitle.append(request.json['project_type'], request.json['client'], request.json['theme'])

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
						'subtitle':subtitle.join(' - '),
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

if __name__ == '__main__':
	app.run(host=host,port=port)
