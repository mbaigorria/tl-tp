from xml.etree import ElementTree as et
from dibu import *

class SemanticException(Exception):
    pass

class Expression(object):

	def evaluate(self):
		# Aca se implementa cada tipo de expresion.
		raise NotImplementedError

class Start(Expression):

	def __init__(self, expressions):
		self.expressions = expressions

	def evaluate(self):
		tree_expressions = self.expressions.evaluate()
		tree_expressions.reverse()

		# for e in tree_expressions:
		# 	print e

		svg = SVG(tree_expressions)
		result = svg.generateSVG();

		return result

class ExpressionList(Expression):

	def __init__(self, function_id, argument_list, next_expression):
		self.function_id = function_id;
		self.argument_list = argument_list;
		self.next_expression = next_expression;

	def evaluate(self, size_defined = False):

		function_id     = self.function_id
		argument_list   = self.argument_list.evaluate()
		next_expression = self.next_expression.evaluate()

		global f

		# check if function exists
		if not f.functionExists(function_id):
			raise SemanticException("Non-existant function "+function_id+".")

		# check if size was already defined
		if function_id == "size":
			if size_defined:
				raise SemanticException("Size was already defined.")
			else:
				size_defined = True

		# check if mandatory attributes are defined
		attribute_types = [x[0] for x in argument_list]
		mandatoryAttributes = [x[0] for x in f.getMandatoryAttributes(function_id)]
		for attribute in mandatoryAttributes:
			if attribute not in attribute_types:
				raise SemanticException("Missing attribute "+attribute+" in "+function_id+".")

		# check if all attributes are valid
		attribute_types = [x[0] for x in argument_list]
		mandatoryAttributes = [x[0] for x in f.getAllAttributes(function_id)]
		for attribute in attribute_types:
			if attribute not in mandatoryAttributes:
				print function_id
				print attribute
				raise SemanticException("Attribute "+attribute+" is invalid.")

		# check no attributes are defined twice
		attribute_types = [x[0] for x in argument_list]
		unique_attributes = set(attribute_types);
		for attribute in attribute_types:
			if attribute in unique_attributes:
				unique_attributes.remove(attribute)
			else:
				raise SemanticException("Multiple definitions of attribute "+attribute+".")

		# check if all attribute types are valid
		possible_attributes = f.getAllAttributes(function_id)
		for attribute_name, attribute_values in argument_list:
			if attribute_name == "style":
				style_attributes = f.getStyleAttributes()
				for name, value in attribute_values:
					if (name, value['type']) not in style_attributes:
						raise SemanticException("Invalid style attribute type for "+name+".")
			elif f.getAttributeType(function_id, attribute_name) == 'point':
				for chord in attribute_values:
					if chord != 'type' and attribute_values[chord]['type'] is not 'number':
						raise SemanticException("Invalid attribute type for "+chord['value']+".")
			elif f.getAttributeType(function_id, attribute_name) == 'array':
				pass
				#todo
			else:
				attribute = (attribute_name, attribute_values['type'])
				if attribute not in possible_attributes:
					raise SemanticException("Invalid attribute type for "+attribute[0]+".")

		# semantic checks done
		expression_list = self.next_expression.evaluate()
		expression_list.append((function_id, argument_list))
		return expression_list

class EmptyExpression(Expression):

	def __init__(self):
		pass

	def evaluate(self):
		return [];

class ArgumentList(Expression):

	def __init__(self, function_id, variable):
		self.function_id = function_id
		self.variable    = variable

	def evaluate(self):
		function_id = self.function_id
		variable    = self.variable.evaluate()

		arg_list = []
		arg_list.append((function_id, variable))
		return arg_list

class ArgumentAppend(Expression):

	def __init__(self, function_id, variable, argument_list):
		self.function_id   = function_id
		self.variable      = variable
		self.argument_list = argument_list

	def evaluate(self):
		function_id = self.function_id
		variable = self.variable.evaluate()

		argument_list = self.argument_list.evaluate()

		argument_list.append((function_id, variable))

		return list(argument_list)

class StyleList(Expression):

	def __init__(self, function_id, variable):
		self.function_id = function_id
		self.variable    = variable

	def evaluate(self):
		function_id = self.function_id
		variable    = self.variable.evaluate()

		arg_list = []
		arg_list.append((function_id, variable))
		return arg_list

class StyleAppend(Expression):

	def __init__(self, function_id, variable, argument_list):
		self.function_id = function_id
		self.variable = variable
		self.argument_list = argument_list

	def evaluate(self):
		function_id = self.function_id
		argument_list = self.argument_list.evaluate()
		variable = self.variable.evaluate()

		argument_list.append((function_id, variable))

		return list(argument_list)

class ID(Expression):

	def __init__(self, value):
		self.value = value;

	def evaluate(self):
		return {'value': self.value, 'type': 'string'}

class Number(Expression):

	def __init__(self, value):
		self.value = value;

	def evaluate(self):
		return {'value': self.value, 'type': 'number'}

class String(Expression):

	def __init__(self, value):
		self.value = value;

	def evaluate(self):
		return {'value': self.value, 'type': 'string'}

class Point(Expression):

	def __init__(self, x, y):
		self.x = x;
		self.y = y;

	def evaluate(self):
		return {'x': self.x.evaluate(), 'y': self.y.evaluate(), 'type': 'point'}

class Array(Expression):

	def __init__(self, variable_list):
		self.variable_list = variable_list

	def evaluate(self):
		value = self.variable_list.evaluate();
		return {'value': list(value), 'type': 'array'} 

class VariableList(Expression):

	def __init__(self, variable):
		self.variable = variable;

	def evaluate(self):
		value = []
		value.append(self.variable.evaluate())
		return list(value)

class VariableAppend(Expression):

	def __init__(self, variable_list, variable):
		self.variable_list = variable_list
		self.variable = variable;

	def evaluate(self):
		variable_list = self.variable_list.evaluate()
		variable = self.variable.evaluate()

		variable_list.append(variable)
		return variable_list

