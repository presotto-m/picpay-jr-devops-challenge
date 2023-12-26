import http.server
import socketserver
import json
import redis

class RequestHandler(http.server.SimpleHTTPRequestHandler):

    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self._send_cors_headers()
        self.end_headers()

        if self.path == '/health':
            self.wfile.write(bytes(json.dumps({"status": "up"}), "utf8"))

    def do_POST(self):
        self.send_response(201)
        self.send_header("Content-type", "application/json")
        self._send_cors_headers()
        self.end_headers()
        
        if self.path == '/write':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            redishost = "picpay-jr-devops-challenge-redis-1"  # Altere o host do Redis conforme necessário
            redisclient = redis.Redis(host=redishost)
            redisclient.set("SHAREDKEY", post_data)
            self.wfile.write(bytes(json.dumps({"message": "Data written to Redis"}), "utf8"))

if __name__ == "__main__":
    handler_object = RequestHandler
    with socketserver.TCPServer(("", 8080), handler_object) as server:
        print("Server started at http://localhost:8080")
        server.serve_forever()
