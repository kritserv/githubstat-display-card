from bs4 import BeautifulSoup, NavigableString

def AddTxt(txt, pos, col_weight, dwg):
	color, weight = col_weight
	dwg.add(dwg.text(txt, insert=pos, fill=color, font_weight=weight, font_family='Arial'))

def AddRect(pos, size, color, dwg):
	dwg.add(dwg.rect(insert=pos, size=size, fill=color))

def AddCss(css, dwg):
	html_string = dwg.tostring()
	soup = BeautifulSoup(html_string, 'html.parser')
	svg_tag = soup.find('svg')

	style_tag = soup.new_tag('style')

	if css == 'blink':
		CSS = """.blink {animation: blink 1s steps(2, start) infinite;} 
		@keyframes blink { to { visibility: hidden;}}"""
	else:
		pass

	style_tag.append(NavigableString(CSS))

	svg_tag.append(style_tag)
	svg = str(svg_tag)

	return svg