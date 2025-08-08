# app.py — one-file Flask periodic table (no f-string braces drama)
import json, webbrowser, threading
from flask import Flask, Response

app = Flask(__name__)

ELEMENTS = [
  {"Z":1,"sym":"H","name":"Hydrogen","group":1,"period":1,"cat":"nonmetal","ar":1.008},
  {"Z":2,"sym":"He","name":"Helium","group":18,"period":1,"cat":"noble","ar":4.0026},
  {"Z":3,"sym":"Li","name":"Lithium","group":1,"period":2,"cat":"alkali","ar":6.94},
  {"Z":4,"sym":"Be","name":"Beryllium","group":2,"period":2,"cat":"alkaline","ar":9.0122},
  {"Z":5,"sym":"B","name":"Boron","group":13,"period":2,"cat":"metalloid","ar":10.81},
  {"Z":6,"sym":"C","name":"Carbon","group":14,"period":2,"cat":"nonmetal","ar":12.011},
  {"Z":7,"sym":"N","name":"Nitrogen","group":15,"period":2,"cat":"nonmetal","ar":14.007},
  {"Z":8,"sym":"O","name":"Oxygen","group":16,"period":2,"cat":"nonmetal","ar":15.999},
  {"Z":9,"sym":"F","name":"Fluorine","group":17,"period":2,"cat":"nonmetal","ar":18.998},
  {"Z":10,"sym":"Ne","name":"Neon","group":18,"period":2,"cat":"noble","ar":20.180},
  {"Z":11,"sym":"Na","name":"Sodium","group":1,"period":3,"cat":"alkali","ar":22.990},
  {"Z":12,"sym":"Mg","name":"Magnesium","group":2,"period":3,"cat":"alkaline","ar":24.305},
  {"Z":13,"sym":"Al","name":"Aluminium","group":13,"period":3,"cat":"posttransition","ar":26.982},
  {"Z":14,"sym":"Si","name":"Silicon","group":14,"period":3,"cat":"metalloid","ar":28.085},
  {"Z":15,"sym":"P","name":"Phosphorus","group":15,"period":3,"cat":"nonmetal","ar":30.974},
  {"Z":16,"sym":"S","name":"Sulfur","group":16,"period":3,"cat":"nonmetal","ar":32.06},
  {"Z":17,"sym":"Cl","name":"Chlorine","group":17,"period":3,"cat":"nonmetal","ar":35.45},
  {"Z":18,"sym":"Ar","name":"Argon","group":18,"period":3,"cat":"noble","ar":39.948}
]

HTML = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Periodic Table (one-file)</title>
<style>
:root { --cell: 64px; --gap: 6px; font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; }
body { margin: 20px; }
h1 { margin: 0 0 10px; }
.legend { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:10px; }
.chip { padding:4px 8px; border-radius:999px; font-size:12px; border:1px solid #ccc; }
.grid { display:grid; grid-template-columns: repeat(18, var(--cell)); gap: var(--gap); }
.el { width: var(--cell); height: var(--cell); border-radius: 8px; padding: 6px;
      box-sizing: border-box; background:#f6f6f6; border:1px solid #ddd; }
.el:hover { outline: 2px solid #000; cursor: pointer; }
.num { font-size: 10px; opacity:.7; }
.sym { font-size: 18px; font-weight:700; line-height:1.1; }
.name { font-size: 10px; opacity:.85; }
.spacer { visibility:hidden; }
.alkali { background:#ffe7e7; }
.alkaline { background:#fff1d6; }
.transition { background:#e7f0ff; }
.posttransition { background:#e9f2ff; }
.metalloid { background:#eafce7; }
.nonmetal { background:#f1e7ff; }
.noble { background:#e7fff9; }
.lanth { background:#fdf6ff; }
.act { background:#fff6f8; }
#search { margin:8px 0 12px; padding:8px 10px; width:min(420px, 90%); }
#details { margin-top:16px; padding:12px; border:1px solid #ddd; border-radius:10px; }
.small { font-size:12px; opacity:.75; }
</style>
</head><body>
  <h1>Periodic Table</h1>
  <div class="legend">
    <span class="chip alkali">Alkali</span>
    <span class="chip alkaline">Alkaline earth</span>
    <span class="chip transition">Transition</span>
    <span class="chip posttransition">Post-transition</span>
    <span class="chip metalloid">Metalloid</span>
    <span class="chip nonmetal">Non-metal</span>
    <span class="chip noble">Noble gas</span>
    <span class="chip lanth">Lanthanide</span>
    <span class="chip act">Actinide</span>
  </div>
  <input id="search" placeholder="Search name or symbol…"/>
  <div class="small">Demo dataset shown. Say “full please” for all 118.</div>

  <div class="grid" id="table"></div>
  <div id="details">Click an element to see details.</div>

  <script src="/data.js"></script>
  <script>
  const grid = document.getElementById("table");
  const details = document.getElementById("details");

  for (let r=1;r<=7;r++) for (let c=1;c<=18;c++) {
    const d=document.createElement("div");
    d.className="el spacer"; d.dataset.r=r; d.dataset.c=c;
    grid.appendChild(d);
  }
  const idx = (r,c)=> (r-1)*18+(c-1);

  function paint(list) {
    [...grid.children].forEach(x=>{ x.className="el spacer"; x.innerHTML=""; x.onclick=null; });
    for (const e of list) {
      const i = idx(e.period, e.group);
      if (i<0 || i>=grid.children.length) continue;
      const cell = grid.children[i];
      cell.className = "el " + (e.cat||"");
      cell.innerHTML = `
        <div class="num">${e.Z}</div>
        <div class="sym">${e.sym}</div>
        <div class="name">${e.name}</div>`;
      cell.onclick = ()=> show(e);
    }
  }

  function show(e) {
    details.innerHTML = `<b>${e.name} (${e.sym})</b><br>
      Atomic number: ${e.Z}<br>
      Group: ${e.group}, Period: ${e.period}<br>
      Category: ${e.cat || "—"}<br>
      Relative atomic mass: ${e.ar ?? "—"}`;
  }

  paint(DATA);

  const box = document.getElementById("search");
  box.addEventListener("input", ()=>{
    const q = box.value.trim().toLowerCase();
    if (!q) return paint(DATA);
    const filtered = DATA.filter(e =>
      e.name.toLowerCase().includes(q) || e.sym.toLowerCase().includes(q));
    paint(filtered);
  });
  </script>
</body></html>
"""

@app.get("/")
def index():
    return Response(HTML, mimetype="text/html")

@app.get("/data.js")
def data_js():
    # Serve JS that defines a global DATA = [...]
    js = "const DATA = " + json.dumps(ELEMENTS) + ";"
    return Response(js, mimetype="application/javascript")

def _open(url):
    try:
        webbrowser.open(url, new=2)
    except Exception:
        pass

if __name__ == "__main__":
    port = 5000
    # If 5000 is busy, change port=5001 below.
    threading.Timer(0.8, _open, args=(f"http://127.0.0.1:{port}",)).start()
    app.run(debug=True, port=port)
