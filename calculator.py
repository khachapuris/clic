class Calculator:
	"""The creation of the Calculator object and the related functionality."""

	def __init__(self):
		"""The initialiser of the class."""
		pass

	def split_string(self, string):
		changes = {'⋅': '*', '×': '*',
			'÷': ':', '{': '(', '}': ')'}
		ans = ['']
		for char in string:
			if (ans[-1] + char).isalpha() or char.isdigit():
				ans[-1] += char
			elif char in '.,':
				ans[-1] += '.'
			elif char == ' ':
				if ans[-1]:
					ans.append('')
			else:
				if char in changes:
					char = changes[char]
				if ans[-1]:
					ans.append(char)
				else:
					ans[-1] += char
				ans.append('')
		return ans

	def infix_notation(self, ls):
		"""Return 'ls' as a list of commands in infix notation."""

calc = Calculator()
print(calc.split_string('{ (1+2,33) * 11s : i1} - sin 1'))
