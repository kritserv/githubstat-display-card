from flask import request
from app import app
from app.backend.function.get_and_add_data import CreateNewTable, QueryFromSQLite, GetSQLiteData, ScrapDataFromGithub, AddNewDataToSQLite
from app.frontend.function.load_default import UseDefaultValue
from app.frontend.function.create_graphic import DrawSVG

CreateNewTable() # Create table if not exist

@app.route('/')
def StatsView():

    username = request.args.get('username')
    theme = request.args.get('theme')
    bg_col = request.args.get('bg_col')
    main_col = request.args.get('main_col')
    second_col = request.args.get('second_col')
    img = request.args.get('img')

    if username:

        context = {}

        userdata_in_db = QueryFromSQLite(username)

        if userdata_in_db == None:

            userdata = ScrapDataFromGithub(username)
            AddNewDataToSQLite(username, userdata)

        try:
            context = GetSQLiteData(username)
        except:
            return {'username': username, 'message': 'username does not exist'}, 201
        
        context['theme'], context['bg_col'], context['main_col'], context['second_col'], context['img'] = UseDefaultValue(
                theme, 
                bg_col, 
                main_col, 
                second_col, 
                img
            )

        return DrawSVG(context)

    else:
        return {'username': username}, 201