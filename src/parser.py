import lexer_rules
import parser_rules

from sys import argv, exit

from ply.lex import lex
from ply.yacc import yacc

from xml.dom.minidom import parseString as xmlParse

if __name__ == "__main__":
    if len(argv) != 2:
        print "Invalid arguments."
        print "Use:"
        print "  parser.py input.dibu output.svg"
        exit()

    filename = argv[1]
    outfile  = argv[2]

    input_file = open(filename, "r")
    code = input_file.read()
    input_file.close()

    lexer = lex(module=lexer_rules)
    parser = yacc(module=parser_rules)

    try:
        expression = parser.parse(text, lexer)
    except parser_rules.SemanticException as exception:
        print "Semantic error: " + str(exception)
    else:
        print "Syntax is valid."

    output     = expression.evaluate()

    pretty_xml = xmlParse(output).toprettyxml();
    
    output_file = open(outfile, "w")
    output_file.write(pretty_xml)
    output_file.close()

    print "SVG Generated!"