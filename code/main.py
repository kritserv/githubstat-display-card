from flask import Flask, request

from function.get_and_add_data import CreateNewTable, QueryFromSQLite, GetSQLiteData, InsertApiData
from function.create_graphic import DrawSVG

app = Flask(__name__)

flaskusr = '' # Your Github Username
token = '' # Your Github Token

CreateNewTable()

@app.route('/')
def github_stats():

	username = request.args.get('username')
	theme = request.args.get('theme')

	context = {}

	query_in_db = QueryFromSQLite(username)

	if query_in_db == None: InsertApiData(username,flaskusr, token)

	context = GetSQLiteData(username)
	context['theme'] = theme

	return DrawSVG(context)

if __name__ == '__main__':
	app.run(debug=True)
