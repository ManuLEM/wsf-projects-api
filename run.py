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

app = Eve()


@app.route("/test")
def test():
	return 'Hello world'

@app.route("/client_list")
def clients():
	return jsonify(
		{
			'text': 'Quel est le client de ton projet?',
			'quick_replies': [{
				'content_type': 'text',
				'title': 'A',
				'payload': '|'
			}]
		}
	)

if __name__ == '__main__':
	app.run(host=host,port=port)
