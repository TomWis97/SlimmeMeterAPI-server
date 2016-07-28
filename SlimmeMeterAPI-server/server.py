#!/usr/bin/env python3
import serial
import interpreter
import time
import json
import configparser
import threading
import urllib.request
import urllib.parse
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep

# Configuration reader
config = configparser.ConfigParser()
config.read('config.ini')
httpPort = int(config['server']['port'])
serialDevice = config['server']['serialDevice']
dataToExpect = int(config['server']['dataToExpect'])
clientIP = config['server']['clientIP']
clientPort = config['server']['clientPort']
# Configuration reading done.

# This variable will contain the latest data.
jsonOutput = ''

class serialListener(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global jsonOutput
        with serial.Serial(serialDevice, 115200, timeout=1) as ser:
            while True:
                data = ser.readlines()
                if (len(data) > 0):
                    # Current data is in bytes. Convert to string.
                    for index, item in enumerate(data):
                        data[index] = str(item, encoding='ASCII').rstrip()
                    returnData = interpreter.readList(data)
                    if len(returnData) != dataToExpect:
                        print("Invalid data!")
                        continue
                    jsonOutput = json.dumps(returnData, sort_keys=True)
                    #print("URL:", 'http://' + clientIP + ':' + clientPort + '/')
                    try:
                        urllib.request.urlopen(
                            urllib.request.Request(
                                'http://' + clientIP + ':' + clientPort + '/',
                                urllib.parse.urlencode(
                                    {jsonOutput: ''}
                                ).encode('UTF-8')))
                    except:
                        print("Error while sending HTTP POST:", sys.exc_info()[0])
                    

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global jsonOutput
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(jsonOutput, "utf-8"))

class restServer(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        myServer = HTTPServer(('',httpPort), webserverHandler)
        print("Starting webserver.")
        myServer.serve_forever()
        myServer.server_close()

serverThread = restServer("RESTServer")
listenerThread = serialListener("SerialListener")

try:
    listenerThread.start()
    sleep (10) # Give the serial thread time to get the data.
    serverThread.start()
    serverThread.join()
    listenerThread.join()
except KeyboardInterrupt:
    print("CTRL-C pressed. Stopping server.")
    exit(0)
