from flask import Response
import svgwrite
import csv
from .calculate_text_width import TxtWidth
from .add_svg_element import AddTxt, AddRect, AddCss
from .settings import LoadTheme, img_dir

def DrawSvg(context):

	dwg = svgwrite.Drawing(profile='tiny')
	need_animate_css = False

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

	try:
		used_font = context['use_font']
	except:
		return {'username': context['username'], 'font': context['use_font'], 'message': 'font does not exist'}, 201

	try:
	    pc_name = context['pc_name']
	except:
	    return {'username': context['username'], 'pc_name': context['pc_name'], 'message': 'cannot use this word'}, 201

	AddRect((0, 0), ('100%', '100%'), bg_col, dwg)

	try:
		with open(img_dir+context['img']+'_'+used_font+'.csv', mode='r') as csvfile:
			img_data = csv.reader(csvfile)
			next(img_data)
			for column in img_data:
				dwg.add(dwg.text(column[3], insert=(column[0], column[1]), fill=col[column[2]], font_weight='normal', font_family=used_font))
	except:
		try:
			with open(img_dir+'animate/'+context['img']+'_'+used_font+'.csv', mode='r') as csvfile:
				img_data = csv.reader(csvfile)
				next(img_data)
				for column in img_data:
					dwg.add(dwg.text(column[3], insert=(column[0], column[1]), fill=col[column[2]], font_weight='normal', font_family=used_font, class_='frame'+column[4]))
				need_animate_css = True
		except:
			return {'username': context['username'], 'img': context['img'], 'message': 'image does not exist'}, 201

	AddTxt(context['username'], (x_pos, 20), (main_col, 'bold'), dwg, used_font)
	AddTxt('@', (x_pos+TxtWidth(context['username'], used_font), 20), (second_col, 'normal'), dwg, used_font)
	AddTxt(context['pc_name'], (x_pos+TxtWidth(context['username']+'@', used_font), 20), (main_col, 'bold'), dwg, used_font)

	line = ''
	while TxtWidth(line, used_font) < TxtWidth(f"{context['username']}@{context['pc_name']}", used_font)+20:
		line += '_ '

	AddTxt(line, (x_pos, 50), (second_col, 'normal'), dwg, used_font)

	AddTxt('last year contrib: ', (x_pos, 80), (main_col, 'bold'), dwg, used_font)
	AddTxt(context['contrib'], (x_pos+TxtWidth('last year contrib: ', used_font), 80), (second_col, 'normal'), dwg, used_font)

	AddTxt('info of top10 repos: ', (x_pos, 110), (main_col, 'bold'), dwg, used_font)
	AddTxt('by stargaze', (x_pos+TxtWidth('info of top10 repos: ', used_font), 110), (second_col, 'normal'), dwg, used_font)

	AddTxt('Total Stars: ', (x_pos, 140), (main_col, 'bold'), dwg, used_font)
	AddTxt(str(context['all_stars'])+' ★', (x_pos+TxtWidth('Total Stars: ', used_font), 140), (second_col, 'normal'), dwg, used_font)

	context['all_lang'] = context['all_lang'].replace("'", "").replace('{','').replace('}','').split(',')
	y_pos = 170
	for lang_and_amount in list(reversed(context['all_lang'])):
		lang, amount = lang_and_amount.split(":")

		AddTxt(f'{lang}: ', (x_pos, y_pos), (main_col, 'bold'), dwg, used_font)
		AddTxt(amount, (x_pos+TxtWidth(f'{lang}: ', used_font), y_pos), (second_col, 'normal'), dwg, used_font)
		y_pos += 30

	AddTxt('date: ', (x_pos, y_pos), (main_col, 'bold'), dwg, used_font)
	AddTxt(context['latest_update'], (x_pos+TxtWidth('date: ', used_font), y_pos), (second_col, 'normal'), dwg, used_font)
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
	AddTxt(context['username'], (10, y_pos), (main_col, 'bold'), dwg, used_font)
	AddTxt('@', (10+TxtWidth(context['username'], used_font), y_pos), (second_col, 'normal'), dwg, used_font)
	AddTxt(context['pc_name']+':', (10+TxtWidth(context['username']+'@', used_font), y_pos), (main_col, 'bold'), dwg, used_font)
	AddTxt('~$', (10+TxtWidth(f"{context['username']}@{context['pc_name']}:", used_font), y_pos), (second_col, 'bold'), dwg, used_font)

	blinktxt = dwg.text('|', insert=(10+TxtWidth(f"{context['username']}@{context['pc_name']}:~$  ", used_font), y_pos), fill=main_col, font_weight='bold', font_family=used_font, class_='blink')
	dwg.add(blinktxt)

	if need_animate_css == True:
		dwg = AddCss('blink_and_animate', dwg)
	else:
		dwg = AddCss('blink', dwg)

	return Response(dwg, mimetype='image/svg+xml')
