from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

def run(server_class=HTTPServer, handler_class=HealthCheckHandler):
    server_address = ("", 8080)
    httpd = server_class(server_address, handler_class)
    print("Health check server running on port 8080...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
