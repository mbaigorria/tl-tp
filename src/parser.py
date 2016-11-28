from ply import yacc
from lexer import DibuLexer
from dibu import AvailableFunctions

from expressions import *
from xml.dom.minidom import parseString as xmlParse
from sys import argv, exit

class DibuParser(object):

	start = 'start'

	tokens = DibuLexer.tokens

	class SyntaxException(Exception):
		pass

	def p_start(self, subexpressions):
		'start : expression'
		subexpressions[0] = Start(subexpressions[1], self.availableFunctions)

	def p_expression(self, subexpressions):
		'expression : ID argument_list expression'
		subexpressions[0] = ExpressionList(subexpressions[1], subexpressions[2], subexpressions[3], self.availableFunctions)

	def p_expression_empty(self, subexpressions):
		'expression :'
		subexpressions[0] = EmptyExpression();

	def p_argument_list_single(self, subexpressions):
		'argument_list : ID EQUALS type_value'
		subexpressions[0] = ArgumentList(subexpressions[1], subexpressions[3])

	def p_argument_list_append(self, subexpressions):
		'argument_list : argument_list COMMA ID EQUALS type_value'
		subexpressions[0] = ArgumentAppend(subexpressions[3], subexpressions[5], subexpressions[1])

	def p_type_value(self, subexpressions):
		'type_value : variable'
		subexpressions[0] = subexpressions[1]

	def p_type_value_style(self, subexpressions):
		'type_value : QUOTATION_MARK argl_style QUOTATION_MARK'
		subexpressions[0] = subexpressions[2]

	def p_argument_list_style_single(self, subexpressions):
		'argl_style : ID COLON style_var SEMICOLON'
		subexpressions[0] = StyleList(subexpressions[1], subexpressions[3])

	def p_argument_list_style_append(self, subexpressions):
		'argl_style : argl_style ID COLON style_var SEMICOLON'
		subexpressions[0] = StyleAppend(subexpressions[2], subexpressions[4], subexpressions[1])

	def p_argl_style_string(self, subexpressions):
		'style_var : ID'
		subexpressions[0] = ID(subexpressions[1])

	def p_argl_style_num(self, subexpressions):
		'style_var : NUMBER'
		subexpressions[0] = Number(subexpressions[1])

	def p_variable_number(self, subexpressions):
		'variable : NUMBER'
		subexpressions[0] = Number(subexpressions[1])

	def p_variable_string(self, subexpressions):
		'variable : STRING'
		subexpressions[0] = String(subexpressions[1])

	def p_variable_point(self, subexpressions):
		'variable : LPAREN variable COMMA variable RPAREN'
		subexpressions[0] = Point(subexpressions[2], subexpressions[4])

	def p_variable_array(self, subexpressions):
		'variable : LBRACKET variable_list RBRACKET'
		subexpressions[0] = Array(subexpressions[2])

	def p_variable_list_one(self, subexpressions):
		'variable_list : variable'
		subexpressions[0] = VariableList(subexpressions[1])

	def p_variable_list_append(self, subexpressions):
		'variable_list : variable_list COMMA variable'
		subexpressions[0] = VariableAppend(subexpressions[1], subexpressions[3])

	def find_column(self, t):
		last_cr = self.code.rfind('\n', 0, t.lexpos)
		if last_cr < 0: last_cr = 0
		column = (t.lexpos - last_cr) + (1 if last_cr == 0 else 0)
		return column

	def p_error(self, t):

		line = t.lineno
		column = self.find_column(t)
		print 'Parse error at line %d, column %d:' % (line, column)
		print self.code.split('\n')[line - 1]
		print ' ' * (column - 1) + '^'
		raise self.SyntaxException()

	def parse(self, code):
		self.code = code
		return self.parser.parse(code, lexer=self.lexer.lexer)

	def __init__(self, code):
		self.availableFunctions = AvailableFunctions()
		self.code = code
		self.lexer = DibuLexer(code)
		self.parser = yacc.yacc(module=self)

if __name__ == "__main__":

	if len(argv) != 3:
		print "Invalid arguments."
		print "Use:"
		print "  parser.py input.dibu output.svg"
		exit()

	filename = argv[1]
	outfile  = argv[2]

	input_file = open(filename, "r")
	code = input_file.read()
	input_file.close()

	parser = DibuParser(code)

	try:
		expression = parser.parse(code)
	except DibuParser.SyntaxException as exception:
		print str(exception)
		exit()
	except DibuLexer.LexicalException as exception:
		print str(exception)
		exit()
	else:
		print "Syntax is valid."

	output = expression.evaluate()

	pretty_xml = xmlParse(output).toprettyxml();
	    
	output_file = open(outfile, "w")
	output_file.write(pretty_xml)
	output_file.close()

	print "SVG Generated!"