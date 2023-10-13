from flask import Response
from bs4 import BeautifulSoup, NavigableString
import svgwrite
import csv
from .calculate_text_width import TxtWidth
from .add_svg_element import AddTxt, AddRect
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
			for row in img_data:
				AddTxt(row[3], (row[0], row[1]), (col[row[2]], 'normal'), dwg)

	except:
		return {'username': context['username'], 'img': context['img'], 'message': 'img does not exist'}, 201

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

	html_string = dwg.tostring()
	soup = BeautifulSoup(html_string, 'html.parser')
	svg_tag = soup.find('svg')

	style_tag = soup.new_tag('style')

	css = """.blink {animation: blink 1s steps(2, start) infinite;}
@keyframes blink { to { visibility: hidden;}}"""
	style_tag.append(NavigableString(css))

	svg_tag.append(style_tag)
	svg = str(svg_tag)

	return Response(svg, mimetype='image/svg+xml')