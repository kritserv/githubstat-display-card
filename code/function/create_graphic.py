import svgwrite

def DrawSVG(context):

	display_text = ['Image', 'Last yr Contrib', 'Total Stars', 'Language']

	dwg = svgwrite.Drawing('github_stats.svg', profile='tiny')

	dwg.add(dwg.text(f"{context['username']}", insert=(0, 20)))
	del context['username']

	dwg.add(dwg.text(f"Theme: {context['theme']}", insert=(0, 40)))
	del context['theme']

	i = 0
	y_pos = 20

	for key in context:
		dwg.add(dwg.text(f"{display_text[i]}: {context[key]}", insert=(100, y_pos)))
		y_pos += 20
		i += 1

	return dwg.tostring()