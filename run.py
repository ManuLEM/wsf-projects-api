# coding: utf-8
import os
from eve import Eve
from flask import jsonify

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
	'clients': 'Quel est le client de ton projet?'
}

app = Eve()

@app.route("/list/<string:type>")
def list_options(type):
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

if __name__ == '__main__':
	app.run(host=host,port=port)
