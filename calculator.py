def replace(iterable, rules):
	"""Replace some elements of the given iterable.

	Arguments:
	obj -- the iterable,
	rules -- a dictionary containing the elements to change.
	>>> replace('finger', {'f': 'h', 'g': 'd'})
	hinder
	"""
	new = []
	for el in iterable:
		if el in rules:
			new.append(rules[el])
		else:
			new.append(el)
	iter_type = type(iterable)
	if iter_type is str:
		return ''.join(new)
	return iter_type(new)

class Calculator:
	"""The creation of the Calculator object and the related functionality."""

	def __init__(self):
		"""The initialiser of the class."""
		pass

	def infix_notation(self, string):
		"""Return 'string' as a list of commands in infix notation."""
		string = replace(string, {',': '.'})
		print(string)

calc = Calculator()
calc.infix_notation('test, test, test...')
