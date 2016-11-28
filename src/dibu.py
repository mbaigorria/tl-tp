from xml.etree import ElementTree as et

class AvailableFunctions(object):
	"""Define available functions in our language."""

	def __init__(self):

		self.d = {}
		self.optionalAttributes = {}
		self.generalAttributes  = {}
		self.styleAttributes    = {}

		# these codes are used since the XML in the SVG
		# functions does not necessarily match the function name
		self.functionCodes  = {}
		self.attributeCodes = {}

		# define available functions
		self.add('size');
		self.addAttribute('size', 'height', 'number');
		self.addAttribute('size', 'width',  'number');

		self.add('rectangle', 'rect');
		self.addAttribute('rectangle', 'upper_left', 'point');
		self.addAttribute('rectangle', 'size',  'point');

		self.add('line');
		self.addAttribute('line', 'from', 'point');
		self.addAttribute('line', 'to', 'point');

		self.add('circle');
		self.addAttribute('circle', 'center', 'point');
		self.addAttribute('circle', 'radius', 'number', 'r');

		self.add('ellipse');
		self.addAttribute('ellipse', 'center', 'point');
		self.addAttribute('ellipse', 'rx', 'number');
		self.addAttribute('ellipse', 'ry', 'number');

		self.add('polyline');
		self.addAttribute('polyline', 'points', 'array');

		self.add('polygon');
		self.addAttribute('polygon', 'points', 'array');

		self.add('text');
		self.addAttribute('text', 't', 'string');
		self.addAttribute('text', 'at', 'point');
		# optional
		self.addOptionalAttribute('text', 'font-familly', 'string');
		self.addOptionalAttribute('text', 'font-size', 'string');

		self.addGeneralAttribute('style', 'list')
		self.addGeneralAttribute('fill', 'string')
		self.addGeneralAttribute('stroke', 'string')
		self.addGeneralAttribute('stroke-width', 'number')

		self.addStyleAttribute('fill', 'string')
		self.addStyleAttribute('stroke', 'string')
		self.addStyleAttribute('stroke-width', 'number')

	def print_functions(self):
		print self.d;

	def add(self, function_name, function_code = False):
		if function_name not in self.d:
			self.d[function_name] = {}
		if function_name not in self.optionalAttributes:
			self.optionalAttributes[function_name] = {}
		if function_code:
			self.functionCodes[function_name] = function_code;

	def addAttribute(self, function_name, attribute_name, attribute_type, attribute_code = False):
		if function_name not in self.d:
			raise ValueError("You must first add the function "+function_name+".")
		self.d[function_name][attribute_name] = attribute_type;
		if attribute_code:
			if function_name not in self.attributeCodes:
				self.attributeCodes[function_name] = {}
			self.attributeCodes[function_name][attribute_name] = attribute_code

	def addOptionalAttribute(self, function_name, attribute_name, attribute_type):
		self.optionalAttributes[function_name][attribute_name] = attribute_type;

	def addGeneralAttribute(self, attribute_name, attribute_type):
		self.generalAttributes[attribute_name] = attribute_type;

	def addStyleAttribute(self, attribute_name, attribute_type):
		self.styleAttributes[attribute_name] = attribute_type;

	def setFunctionCode(self, function_name, function_code):
		self.functionCodes[function_name] = function_code;

	def getMandatoryAttributes(self, function_name):
		attr_list = []
		for attr, attr_type in self.d[function_name].items():
			attr_list.append((attr, attr_type))
		return attr_list;

	def getAllAttributes(self, function_name):
		attr_list = []
		for attr, attr_type in self.d[function_name].items():
			attr_list.append((attr, attr_type))
		for attr, attr_type in self.optionalAttributes[function_name].items():
			attr_list.append((attr, attr_type))
		for attr, attr_type in self.generalAttributes.items():
			attr_list.append((attr, attr_type))
		return attr_list;

	def getAttributeType(self, function_name, attribute_name):

		if attribute_name in self.d[function_name]:
			return self.d[function_name][attribute_name]

		if attribute_name in self.optionalAttributes[function_name]:
			return self.optionalAttributes[function_name][attribute_name]

		if attribute_name in self.generalAttributes:
			return self.generalAttributes[attribute_name]

		print function_name
		print attribute_name

		raise ValueError("Non-existant attribute name.")

	def getStyleAttributes(self):
		attr_list = []
		for attr, attr_type in self.styleAttributes.items():
			attr_list.append((attr, attr_type))
		return attr_list;

	def getFunctionCode(self, function_name):
		return self.functionCodes.get(function_name, function_name)

	def getAttributeCode(self, function_name, attribute_name):
		return self.attributeCodes.get(function_name, {}).get(attribute_name, attribute_name)

	def functionExists(self, function_name):
		return function_name in self.d;

	def attributeExists(self, function_name, attribute_name):
		return self.functionExists(function_name) and attribute_name in self.d[function_name];

	def functionHasAttribute(self, function_name, attribute_name, attribute_type):
		return self.functionExists(function_name) and (self.d[function_name][attribute_name] == attribute_type 
														or self.generalAttributes.get(attribute_name, 0) == attribute_type);

class SVG(object):

	def __init__(self, expressions, f):
		self.expressions = expressions;
		self.f = f

	def generateSVG(self):

		doc = et.Element('svg', version='1.1', xmlns='http://www.w3.org/2000/svg')

		# search for SVG size in expression tree
		size_set = False
		for function, argument_list in self.expressions:
			if function == 'size':
				for attribute, value in argument_list:
					doc.attrib[attribute] = str(value['value']); 
				size_set = True
				break


		# sometimes size is not defined, get the size from a rectangle
		if not size_set:
			for function, argument_list in self.expressions:
				if function == 'rectangle' and not size_set:
					for attribute, value in argument_list:
						if attribute == 'size':
							doc.attrib['height'] = str(value['y']['value']); 
							doc.attrib['width']  = str(value['x']['value']); 
							size_set = True
							break


		# add the rest of the attributes
		for function, argument_list in self.expressions:

			if function == 'size': continue;

			if function == 'text':
				print argument_list
				# [('t', {'type': 'string', 'value': 'I love Dibu'}),
				#  ('at', {'y': {'type': 'number', 'value': 15}, 'x': {'type': 'number', 'value': 0}, 'type': 'point'})]
				text = et.Element('text')

				for attribute, value in argument_list:
					if attribute == 'at':
						text.attrib['x'] = str(value['x']['value'])
						text.attrib['y'] = str(value['y']['value'])
					elif attribute == 't':
						text.text = value['value']
					else:
						print attribute
						print value
						text.attrib[self.f.getAttributeCode(function, attribute)] = str(value['value'])

				doc.append(text)
			else:
				new_element = et.SubElement(doc, self.f.getFunctionCode(function));
				for attribute, value in argument_list:

					# print argument_list
					# style attribute does not have a value with type but a list
					if attribute == 'style':
						# ('style', [('stroke', {'type': 'string', 'value': 'black'}),
						# ('stroke-width', {'type': 'number', 'value': 3.0}),
						# ('fill', {'type': 'string', 'value': 'none'})])]
						string = []
						for e in value:
							string.append(e[0] + ': ' + str(e[1]['value']) + ';');
						new_element.attrib['style'] = ' '.join(string)
					elif value['type'] == 'point':
						if attribute == 'size':
							new_element.attrib['height'] = str(value['x']['value'])
							new_element.attrib['width']  = str(value['y']['value'])
						elif function == 'circle':
							new_element.attrib['cx'] = str(value['x']['value'])
							new_element.attrib['cy'] = str(value['y']['value'])
						else:
							new_element.attrib['x'] = str(value['x']['value'])
							new_element.attrib['y'] = str(value['y']['value'])
					elif value['type'] == 'array':
						points = []
						for point in value['value']:
							points.append(str(point['x']['value'])+","+str(point['y']['value']))
						new_element.attrib[self.f.getAttributeCode(function, attribute)] = ' '.join(points)
					else:
						new_element.attrib[self.f.getAttributeCode(function, attribute)] = str(value['value'])

		string  = "<?xml version=\"1.0\" standalone=\"no\"?>\n";
		string += et.tostring(doc)

		return string