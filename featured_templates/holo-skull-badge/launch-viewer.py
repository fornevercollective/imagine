#!/usr/bin/env python3
import os, webbrowser, http.server, socketserver, threading, time

PORT = 8000
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # go to imagine root

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

def serve():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving on http://localhost:{PORT}")
        print("Open: http://localhost:{}/featured_templates/holo-skull-badge/holo-viewer.html".format(PORT))
        httpd.serve_forever()

if __name__ == "__main__":
    t = threading.Thread(target=serve, daemon=True)
    t.start()
    time.sleep(0.8)
    url = f"http://localhost:{PORT}/featured_templates/holo-skull-badge/holo-viewer.html"
    print("Launching browser to the Holo Skull Badge viewer...")
    print("IMPORTANT: Once the page loads, do a HARD REFRESH (Cmd/Ctrl + Shift + R) to ensure all images and videos load properly.")
    webbrowser.open(url)
    try:
        input("Press Enter to stop server...\n")
    except:
        pass
