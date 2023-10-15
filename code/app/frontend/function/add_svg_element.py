from bs4 import BeautifulSoup, NavigableString

def AddTxt(txt, pos, col_weight, dwg, used_font):
	color, weight = col_weight
	dwg.add(dwg.text(txt, insert=pos, fill=color, font_weight=weight, font_family=used_font.title()))

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
	elif css == 'blink_and_animate':
		CSS = """.blink {animation: blink 1s steps(2, start) infinite;} 
		@keyframes blink { to { visibility: hidden;}}
		.frame1, .frame2, .frame3, .frame4, .frame5, .frame6, .frame7, .frame8, .frame9, .frame0 {position: absolute;}
		.frame1 {animation: f1 3s; animation-iteration-count: infinite;}
		.frame2 {animation: f2 3s; animation-iteration-count: infinite;}
		.frame3 {animation: f3 3s; animation-iteration-count: infinite;}
		.frame4 {animation: f4 3s; animation-iteration-count: infinite;}
		.frame5 {animation: f5 3s; animation-iteration-count: infinite;}
		.frame6 {animation: f6 3s; animation-iteration-count: infinite;}
		.frame7 {animation: f7 3s; animation-iteration-count: infinite;}
		.frame8 {animation: f8 3s; animation-iteration-count: infinite;}
		.frame9 {animation: f9 3s; animation-iteration-count: infinite;}
		.frame0 {animation: f0 3s; animation-iteration-count: infinite;}
		@keyframes f1 {from {visibility: visible;}5% {visibility: hidden;}10% {visibility: hidden;}15% {visibility: hidden;}20% {visibility: hidden;}25% {visibility: hidden;}30% {visibility: hidden;}35% {visibility: hidden;}40% {visibility: hidden;}45% {visibility: hidden;}50% {visibility: hidden;}55% {visibility: hidden;}60% {visibility: hidden;}65% {visibility: hidden;}70% {visibility: hidden;}75% {visibility: hidden;}80% {visibility: hidden;}85% {visibility: hidden;}90% {visibility: hidden;}95% {visibility: hidden;}to {visibility: visible;}}
		@keyframes f2 {from {visibility: hidden;}5% {visibility: hidden;}10% {visibility: visible;}15% {visibility: hidden;}20% {visibility: hidden;}25% {visibility: hidden;}30% {visibility: hidden;}35% {visibility: hidden;}40% {visibility: hidden;}45% {visibility: hidden;}50% {visibility: hidden;}55% {visibility: hidden;}60% {visibility: hidden;}65% {visibility: hidden;}70% {visibility: hidden;}75% {visibility: hidden;}80% {visibility: hidden;}85% {visibility: hidden;}90% {visibility: hidden;}95% {visibility: hidden;}100% {visibility: hidden;}}
		@keyframes f3 {from {visibility: hidden;}5% {visibility: hidden;}10% {visibility: hidden;}15% {visibility: hidden;}20% {visibility: visible;}25% {visibility: hidden;}30% {visibility: hidden;}35% {visibility: hidden;}40% {visibility: hidden;}45% {visibility: hidden;}50% {visibility: hidden;}55% {visibility: hidden;}60% {visibility: hidden;}65% {visibility: hidden;}70% {visibility: hidden;}75% {visibility: hidden;}80% {visibility: hidden;}85% {visibility: hidden;}90% {visibility: hidden;}95% {visibility: hidden;}100% {visibility: hidden;}}
		@keyframes f4 {from {visibility: hidden;}5% {visibility: hidden;}10% {visibility: hidden;}15% {visibility: hidden;}20% {visibility: hidden;}25% {visibility: hidden;}30% {visibility: visible;}35% {visibility: hidden;}40% {visibility: hidden;}45% {visibility: hidden;}50% {visibility: hidden;}55% {visibility: hidden;}60% {visibility: hidden;}65% {visibility: hidden;}70% {visibility: hidden;}75% {visibility: hidden;}80% {visibility: hidden;}85% {visibility: hidden;}90% {visibility: hidden;}95% {visibility: hidden;}100% {visibility: hidden;}}
		@keyframes f5 {from {visibility: hidden;}5% {visibility: hidden;}10% {visibility: hidden;}15% {visibility: hidden;}20% {visibility: hidden;}25% {visibility: hidden;}30% {visibility: hidden;}35% {visibility: hidden;}40% {visibility: visible;}45% {visibility: hidden;}50% {visibility: hidden;}55% {visibility: hidden;}60% {visibility: hidden;}65% {visibility: hidden;}70% {visibility: hidden;}75% {visibility: hidden;}80% {visibility: hidden;}85% {visibility: hidden;}90% {visibility: hidden;}95% {visibility: hidden;}100% {visibility: hidden;}}
		@keyframes f6 {from {visibility: hidden;}5% {visibility: hidden;}10% {visibility: hidden;}15% {visibility: hidden;}20% {visibility: hidden;}25% {visibility: hidden;}30% {visibility: hidden;}35% {visibility: hidden;}40% {visibility: hidden;}45% {visibility: hidden;}50% {visibility: visible;}55% {visibility: hidden;}60% {visibility: hidden;}65% {visibility: hidden;}70% {visibility: hidden;}75% {visibility: hidden;}80% {visibility: hidden;}85% {visibility: hidden;}90% {visibility: hidden;}95% {visibility: hidden;}100% {visibility: hidden;}}
		@keyframes f7 {from {visibility: hidden;}5% {visibility: hidden;}10% {visibility: hidden;}15% {visibility: hidden;}20% {visibility: hidden;}25% {visibility: hidden;}30% {visibility: hidden;}35% {visibility: hidden;}40% {visibility: hidden;}45% {visibility: hidden;}50% {visibility: hidden;}55% {visibility: hidden;}60% {visibility: visible;}65% {visibility: hidden;}70% {visibility: hidden;}75% {visibility: hidden;}80% {visibility: hidden;}85% {visibility: hidden;}90% {visibility: hidden;}95% {visibility: hidden;}100% {visibility: hidden;}}
		@keyframes f8 {from {visibility: hidden;}5% {visibility: hidden;}10% {visibility: hidden;}15% {visibility: hidden;}20% {visibility: hidden;}25% {visibility: hidden;}30% {visibility: hidden;}35% {visibility: hidden;}40% {visibility: hidden;}45% {visibility: hidden;}50% {visibility: hidden;}55% {visibility: hidden;}60% {visibility: hidden;}65% {visibility: hidden;}70% {visibility: visible;}75% {visibility: hidden;}80% {visibility: hidden;}85% {visibility: hidden;}90% {visibility: hidden;}95% {visibility: hidden;}100% {visibility: hidden;}}
		@keyframes f9 {from {visibility: hidden;}5% {visibility: hidden;}10% {visibility: hidden;}15% {visibility: hidden;}20% {visibility: hidden;}25% {visibility: hidden;}30% {visibility: hidden;}35% {visibility: hidden;}40% {visibility: hidden;}45% {visibility: hidden;}50% {visibility: hidden;}55% {visibility: hidden;}60% {visibility: hidden;}65% {visibility: hidden;}70% {visibility: hidden;}75% {visibility: hidden;}80% {visibility: visible;}85% {visibility: hidden;}90% {visibility: hidden;}95% {visibility: hidden;}100% {visibility: hidden;}}
		@keyframes f0 {from {visibility: hidden;}5% {visibility: hidden;}10% {visibility: hidden;}15% {visibility: hidden;}20% {visibility: hidden;}25% {visibility: hidden;}30% {visibility: hidden;}35% {visibility: hidden;}40% {visibility: hidden;}45% {visibility: hidden;}50% {visibility: hidden;}55% {visibility: hidden;}60% {visibility: hidden;}65% {visibility: hidden;}70% {visibility: hidden;}75% {visibility: hidden;}80% {visibility: hidden;}85% {visibility: hidden;}90% {visibility: visible;}95% {visibility: hidden;}100% {visibility: hidden;}}"""
	else:
		pass

	style_tag.append(NavigableString(CSS))

	svg_tag.append(style_tag)
	svg = str(svg_tag)

	return svg