import os
import json

root_dir = os.getcwd()

theme_dir = f'{root_dir}/app/frontend/theme/'

img_dir = 'app/frontend/display_image/'

def LoadTheme(theme):
	file = open(theme_dir+'/'+theme.split('_')[0]+'.json')
	return json.load(file)