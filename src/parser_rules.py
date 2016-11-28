from lexer_rules import tokens
from expressions import *

start = 'start'

def p_start(subexpressions):
	'start : expression'
	subexpressions[0] = Start(subexpressions[1])

def p_expression(subexpressions):
	'expression : ID argument_list expression'
	subexpressions[0] = ExpressionList(subexpressions[1], subexpressions[2], subexpressions[3])

def p_expression_empty(subexpressions):
	'expression :'
	subexpressions[0] = EmptyExpression();

def p_argument_list_single(subexpressions):
	'argument_list : ID EQUALS type_value'
	subexpressions[0] = ArgumentList(subexpressions[1], subexpressions[3])

def p_argument_list_append(subexpressions):
	'argument_list : argument_list COMMA ID EQUALS type_value'
	subexpressions[0] = ArgumentAppend(subexpressions[3], subexpressions[5], subexpressions[1])

def p_type_value(subexpressions):
	'type_value : variable'
	subexpressions[0] = subexpressions[1]

def p_type_value_style(subexpressions):
	'type_value : QUOTATION_MARK argl_style QUOTATION_MARK'
	subexpressions[0] = subexpressions[2]

def p_argument_list_style_single(subexpressions):
	'argl_style : ID COLON style_var SEMICOLON'
	subexpressions[0] = StyleList(subexpressions[1], subexpressions[3])

def p_argument_list_style_append(subexpressions):
	'argl_style : argl_style ID COLON style_var SEMICOLON'
	subexpressions[0] = StyleAppend(subexpressions[2], subexpressions[4], subexpressions[1])

def p_argl_style_string(subexpressions):
	'style_var : ID'
	subexpressions[0] = ID(subexpressions[1])

def p_argl_style_num(subexpressions):
	'style_var : NUMBER'
	subexpressions[0] = Number(subexpressions[1])

def p_variable_number(subexpressions):
	'variable : NUMBER'
	subexpressions[0] = Number(subexpressions[1])

def p_variable_string(subexpressions):
	'variable : STRING'
	subexpressions[0] = String(subexpressions[1])

def p_variable_point(subexpressions):
	'variable : LPAREN variable COMMA variable RPAREN'
	subexpressions[0] = Point(subexpressions[2], subexpressions[4])

def p_variable_array(subexpressions):
	'variable : LBRACKET variable_list RBRACKET'
	subexpressions[0] = Array(subexpressions[2])

def p_variable_list_one(subexpressions):
	'variable_list : variable'
	subexpressions[0] = VariableList(subexpressions[1])

def p_variable_list_append(subexpressions):
	'variable_list : variable_list COMMA variable'
	subexpressions[0] = VariableAppend(subexpressions[1], subexpressions[3])

def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
