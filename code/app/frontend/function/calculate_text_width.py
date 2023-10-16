Arial_dict_size = {
	4 : ['i', 'l'],
	5 : ['j', 't', 'I', '\\', '/', '!', '[', ']', ' ', '.', ':'],
	6 : ['f', '-', '(', ')', '"', '}', '{'],
	7 : ['r', '*'],
	8 : ['^'],
	9 : ['c', 'k', 's', 'v', 'x', 'y', 'z', 'J'],
	10 : ['a', 'b', 'd', 'e', 'g', 'h', 'n', 'o', 'p', 'q', 'u', 'L', '#', '?', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
	11 : ['F', 'T', 'Z', '+', '=', '>', '<'],
	12 : ['B', 'E', 'K', 'P', 'S', 'V', 'X', 'Y', '&', '_', '&'],
	13 : ['w', 'C', 'D', 'H', 'N', 'R', 'U'],
	14 : ['A', 'G', 'O', 'Q', '★'],
	15 : ['m', 'M'],
	16 : ['%'],
	17 : ['W'],
	18 : ['@', '$']
}

Monospace_dict_size = {8: ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z', '\\', '/', '&', '*', '+', '-', '_', '#', '$', '!', '%', '^', '&', '(', ')', '=', '?', '>', '<', '"', '}', '{', '[', ']', '★', ':', ' ', '.', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], 9: ['m', 'U', '@']}

def TxtWidth(txt, used_font):
	total_length = 0
	if used_font == 'arial':
		used_dict = Arial_dict_size
	elif used_font == 'monospace':
		used_dict = Monospace_dict_size
	for char in txt:
		for length in used_dict:
			if char in used_dict[length]:
				total_length+=length
	return total_length