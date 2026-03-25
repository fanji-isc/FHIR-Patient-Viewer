#!/usr/bin/env python3
"""
FHIR Patient Viewer — proxy server
Serves viewer/ files and proxies /fhir/r4/* to the FHIR server.
No CORS configuration needed on IRIS.
"""
import base64
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# ── Read config.js ────────────────────────────────────────────────────────────
CONFIG_JS = os.path.join(os.path.dirname(__file__), "viewer", "config.js")
VIEWER_DIR = os.path.join(os.path.dirname(__file__), "viewer")

def _read_config():
    cfg = {"base": "http://localhost:8080/csp/healthshare/demo/fhir/r4",
           "username": "", "password": ""}
    try:
        text = open(CONFIG_JS).read()
        for key in ("base", "username", "password"):
            m = re.search(rf"{key}:\s*'([^']*)'", text)
            if m:
                cfg[key] = m.group(1)
    except Exception as e:
        print(f"Warning: could not read config.js: {e}")
    return cfg

CFG       = _read_config()
FHIR_BASE = CFG["base"].rstrip("/")
AUTH      = ("Basic " + base64.b64encode(
                 f"{CFG['username']}:{CFG['password']}".encode()).decode()
             if CFG["username"] and CFG["password"] else None)

MIME = {".html": "text/html", ".js": "application/javascript",
        ".css": "text/css",   ".json": "application/json"}

# ── Request handler ───────────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        if self.path.startswith("/fhir/r4"):
            self._proxy()
        else:
            self._static()

    def _proxy(self):
        tail     = self.path[len("/fhir/r4"):]
        url      = FHIR_BASE + tail
        headers  = {"Accept": "application/fhir+json"}
        if AUTH:
            headers["Authorization"] = AUTH
        try:
            with urlopen(Request(url, headers=headers), timeout=30) as r:
                body = r.read()
                self.send_response(r.status)
                self.send_header("Content-Type",
                                 r.headers.get("Content-Type", "application/json"))
                self.send_header("Content-Length", len(body))
                self.end_headers()
                self.wfile.write(body)
        except HTTPError as e:
            body = e.read()
            self.send_response(e.code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
        except URLError as e:
            msg = f"Cannot reach FHIR server: {e.reason}".encode()
            self.send_response(502)
            self.end_headers()
            self.wfile.write(msg)

    def _static(self):
        path = self.path.split("?")[0] or "/"
        if path == "/":
            path = "/index.html"
        fp = os.path.join(VIEWER_DIR, path.lstrip("/"))
        if not os.path.isfile(fp):
            fp = os.path.join(VIEWER_DIR, "index.html")
        try:
            ext  = os.path.splitext(fp)[1]
            mime = MIME.get(ext, "application/octet-stream")
            body = open(fp, "rb").read()
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    print(f"\n  FHIR Patient Viewer")
    print(f"  Open:  http://localhost:{port}")
    print(f"  FHIR:  {FHIR_BASE}")
    print(f"  Stop:  Ctrl+C\n")
    try:
        HTTPServer(("", port), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped.")
