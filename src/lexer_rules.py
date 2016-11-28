import ply.lex as lex

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

def t_ID(token):
    r"[_a-zA-Z][\-_a-zA-Z0-9]*"
    return token

def t_NUMBER(token):
    r"[0-9]+(\.[0-9]+)?"
    if token.value.find(".") >= 0:
        token.value = float(token.value)
    else:
        token.value = int(token.value)
    return token

def t_NEWLINE(token):
    r"\n+"
    token.lexer.lineno += len(token.value)
    print "[%s]" % len(token.value)

def t_STRING(token):
	r"\"[_a-zA-Z][ _a-zA-Z0-9]*\""
	token.value = token.value[1:-1]
	return token

t_EQUALS = r"="
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_COMMA = r","
t_QUOTATION_MARK = r"\""
t_COLON = r":"
t_SEMICOLON = r";"

t_ignore = " \t"

def t_error(token):
    message = "Token desconocido:"
    message += "\ntype:" + token.type
    message += "\nvalue:" + str(token.value)
    message += "\nline:" + str(token.lineno)
    message += "\nposition:" + str(token.lexpos)
    raise Exception(message)

# Build the lexer
lexer = lex.lex()

def dump_tokens(lexer, output_file):
    token = lexer.token()
    
    while token is not None:
        output_file.write("type:" + token.type)
        output_file.write(" value:" + str(token.value))
        output_file.write(" line:" + str(token.lineno))
        output_file.write(" position:" + str(token.lexpos))
        output_file.write("\n")

        token = lexer.token()

if __name__ == "__main__":

	code = "size height=30, width=200 text t=\"I love Dibu\", at=(0,15), fill=\"red\"";

	lexer.input(code)

	output_file = open("test.txt", "w")
	output_file.write(code)
	dump_tokens(lexer, output_file)
	output_file.close()
