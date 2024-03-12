from http.server import BaseHTTPRequestHandler, HTTPServer

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/v1":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = "Hello World"
            self.wfile.write(bytes(message, "utf8"))

if __name__ == "__main__":
    wserver = HTTPServer(('localhost', 8080), MyServer)
    print("Server started on http://localhost:8080")
    
    try:
        wserver.serve_forever()
    except KeyboardInterrupt:
        pass

    wserver.server_close()
    print("Server Stopped")