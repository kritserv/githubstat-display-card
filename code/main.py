from flask import Flask, request

from function.get_and_add_data import CreateNewTable, QueryFromSQLite, GetSQLiteData, InsertApiData
from function.create_graphic import DrawSVG

app = Flask(__name__)

CreateNewTable() # Create Database if not already exists

@app.route('/')
def StatsView():

	username = request.args.get('username')
	theme = request.args.get('theme')

	if username:

		query_in_db = QueryFromSQLite(username)

		if query_in_db == None: InsertApiData(username)

		context = GetSQLiteData(username)
		if theme == None: theme = "default"
		context['theme'] = theme

		return DrawSVG(context)

	else:
		return {'username': username, 'theme': theme}, 201

if __name__ == '__main__':
	app.run(debug=True)