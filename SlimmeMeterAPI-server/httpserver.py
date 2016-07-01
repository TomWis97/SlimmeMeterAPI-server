from http.server import BaseHTTPRequestHandler, HTTPServer

# TODO Make configureable.
hostName = "0.0.0.0"
hostPort = 9000

jsonOutput = '[{"random": "koekjes."}]'

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global jsonOutput
        self.send_response(200)
        self.send_header("Content-type", "application/jsonOutput")
        self.end_headers()
        self.wfile.write(bytes(jsonOutput, "utf-8"))

myServer = HTTPServer((hostName, hostPort), MyServer)
myServer.serve_forever()
myServer.server_close()

