from eve import Eve
from flask import jsonify
app = Eve()

@app.route("/client_list")
def clients():
	return jsonify({
		'text': 'Quel est le client de ton projet?',
		'quick_replies': [{
			'content_type': 'text',
			'title': 'A',
			'payload': '|'
		}]
	})

if __name__ == '__main__':
	app.run()
