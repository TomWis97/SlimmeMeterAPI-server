import serial
import interpreter

with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
	print(ser.name)
	while True:
		data = ser.readlines()
		if (len(data) > 0):
			# Current data is in bytes. Conver to string.
			for index, item in enumerate(data):
				data[index] = str(item, encoding='ASCII')
			returnData = interpreter.readList(data)
			print(returnData)
		else:
			print("------------ Leeg ----------")
