from decimal import Decimal

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
	def obj(cls, kind, obj):
		"""An initialiser for data storage tokens."""
		return cls((lambda: obj), 0, 10, 0, kind=kind)
	
	@classmethod
	def var(cls, name, defined):
		"""An initialiser for variable and value tokens."""
		return cls((lambda: defined[name]), 0, 10, 0, name=name, kind='var')
	
	def __repr__(self):
		if self.name:
			return self.name
		if self.arg_num == 0:
			return str(self.calc())
		if self.kind:
			return self.kind
		return '<TOKEN>'


glob_opers = {
	'+': Token(lambda a, b: a + b, 2, 1, 0, name='<ADD>'),
	'-': Token(lambda a, b: a - b, 2, 1, 0, name='<SUB>'),
	'*': Token(lambda a, b: a * b, 2, 2, 0, name='<MUL>'),
	':': Token(lambda a, b: a / b, 2, 2, 0, name='<DIV>'),
	'/': Token(lambda a, b: a / b, 2, 0, 0, name='<BAR>'),
	'^': Token(lambda a, b: a ** b, 2, 3, 1, name='<POW>'),
	'~': Token(lambda a: -a, 2, 3, 1, name='<NEG>'),
}

glob_funcs = {}


class Calculator:
	"""The creation of the Calculator object and the related functionality."""

	def __init__(self):
		"""The initialiser of the class."""
		self.vars = {}

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
			elif char in '.,' and (ans[-1] + '0').isdigit():
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
		ans = []
		for word in ls:
			if word.isdigit() or '.' in word:
				ans.append(Token.obj('num', Decimal(word)))
			elif word[0] == '"':
				ans.append(Token.obj('str', word))
			elif word in glob_opers:
				ans.append(glob_opers[word])
			elif word in glob_funcs:
				ans.append(glob_funcs[word])
			elif word[0].isalpha():
				ans.append(Token.var(word, self.vars))
		return ans

	def infix_notation(self, ls):
		"""Return 'ls' as a list of commands in infix notation."""

calc = Calculator()
expression = '30.3 - 20,2 * i1'
expression = calc.split_string(expression)
print(expression)
expression = calc.transform_operators(expression)
print(expression)
