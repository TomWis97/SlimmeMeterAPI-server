import re

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
	dataName = getName(dataId)
	return {'id': dataId, 'value': dataValue, 'name': getName(dataId)}

def readList(dataList):
	"""Input a list of lines, strip the unnecessary stuff and
	send to readData. Return a list of all the processed values."""
	blockedChars = ('/', '!')
	totalList = []
	for line in dataList:
		if not ((len(line) == 0) or (line[0] in blockedChars)): 
			totalList.append(readData(line))
	return totalList

def getName(id):
	"""Input an ID and return a name. If no name is present, return ID."""
	global nameIdMaps
	return nameIdMaps[id]
	
# TODO Put this in an __init__?
# Import the map file and put it in a dictionary.
mapFile = open('id_name_map.txt', 'r')
nameIdMaps = {}
for line in mapFile:
	splitLine = line.split('=')
	nameIdMaps[splitLine[0].strip()] = splitLine[1].strip()
