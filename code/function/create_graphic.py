from flask import render_template_string
import svgwrite
from svgwrite import animate
from PIL import ImageFont
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

	x_pos = 300

	col = {
		'black':'#171421',
		'red':'#C01C28',
		'green':'#26A269',
		'brown':'#A2734C',
		'darkblue':'#12488B',
		'darkpurple':'#A347BA',
		'cyan':'#2AA1B3',
		'lightgrey':'#D0CFCC',
		'grey':'#5E5C64',
		'lightred':'#F66151',
		'lightgreen':'#33D17A',
		'yellow':'#E9AD0C',
		'blue':'#2A7BDE',
		'purple':'#C061CB',
		'skyblue':'#33C7DE',
		'white':'#FFFFFF',
	}

	bg_col = '#171421'
	main_col = col['green']
	second_col = col['white']

	AddRect((0, 0), ('100%', '100%'), bg_col)

	AddTxt(context['username'], (x_pos, 20), (main_col, 'bold'))
	AddTxt('@', (x_pos+TxtWidth(context['username']), 20), (second_col, 'normal'))
	AddTxt('githubstat', (x_pos+TxtWidth(context['username']+'@'), 20), (main_col, 'bold'))

	line = ''
	while TxtWidth(line) < TxtWidth(f"{context['username']}@githubstat")+20:
		line += '_ '

	AddTxt(line, (x_pos, 50), (col['white'], 'normal'))

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

	# Add the CSS inside a <style> block
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

	# Render the SVG with CSS in an HTML template
	return render_template_string('<div>{{ svg|safe }}</div>', svg=svg_with_css)

	#return dwg.tostring()