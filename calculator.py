class Token:
	"""The creation of the Token object and the related functionality."""
	
	def __init__(self, calc, arg_num, pref, ltor, name='', kind=''):
		"""The initialiser of the class.
		
		Arguments:
		calc -- the token's function,
		arg_num -- number of arguments of calc,
		pref -- the token's preference,
		ltor -- a truthy value, if tokens with the same pref
		  should be calculated left-to-right, falsy otherwise,
		name -- the name of the token (optional),
		kind -- the kind of the token (optional).
		"""
		self.name = name
		self.calc = calc
		self.arg_num = arg_num
		self.pref = pref
		self.ltor = ltor
		self.name = name
		self.kind = kind
	
	@classmethod
	def number(cls, number):
		return cls((lambda: number), 0, 10, 0, kind='num')
	
	@classmethod
	def variable(cls, name, known_vars):
		return cls((lambda: known_vars[name]), 0, 10, 0, name=name, kind='var')
	
	def __repr__(self):
		if self.name:
			return self.name
		if self.arg_num == 0:
			return str(self.calc())
		if self.kind:
			return self.kind
		return '<TOKEN>'


class Calculator:
	"""The creation of the Calculator object and the related functionality."""

	def __init__(self):
		"""The initialiser of the class."""
		pass

	def split_string(self, string):
		"""Split the given string by tokens."""
		changes = {'⋅': '*', '×': '*',
			'÷': ':', '{': '(', '}': ')'}
		ans = ['']
		in_string = False
		for char in string:
			if char == '"':
				in_string = not in_string
				ans[-1] += char
			elif in_string:
				ans[-1] += char
			elif (ans[-1] + char).isalpha() or char.isdigit():
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
		if in_string:
			raise ValueError('unclosed double quotes')
		return ans

	def transform_operators(self, ls):
		for el in ls:
			pass

	def infix_notation(self, ls):
		"""Return 'ls' as a list of commands in infix notation."""

calc = Calculator()
print(calc.split_string('1 + 2 - "1 + 2" + "12 - 345"'))
