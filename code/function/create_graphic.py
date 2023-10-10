from flask import render_template_string
import svgwrite
from PIL import ImageFont
import json
import csv

font = ImageFont.truetype('function/font/Arial.ttf', 18)

def DrawSVG(context):

	def TxtWidth(txt):
		return font.getsize(txt)[0]

	def AddTxt(txt, pos, style):
		color, weight = style
		dwg.add(dwg.text(txt, insert=pos, fill=color, font_weight=weight, font_family='Arial'))

	def AddRect(pos, size, color):
		dwg.add(dwg.rect(insert=pos, size=size, fill=color))

	dwg = svgwrite.Drawing(profile='tiny')

	x_pos = 350

	try:
		file = open('theme/'+context['theme'].split('_')[0]+'.json')
		col = json.load(file)
	except:
		try:
			file = open('theme/'+context['theme']+'.json')
			col = json.load(file)
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

	AddRect((0, 0), ('100%', '100%'), bg_col)

	try:
		with open('display_image/'+context['img']+'.csv', mode='r') as csvfile:
			img_data = csv.reader(csvfile)
			next(img_data)
			for row in img_data:
				AddTxt(row[3], (row[0], row[1]), (col[row[2]], 'normal'))

	except:
		return {'username': context['username'], 'img': context['img'], 'message': 'img does not exist'}, 201

	AddTxt(context['username'], (x_pos, 20), (main_col, 'bold'))
	AddTxt('@', (x_pos+TxtWidth(context['username']), 20), (second_col, 'normal'))
	AddTxt('githubstat', (x_pos+TxtWidth(context['username']+'@'), 20), (main_col, 'bold'))

	line = ''
	while TxtWidth(line) < TxtWidth(f"{context['username']}@githubstat")+20:
		line += '_ '

	AddTxt(line, (x_pos, 50), (second_col, 'normal'))

	AddTxt('last year contrib: ', (x_pos, 80), (main_col, 'bold'))
	AddTxt(context['contrib'], (x_pos+TxtWidth('last year contrib: '), 80), (second_col, 'normal'))

	AddTxt('info of top10 repos: ', (x_pos, 110), (main_col, 'bold'))
	AddTxt('by stargaze', (x_pos+TxtWidth('info of top10 repos: '), 110), (second_col, 'normal'))

	AddTxt('Total stars: ', (x_pos, 140), (main_col, 'bold'))
	AddTxt(context['all_stars'], (x_pos+TxtWidth('Total stars: '), 140), (second_col, 'normal'))

	context['all_lang'] = context['all_lang'].replace("'", "").replace('{','').replace('}','').split(',')
	y_pos = 170
	for lang_and_amount in context['all_lang']:
		lang, amount = lang_and_amount.split(":")

		AddTxt(f'{lang}: ', (x_pos, y_pos), (main_col, 'bold'))
		AddTxt(amount, (x_pos+TxtWidth(f'{lang}: '), y_pos), (second_col, 'normal'))
		y_pos += 30

	color_in_row = 0
	for color in col:
		if color_in_row > 7:
			color_in_row = 0
			y_pos += 30
			x_pos -= 30*8
		AddRect((x_pos, y_pos), (30, 20), col[color])
		color_in_row += 1
		x_pos += 30

	y_pos += 50
	AddTxt(context['username'], (10, y_pos), (main_col, 'bold'))
	AddTxt('@', (10+TxtWidth(context['username']), y_pos), (second_col, 'normal'))
	AddTxt('githubstat:', (10+TxtWidth(context['username']+'@'), y_pos), (main_col, 'bold'))
	AddTxt('~$', (10+TxtWidth(f"{context['username']}@githubstat:"), y_pos), (second_col, 'bold'))

	blinktxt = dwg.text('|', insert=(10+TxtWidth(f"{context['username']}@githubstat:~$"), y_pos), fill=main_col, font_weight='bold', font_family='Arial', class_='blink')
	dwg.add(blinktxt)

	svg = dwg.tostring()

	svg_with_css = f'''
		<style>
			.blink {{
				animation: blink 1s steps(2, start) infinite;
			}}
			@keyframes blink {{
				to {{
					visibility: hidden;
					}}
			}}
		</style>
		{svg}
		'''

	return render_template_string('<div>{{ svg|safe }}</div>', svg=svg_with_css)