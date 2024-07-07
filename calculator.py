from decimal import Decimal
import math
import copy

glob_pi = Decimal('3.1415926535897932384626433833')


class Quantity:
	"""The creation of the Quantity object and the related functionality."""

	class OperationError(ArithmeticError):
		pass

	def __init__(self, value, units):
		"""The initialiser for the class.

		Arguments:
		value -- a number representing the numeric value of a quantity,
		units -- a dictionary that matches units and their powers.
		"""
		self.units = units
		self.value = value

	@classmethod
	def usr_init(cls, value, degree=False):
		"""An initialiser for angle quantities.

		>>> Quantity.angle(5)
		Q(5, ang)
		>>> Quantity.angle(1, 'degree')
		Q(0.0175, ang)
		"""
		if degree:
			return cls(value / Dec(180) * glob_pi, {'ang': 1})
		return cls(value, {'ang': 1})

	def __str__(self):
		"""Return a string representation of the quantity's unit part."""
		ans = ''
		for u in list(self.units):
			power = self.units[u]
			ans += str(u)
			if power != 1:
				ans += '^' + str(power)
			ans += '*'
		return ans[:-1]

	def getpow(self, unit):
		"""Return the power in which unit is present in the quantity."""
		if unit in self.units:
			return self.units[unit]
		return 0

	def __mul__(self, other):
		if isinstance(other, Quantity):
			units = {}
			for u in list(self.units | other.units):
				power = self.getpow(u) + other.getpow(u)
				if power != 0:
					units[u] = power
			value = self.value * other.value
			if units:
				return Quantity(value, units)
			return value
		return Quantity(self.value * other, self.units)

	def __truediv__(self, other):
		if isinstance(other, Quantity):
			units = {}
			for u in list(self.units | other.units):
				power = self.getpow(u) - other.getpow(u)
				if power != 0:
					units[u] = power
			value = self.value * other.value
			if units:
				return Quantity(value, units)
			return value
		return Quantity(self.value * other, self.units)

	def __add__(self, other):
		if isinstance(other, Quantity):
			if self.units == other.units:
				return Quantity(self.value + other.value, self.units)
		raise Quantity.OperationError('addition of different units')

	def __neg__(self):
		return Quantity(-self.value, self.units)

	def __sub__(self, other):
		if isinstance(other, Quantity):
			if self.units == other.units:
				return Quantity(self.value - other.value, self.units)
		raise Quantity.OperationError('subtraction of different units')

	def __rmul__(self, other):
		return self * other

	def __rtruediv__(self, other):
		return other * Quantity(Decimal(1), {}) / self

	def __radd__(self, other):
		raise Quantity.OperationError('addition of different units')

	def __rsub__(self, other):
		raise Quantity.OperationError('subtraction of different units')

	def __round__(self, num):
		return Quantity(round(self.value, num), self.units)

	def __pow__(self, other, opt=None):
		if isinstance(other, (int, Dec)):
			raise Quantity.OperationError('raising to a (quantity) power')
		units = {a: self.units[a] * other for a in list(self.units)}
		return Quantity(self.value ** other, units)

	def __repr__(self):
		if self.value == 1:
			return f'Q({str(self)})'
		return f'Q({str(self.value)}, {str(self)})'

	def cos(self):
		"""Return the cosine of the angle."""
		if isinstance(self, Decimal):
			self = Quantity.angle(self)
		elif self.units != {'ang': 1}:
			raise Quantity.OperationError('trigonometry of non-angle quantities')
		x = self.value
		decimal.getcontext().prec += 2
		i, lasts, s, fact, num, sign = 0, 0, 1, 1, 1, 1
		while s != lasts:
			lasts = s
			i += 2
			fact *= i * (i-1)
			num *= x * x
			sign *= -1
			s += num / fact * sign
		decimal.getcontext().prec -= 2
		return +s

	def sin(self):
		"""Return the sine of the angle."""
		if isinstance(self, Decimal):
			self = Quantity.angle(self)
		elif self.units != {'ang': 1}:
			raise Quantity.OperationError('trigonometry of non-angle quantities')
		x = self.value
		decimal.getcontext().prec += 2
		i, lasts, s, fact, num, sign = 1, 0, x, 1, x, 1
		while s != lasts:
			lasts = s
			i += 2
			fact *= i * (i-1)
			num *= x * x
			sign *= -1
			s += num / fact * sign
		decimal.getcontext().prec -= 2
		return +s

	def tan(self):
		"""Return the tangene of the angle."""
		if not isinstance(self, Quantity):
			self = Quantity.angle(self)
		return self.sin() / self.cos()

	def cot(self):
		"""Return the cotangene of the angle."""
		if not isinstance(self, Quantity):
			self = Quantity.angle(self)
		return self.cos() / self.sin()

	def arcsin(x):
		"""Return an angle with given sine."""
		return Quantity.angle(Dec(math.asin(x)))

	def arccos(x):
		"""Return an angle with given cosine."""
		return Quantity.angle(Dec(math.acos(x)))

	def arctan(x):
		"""Return an angle with given tangene."""
		return Quantity.angle(Dec(math.atan(x)))


class Token:
	"""The creation of the Token object and the related functionality."""

	def __init__(self, calc, arg_num, pref, ltor, kind='', name=''):
		"""The initialiser of the class.

		Arguments:
		calc -- the token's function,
		arg_num -- number of arguments of calc,
		pref -- the token's preference,
		ltor -- a truthy value, if tokens with the same pref
		  should be calculated left-to-right, falsy otherwise,
		kind -- the kind of the token (optional),
		name -- the name of the token (optional).
		"""
		self.name = name
		self.calc = calc
		self.arg_num = arg_num
		self.pref = pref
		self.ltor = ltor
		self.kind = kind
		self.name = name

	def give(obj):
		def func():
			return copy.copy(obj)
		return func

	def __repr__(self):
		if self.name:
			return self.name
		if self.arg_num == 0:
			return str(self.calc())
		if self.kind:
			return self.kind
		return '<?>'


glob_funcs = {
	'+': Token(lambda a, b: a + b,   2, 1, 0, 'oper', '<ADD>'),
	'-': Token(lambda a, b: a - b,   2, 1, 0, 'oper', '<SUB>'),
	'*': Token(lambda a, b: a * b,   2, 2, 0, 'oper', '<MUL>'),
	':': Token(lambda a, b: a / b,   2, 2, 0, 'oper', '<DIV>'),
	'/': Token(lambda a, b: a / b,   2, 0, 0, 'oper', '<BAR>'),
	'^': Token(lambda a, b: a ** b,  2, 3, 1, 'oper', '<POW>'),
	'neg': Token(lambda a: -a,       1, 3, 1, 'oper', '<NEG>'),
	'dot': Token(lambda a, b: a * b, 2, 3, 1, 'oper', '<DOT>'),
	'sin': Token(lambda a: Quantity.sin(a), 1, 3, 1, 'trig', '<sin>'),
	'cos': Token(lambda a: Quantity.cos(a), 1, 3, 1, 'trig', '<cos>'),
	'tan': Token(lambda a: Quantity.tan(a), 1, 3, 1, 'trig', '<tan>'),
}

glob_pth = {
	'(': Token(lambda: None, 0, 10, 0, "'('", "'('"),
	')': Token(lambda: None, 0, 10, 0, "')'", "')'")
}

glob_trigpow = {
	'sin': Token(lambda a, b: Quantity.sin(a) ** b, 1, 3, 1, 'func', '<sin^>'),
	'cos': Token(lambda a, b: Quantity.cos(a) ** b, 1, 3, 1, 'func', '<cos^>'),
	'tan': Token(lambda a, b: Quantity.tan(a) ** b, 1, 3, 1, 'func', '<tan^>'),
}


class Calculator:
	"""The creation of the Calculator object and the related functionality."""

	def __init__(self):
		"""The initialiser of the class."""
		self.vars = {}

	def list_of_strings(self, string):
		"""Split the given string expression."""
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
		if ans[-1]:
			return ans
		return ans[:-1]

	def list_of_tokens(self, ls):
		"""Transform a list of strings to a list of Token objects."""
		ans = []
		for word in ls:
			if word[0] in '()':
				ans.append(glob_pth[word])
			elif word[0] == '"':
				ans.append(Token(Token.give(word), 0, 10, 0, kind='str'))
			elif word.isdigit() or '.' in word:
				num = Decimal(word)
				ans.append(Token(Token.give(num), 0, 10, 0, kind='num'))
			elif word in glob_funcs:
				ans.append(glob_funcs[word])
			elif word[0].isalpha():
				get = Token.give(None)
				if word in self.vars:
					get = Token.give(self.vars[word])
				ans.append(Token(get, 0, 10, 0, kind='var', name=word))
		return ans

	def infix_notation(self, ls):
		"""Add ommited operators to a list of tokens."""
		last = glob_pth['(']
		ans = []
		for token in ls:
			match (last.kind, token.name):
				case ("'('" | 'oper' | 'func' | 'trig', '<ADD>'):
					pass
				case ("'('" | 'oper' | 'func' | 'trig', '<SUB>'):
					ans.append(glob_funcs['neg'])
				case ('trig', '<POW>'):
					ans[-1] = glob_trigpow(last.name)
				case _:
					match last.kind, token.kind:
						case ('var', 'var' | "'('" | 'num'):
							ans.append(glob_funcs['dot'])
						case ('var' | "')'" | 'num', 'var'):
							ans.append(glob_funcs['dot'])
						case ("')'", "'('"):
							ans.append(glob_funcs['dot'])
					ans.append(token)
			if ans:
				last = ans[-1]
		return ans

ctor = Calculator()
expression = '+ 1 + 3 * 15a (-2)'
print(expression)
expression = ctor.list_of_strings(expression)
print(expression)
expression = ctor.list_of_tokens(expression)
print(expression)
expression = ctor.infix_notation(expression)
print(expression)
