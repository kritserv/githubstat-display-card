def AddTxt(txt, pos, col_weight, dwg):
	color, weight = col_weight
	dwg.add(dwg.text(txt, insert=pos, fill=color, font_weight=weight, font_family='Arial'))

def AddRect(pos, size, color, dwg):
	dwg.add(dwg.rect(insert=pos, size=size, fill=color))