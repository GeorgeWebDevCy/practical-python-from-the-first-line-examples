"""Controlled loopback JSON service for Chapter 16. Not a public API."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BODY = b'[{"topic":"files","minutes":25},{"topic":"tests","minutes":20}]'


class FixtureHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/sessions":
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(BODY)))
        self.end_headers()
        self.wfile.write(BODY)

    def log_message(self, format, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    with ThreadingHTTPServer(("127.0.0.1", args.port), FixtureHandler) as server:
        print(f"Fixture: http://127.0.0.1:{server.server_port}/sessions", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
