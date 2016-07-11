import serial
import interpreter
import time
import json

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep

jsonOutput = ''

class serialListener(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self, name)
        self.name = name

    def run(self):
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
                    if len(returnData) != 23:
                        raise ValueError
                    print(json.dumps(returnData, sort_keys=True))

class HTTPServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global jsonOutput
        self.send_response(200)
        self.send_header("Content-Type", "application/jsonOutput")
        self.end_headers()
        self.wfile.write(bytes(jsonOutput, "utf-8"))

class restServer(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self, name)
        self.name = name

    def run(self):
        myServer = HTTPServer(('',19353), serverServer)
        myServer.serve_forever()
        myServer.server_close()

serverThread = restServer("RESTServer")
listenerThread = serialListener("SerialListener")

listenerThread.start()
sleep (10)
serverThread.start()

serverThread.join()
listenerThread.join()
