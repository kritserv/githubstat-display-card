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
		with open(img_dir+context['img']+'.csv', mode='r') as csvfile:
			img_data = csv.reader(csvfile)
			next(img_data)
			for column in img_data:
				AddTxt(column[3], (column[0], column[1]), (column[2], 'normal'), dwg)
	except:
		with open(img_dir+'animate/'+context['img']+'.csv', mode='r') as csvfile:
			img_data = csv.reader(csvfile)
			next(img_data)
			for column in img_data:
				dwg.add(dwg.text(column[3], insert=(column[0], column[1]), fill=col[column[2]], font_weight='normal', font_family='Arial', class_='frame'+column[4]))

	AddTxt(context['username'], (x_pos, 20), (main_col, 'bold'), dwg)
	AddTxt('@', (x_pos+TxtWidth(context['username']), 20), (second_col, 'normal'), dwg)
	AddTxt('githubstat', (x_pos+TxtWidth(context['username']+'@'), 20), (main_col, 'bold'), dwg)

	line = ''
	while TxtWidth(line) < TxtWidth(f"{context['username']}@githubstat")+20:
		line += '_ '

	AddTxt(line, (x_pos, 50), (second_col, 'normal'), dwg)

	AddTxt('last year contrib: ', (x_pos, 80), (main_col, 'bold'), dwg)
	AddTxt(context['contrib'], (x_pos+TxtWidth('last year contrib: '), 80), (second_col, 'normal'), dwg)

	AddTxt('info of top10 repos: ', (x_pos, 110), (main_col, 'bold'), dwg)
	AddTxt('by stargaze', (x_pos+TxtWidth('info of top10 repos: '), 110), (second_col, 'normal'), dwg)

	AddTxt('Total Stars: ', (x_pos, 140), (main_col, 'bold'), dwg)
	AddTxt(str(context['all_stars'])+' ★', (x_pos+TxtWidth('Total Stars: '), 140), (second_col, 'normal'), dwg)

	context['all_lang'] = context['all_lang'].replace("'", "").replace('{','').replace('}','').split(',')
	y_pos = 170
	for lang_and_amount in list(reversed(context['all_lang'])):
		lang, amount = lang_and_amount.split(":")

		AddTxt(f'{lang}: ', (x_pos, y_pos), (main_col, 'bold'), dwg)
		AddTxt(amount, (x_pos+TxtWidth(f'{lang}: '), y_pos), (second_col, 'normal'), dwg)
		y_pos += 30

	AddTxt('date: ', (x_pos, y_pos), (main_col, 'bold'), dwg)
	AddTxt(context['latest_update'], (x_pos+TxtWidth('date: '), y_pos), (second_col, 'normal'), dwg)
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
	AddTxt(context['username'], (10, y_pos), (main_col, 'bold'), dwg)
	AddTxt('@', (10+TxtWidth(context['username']), y_pos), (second_col, 'normal'), dwg)
	AddTxt('githubstat:', (10+TxtWidth(context['username']+'@'), y_pos), (main_col, 'bold'), dwg)
	AddTxt('~$', (10+TxtWidth(f"{context['username']}@githubstat:"), y_pos), (second_col, 'bold'), dwg)

	blinktxt = dwg.text('|', insert=(10+TxtWidth(f"{context['username']}@githubstat:~$  "), y_pos), fill=main_col, font_weight='bold', font_family='Arial', class_='blink')
	dwg.add(blinktxt)

	dwg = AddCss('blink_and_animate', dwg)

	return Response(dwg, mimetype='image/svg+xml')