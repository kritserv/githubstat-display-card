from flask import Flask, request

from function.get_and_add_data import CreateNewTable, QueryFromSQLite, GetSQLiteData, ScrapDataFromGithub, AddNewDataToSQLite
from function.create_graphic import DrawSVG

app = Flask(__name__)

CreateNewTable() # Create Database if not already exists

@app.route('/')
def StatsView():

	username = request.args.get('username')
	theme = request.args.get('theme')
	bg_col = request.args.get('bg_col')
	main_col = request.args.get('main_col')
	second_col = request.args.get('second_col')

	if username:

		userdata_in_db = QueryFromSQLite(username)

		if userdata_in_db == None:

			userdata = ScrapDataFromGithub(username)
			AddNewDataToSQLite(username, userdata)

		context = GetSQLiteData(username)
		
		if theme == None: 
			theme = "tango_dark"

		if bg_col == None and 'dark' in theme: 
			bg_col = "black"
		elif bg_col == None and 'light' in theme: 
			bg_col = "white"
		else: 
			bg_col = "black"

		if main_col == None: 
			main_col = "lightgreen"

		if second_col == None and bg_col == "black": 
			second_col = "white"
			
		if second_col == None and bg_col == "white": 
			second_col = "black"

		context['theme'] = theme
		context['bg_col'] = bg_col
		context['main_col'] = main_col
		context['second_col'] = second_col

		return DrawSVG(context)

	else:
		return {'username': username}, 201

if __name__ == '__main__':
	app.run(debug=True)