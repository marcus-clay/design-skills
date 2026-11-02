#!/usr/bin/env python3
"""Serveur local pour projeter un croquis pendant une réunion ou un atelier.

Principe: Claude réécrit le dessin brut (draft.svg) à chaque échange; ce script le surveille,
le recompose et l'affiche en plein écran dans le navigateur, qui se met à jour tout seul
(fondu léger, sans clignotement). On projette l'onglet, on parle, le croquis suit.

Usage:
    python3 live.py draft.svg                  # http://localhost:8765, recomposition automatique
    python3 live.py draft.svg --port 9000 --paper white
    python3 live.py page.html --raw            # sert tel quel un HTML interactif (rechargement auto)

Touche dans le navigateur: f = plein écran.
Aucune dépendance: bibliothèque standard uniquement.
"""
import argparse
import http.server
import pathlib
import subprocess
import sys
import threading
import time

HERE = pathlib.Path(__file__).resolve().parent

VIEWER = """<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Croquis en direct</title>
<style>html,body{margin:0;height:100%;background:%BG%;overflow:hidden}
#v{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;transition:opacity .25s}
#v svg{width:100vw;height:100vh;display:block}
#st{position:fixed;right:10px;bottom:6px;font:13px/1 system-ui,sans-serif;color:#9a9a94;opacity:.0;transition:opacity .4s}
body:hover #st{opacity:1}</style></head><body><div id="v"></div><div id="st">en direct</div>
<script>
var cur=null,box=document.getElementById('v'),st=document.getElementById('st');
async function tick(){
  try{
    var m=await (await fetch('/__mtime',{cache:'no-store'})).text();
    if(m!==cur){
      var html=await (await fetch('/__content',{cache:'no-store'})).text();
      if(cur!==null){box.style.opacity=.15;await new Promise(r=>setTimeout(r,160));}
      if(html.indexOf('<!doctype')===0||html.indexOf('<html')===0){location.reload();return;}
      box.innerHTML=html;box.style.opacity=1;cur=m;st.textContent='mis à jour '+new Date().toLocaleTimeString();
    }
  }catch(e){st.textContent='connexion perdue';}
  setTimeout(tick,600);
}
tick();
document.addEventListener('keydown',function(e){if(e.key==='f'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen()}});
</script></body></html>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--paper", default="cream")
    ap.add_argument("--size", default="1600x900")
    ap.add_argument("--raw", action="store_true", help="servir le fichier tel quel (déjà composé)")
    a = ap.parse_args()

    src = pathlib.Path(a.src).resolve()
    if not src.exists():
        sys.exit(f"Fichier introuvable: {src}")
    out = src.with_name(src.stem + ".live.svg")
    state = {"m": 0.0, "err": ""}

    def rebuild():
        if a.raw:
            return
        r = subprocess.run([sys.executable, str(HERE / "compose.py"), str(src), "-o", str(out), "--paper", a.paper,
                            "--size", a.size, "--outline"], capture_output=True, text=True)
        state["err"] = r.stderr.strip() if r.returncode else ""
        if r.returncode:
            print("compose:", r.stderr.strip() or r.stdout.strip())

    def watch():
        last = 0.0
        while True:
            try:
                m = src.stat().st_mtime
                if m != last:
                    last = m
                    rebuild()
                    state["m"] = time.time()
            except FileNotFoundError:
                pass
            time.sleep(0.3)

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def _send(self, body, ctype="text/html; charset=utf-8"):
            b = body.encode("utf-8") if isinstance(body, str) else body
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(b)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(b)

        def do_GET(self):
            if self.path.startswith("/__mtime"):
                return self._send(str(state["m"]), "text/plain")
            if self.path.startswith("/__content"):
                f = src if a.raw else out
                try:
                    return self._send(f.read_text(encoding="utf-8"))
                except FileNotFoundError:
                    return self._send("<p style='font:20px sans-serif;padding:2em'>En attente du premier croquis...</p>")
            from compose import PAPERS  # noqa
            bg = PAPERS.get(a.paper, PAPERS["cream"])[0]
            self._send(VIEWER.replace("%BG%", bg))

    sys.path.insert(0, str(HERE))
    threading.Thread(target=watch, daemon=True).start()
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", a.port), H)
    print(f"Croquis en direct: http://localhost:{a.port}  (surveille {src.name}, Ctrl+C pour arrêter)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
