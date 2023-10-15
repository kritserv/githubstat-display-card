from flask import Response
import svgwrite
import csv
from .calculate_text_width import TxtWidth
from .add_svg_element import AddTxt, AddRect, AddCss
from .settings import LoadTheme, img_dir

def DrawSvg(context):

	dwg = svgwrite.Drawing(profile='tiny')

	x_pos = 350

	try:
		col = LoadTheme(context['theme'].split('_')[0])
	except:
		try:
			col = LoadTheme(context['theme'])
		except:
			return {'username': context['username'], 'theme': context['theme'], 'message': 'theme does not exist'}, 201

	try:
		bg_col = col[context['bg_col']]
	except:
		return {'username': context['username'], 'bg_col': context['bg_col'], 'message': 'color does not exist'}, 201

	try:
		main_col = col[context['main_col']]
	except:
		return {'username': context['username'], 'main_col': context['main_col'], 'message': 'color does not exist'}, 201

	try:
		second_col = col[context['second_col']]
	except:
		return {'username': context['username'], 'second_col': context['second_col'], 'message': 'color does not exist'}, 201

	AddRect((0, 0), ('100%', '100%'), bg_col, dwg)

	try:
		with open(img_dir+context['img']+'_'+context['use_font']+'.csv', mode='r') as csvfile:
			img_data = csv.reader(csvfile)
			next(img_data)
			for column in img_data:
				dwg.add(dwg.text(column[3], insert=(column[0], column[1]), fill=col[column[2]], font_weight='normal', font_family=context['use_font'].title()))
	except:
		with open(img_dir+'animate/'+context['img']+'_'+context['use_font']+'.csv', mode='r') as csvfile:
			img_data = csv.reader(csvfile)
			next(img_data)
			for column in img_data:
				dwg.add(dwg.text(column[3], insert=(column[0], column[1]), fill=col[column[2]], font_weight='normal', font_family=context['use_font'].title(), class_='frame'+column[4]))

	AddTxt(context['username'], (x_pos, 20), (main_col, 'bold'), dwg, context['use_font'].title())
	AddTxt('@', (x_pos+TxtWidth(context['username'], context['use_font']), 20), (second_col, 'normal'), dwg, context['use_font'].title())
	AddTxt('githubstat', (x_pos+TxtWidth(context['username']+'@', context['use_font']), 20), (main_col, 'bold'), dwg, context['use_font'].title())

	line = ''
	while TxtWidth(line, context['use_font']) < TxtWidth(f"{context['username']}@githubstat", context['use_font'])+20:
		line += '_ '

	AddTxt(line, (x_pos, 50), (second_col, 'normal'), dwg, context['use_font'].title())

	AddTxt('last year contrib: ', (x_pos, 80), (main_col, 'bold'), dwg, context['use_font'].title())
	AddTxt(context['contrib'], (x_pos+TxtWidth('last year contrib: ', context['use_font']), 80), (second_col, 'normal'), dwg, context['use_font'].title())

	AddTxt('info of top10 repos: ', (x_pos, 110), (main_col, 'bold'), dwg, context['use_font'].title())
	AddTxt('by stargaze', (x_pos+TxtWidth('info of top10 repos: ', context['use_font']), 110), (second_col, 'normal'), dwg, context['use_font'].title())

	AddTxt('Total Stars: ', (x_pos, 140), (main_col, 'bold'), dwg, context['use_font'].title())
	AddTxt(str(context['all_stars'])+' ★', (x_pos+TxtWidth('Total Stars: ', context['use_font']), 140), (second_col, 'normal'), dwg, context['use_font'].title())

	context['all_lang'] = context['all_lang'].replace("'", "").replace('{','').replace('}','').split(',')
	y_pos = 170
	for lang_and_amount in list(reversed(context['all_lang'])):
		lang, amount = lang_and_amount.split(":")

		AddTxt(f'{lang}: ', (x_pos, y_pos), (main_col, 'bold'), dwg, context['use_font'].title())
		AddTxt(amount, (x_pos+TxtWidth(f'{lang}: ', context['use_font']), y_pos), (second_col, 'normal'), dwg, context['use_font'].title())
		y_pos += 30

	AddTxt('date: ', (x_pos, y_pos), (main_col, 'bold'), dwg, context['use_font'].title())
	AddTxt(context['latest_update'], (x_pos+TxtWidth('date: ', context['use_font']), y_pos), (second_col, 'normal'), dwg, context['use_font'].title())
	y_pos += 30

	color_in_row = 0
	for color in col:
		if color_in_row > 7:
			color_in_row = 0
			y_pos += 30
			x_pos -= 30*8
		AddRect((x_pos, y_pos), (30, 20), col[color], dwg)
		color_in_row += 1
		x_pos += 30

	y_pos += 50
	AddTxt(context['username'], (10, y_pos), (main_col, 'bold'), dwg, context['use_font'].title())
	AddTxt('@', (10+TxtWidth(context['username'], context['use_font']), y_pos), (second_col, 'normal'), dwg, context['use_font'].title())
	AddTxt('githubstat:', (10+TxtWidth(context['username']+'@', context['use_font']), y_pos), (main_col, 'bold'), dwg, context['use_font'].title())
	AddTxt('~$', (10+TxtWidth(f"{context['username']}@githubstat:", context['use_font']), y_pos), (second_col, 'bold'), dwg, context['use_font'].title())

	blinktxt = dwg.text('|', insert=(10+TxtWidth(f"{context['username']}@githubstat:~$  ", context['use_font']), y_pos), fill=main_col, font_weight='bold', font_family=context['use_font'].title(), class_='blink')
	dwg.add(blinktxt)

	dwg = AddCss('blink_and_animate', dwg)

	return Response(dwg, mimetype='image/svg+xml')