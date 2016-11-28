import ply.lex as lex

class DibuLexer(object):

	class LexicalException(Exception):
		pass

	# list of ts
	tokens = (
		'ID',
		'EQUALS',
		'LPAREN',
		'RPAREN',
		'LBRACKET',
		'RBRACKET',
		'COMMA',
		'NUMBER',
		'STRING',
		'QUOTATION_MARK',
		'COLON',
		'SEMICOLON'
	)

	# regular expression rules for simple ts
	t_EQUALS = r"="
	t_LPAREN = r"\("
	t_RPAREN = r"\)"
	t_LBRACKET = r"\["
	t_RBRACKET = r"\]"
	t_COMMA = r","
	t_QUOTATION_MARK = r"\""
	t_COLON = r":"
	t_SEMICOLON = r";"
	t_ignore = " \t\r"

	def t_ID(self, t):
		r"[_a-zA-Z][\-_a-zA-Z0-9]*"
		return t

	def t_NUMBER(self, t):
		r"[0-9]+(\.[0-9]+)?"
		if t.value.find(".") >= 0:
			t.value = float(t.value)
		else:
			t.value = int(t.value)
		return t

	def t_NEWLINE(self, t):
		r"\n+"
		t.lexer.lineno += len(t.value)

	def t_STRING(self, t):
		r"\"[_a-zA-Z][ _a-zA-Z0-9]*\""
		t.value = t.value[1:-1]
		return t

	def find_column(self, t):
		last_cr = self.code.rfind('\n', 0, t.lexpos)
		if last_cr < 0: last_cr = 0
		column = (t.lexpos - last_cr) + (1 if last_cr == 0 else 0)
		return column

	def t_error(self, t):

		line = t.lineno
		column = self.find_column(t)
		print 'Lexical error at line %d, column %d:' % (line, column)
		print self.code.split('\n')[line - 1]
		print ' ' * (column - 1) + '^'
		raise self.LexicalException()

	def dump_tokens(self, filename):
		t = self.lexer.token()
		output_file = open(filename, "w")

		while t is not None:
			output_file.write("type:" + t.type)
			output_file.write(" value:" + str(t.value))
			output_file.write(" line:" + str(t.lineno))
			output_file.write(" position:" + str(t.lexpos))
			output_file.write("\n")

			t = self.lexer.token()

		output_file.close()

	def input(self, code):
		self.code = code

	def lex(self, code):
		self.lexer.input(code)

	def __init__(self, code):
		self.code = code;
		self.lexer = lex.lex(module=self)

if __name__ == "__main__":

	code = "size height=30, width=200 text t=\"I love Dibu\", at=(0,15), fill=\"red\"";

	m = DibuLexer(code)
	m.lex(code)
	m.dump_tokens("test.txt")