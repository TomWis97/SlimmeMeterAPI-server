import serial
import interpreter
import time
import json

with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
	print(ser.name)
	while True:
		data = ser.readlines()
		if (len(data) > 0):
			if not (data[0] == b'/KFM5KAIFA-METER\r\n'):
				# TODO Make this configurable.
				# TODO Doesn't seem to be always working.
				# Make sure tha data is valid.
				print("Invalid data!!!!1")
				continue
			# Current data is in bytes. Convert to string.
			for index, item in enumerate(data):
				data[index] = str(item, encoding='ASCII').rstrip()
			returnData = interpreter.readList(data)
			print(returnData)
			for item in returnData:
				print(item)
			if len(returnData) != 23:
				raise ValueError
			print("----------- JSON -----------")
			print(json.dumps(returnData, sort_keys=True))
			exit()
