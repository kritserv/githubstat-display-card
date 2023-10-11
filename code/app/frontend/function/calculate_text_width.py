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

def TxtWidth(txt):
	total_length = 0
	for char in txt:
		for length in Arial_dict_size:
			if char in Arial_dict_size[length]:
				total_length+=length
	return total_length

