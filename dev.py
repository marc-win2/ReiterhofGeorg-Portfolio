"""Local preview with automatic builds and browser reload. Python standard library only."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock, Thread
import argparse
import json
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
LOCK = Lock()
version = 0


def build():
    global version
    with LOCK:
        result = subprocess.run([sys.executable, str(ROOT / 'build.py')], cwd=ROOT)
        if result.returncode == 0:
            version += 1
            print(f'Vorschau aktualisiert (Stand {version}).', flush=True)
        return result.returncode == 0


def snapshot():
    files = [ROOT / 'build.py', *sorted((ROOT / 'src').rglob('*'))]
    return tuple((str(p), p.stat().st_mtime_ns, p.stat().st_size)
                 for p in files if p.is_file())


def watch():
    previous = snapshot()
    while True:
        time.sleep(.6)
        try:
            current = snapshot()
            if current != previous:
                time.sleep(.2)
                previous = snapshot()
                build()
        except OSError as error:
            print(f'Dateiprüfung: {error}', flush=True)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / 'dist'), **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def do_GET(self):
        with LOCK:
            if self.path.split('?')[0] == '/__dev/version':
                self.send_bytes(json.dumps({'version': version}).encode(), 'application/json')
                return
            target = Path(self.translate_path(self.path))
            if target.is_dir() and self.path.split('?')[0].endswith('/'):
                target /= 'index.html'
            if target.is_file() and target.suffix == '.html':
                script = '''<script>(()=>{
                  const initial=VERSION;
                  let pending=false;
                  setInterval(async()=>{
                    if(pending)return;pending=true;
                    try{
                      const r=await fetch('/__dev/version',{cache:'no-store'});
                      if(r.ok && (await r.json()).version!==initial)location.reload();
                    }catch{}finally{pending=false;}
                  },1000);
                })();</script>'''.replace('VERSION', str(version))
                body = target.read_text().replace('</body>', script + '</body>').encode()
                self.send_bytes(body, 'text/html; charset=utf-8')
                return
            super().do_GET()

    def send_bytes(self, data, content_type):
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        if self.path.split('?')[0] != '/__dev/version':
            super().log_message(format, *args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    if not build():
        server.server_close()
        raise SystemExit(1)
    Thread(target=watch, daemon=True).start()
    print(f'Live-Vorschau: http://127.0.0.1:{args.port} (Stoppen: Strg+C)', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
