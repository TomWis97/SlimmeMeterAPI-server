data = "1-0:1.8.2(004151.898*kWh)"

def readData(data):
	"""This function will convert a string to a dictionary.
	The dictionary will have the following keys:
		- name (string)
		- id (string)
		- value (tuple)
	This function assumes the following lay-out:
		id(value_1)(value_2)..(value_n)
	Where only one value is required.
	"""
	# Raise exception when input is not a string.
	if not isinstance(data, str):
		raise ValueError("Input is not a string.")
	# Creating variables.
	dataId = ''
	dataValue = ()
	# Creating flags
	dataIdSet = False
	currentValue = ''
	for char in data:
		# If the current character is a '(', that means that the
		# ID is complete.
		if char == '(':
			dataIdSet = True
			continue
		# If the current character is a ')', that means that the
		# current value has ended.
		if char == ')':
			dataValue = dataValue + (currentValue,)
			currentValue = ''
			continue
		if dataIdSet:
			currentValue = currentValue + char
			continue
		else:
			dataId = dataId + char
			continue
		# TODO: Map names to IDs.
	return {'id': dataId, 'value': dataValue}
print(readData(data))