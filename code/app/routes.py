from flask import request
from app import app
from app.backend.function.get_and_add_data import CreateNewTable, QueryFromSqlite, GetSqliteData, ScrapDataFromGithub, AddNewDataToSqlite
from app.frontend.function.load_default import UseDefaultValue
from app.frontend.function.main import DrawSvg

CreateNewTable() # Create table if not exist

@app.route('/')
def StatsView():

    username = request.args.get('username')
    theme = request.args.get('theme')
    bg_col = request.args.get('bg_col')
    main_col = request.args.get('main_col')
    second_col = request.args.get('second_col')
    img = request.args.get('img')
    use_font = request.args.get('font')

    if username:

        context = {}

        userdata_in_db = QueryFromSqlite(username)

        if userdata_in_db == None:

            userdata = ScrapDataFromGithub(username)
            AddNewDataToSqlite(username, userdata)

        try:
            context = GetSqliteData(username)
        except:
            return {'username': username, 'message': 'username does not exist'}, 201
        
        context['theme'], context['bg_col'], context['main_col'], context['second_col'], context['img'], context['use_font'] = UseDefaultValue(
                theme, 
                bg_col, 
                main_col, 
                second_col, 
                img,
                use_font
            )

        return DrawSvg(context)

    else:
        return {'username': username}, 201