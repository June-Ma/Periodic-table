# app.py — one-file Flask periodic table (no f-string braces drama)
import json, webbrowser, threading
from flask import Flask, Response

app = Flask(__name__)

ELEMENTS = [
    # Period 1
    {"Z":1,"sym":"H","name":"Hydrogen","group":1,"period":1,"cat":"nonmetal","ar":1.008},
    {"Z":2,"sym":"He","name":"Helium","group":18,"period":1,"cat":"noble","ar":4.0026},

    # Period 2
    {"Z":3,"sym":"Li","name":"Lithium","group":1,"period":2,"cat":"alkali","ar":6.94},
    {"Z":4,"sym":"Be","name":"Beryllium","group":2,"period":2,"cat":"alkaline","ar":9.0122},
    {"Z":5,"sym":"B","name":"Boron","group":13,"period":2,"cat":"metalloid","ar":10.81},
    {"Z":6,"sym":"C","name":"Carbon","group":14,"period":2,"cat":"nonmetal","ar":12.011},
    {"Z":7,"sym":"N","name":"Nitrogen","group":15,"period":2,"cat":"nonmetal","ar":14.007},
    {"Z":8,"sym":"O","name":"Oxygen","group":16,"period":2,"cat":"nonmetal","ar":15.999},
    {"Z":9,"sym":"F","name":"Fluorine","group":17,"period":2,"cat":"nonmetal","ar":18.998},
    {"Z":10,"sym":"Ne","name":"Neon","group":18,"period":2,"cat":"noble","ar":20.180},

    # Period 3
    {"Z":11,"sym":"Na","name":"Sodium","group":1,"period":3,"cat":"alkali","ar":22.990},
    {"Z":12,"sym":"Mg","name":"Magnesium","group":2,"period":3,"cat":"alkaline","ar":24.305},
    {"Z":13,"sym":"Al","name":"Aluminium","group":13,"period":3,"cat":"posttransition","ar":26.982},
    {"Z":14,"sym":"Si","name":"Silicon","group":14,"period":3,"cat":"metalloid","ar":28.085},
    {"Z":15,"sym":"P","name":"Phosphorus","group":15,"period":3,"cat":"nonmetal","ar":30.974},
    {"Z":16,"sym":"S","name":"Sulfur","group":16,"period":3,"cat":"nonmetal","ar":32.06},
    {"Z":17,"sym":"Cl","name":"Chlorine","group":17,"period":3,"cat":"nonmetal","ar":35.45},
    {"Z":18,"sym":"Ar","name":"Argon","group":18,"period":3,"cat":"noble","ar":39.948},

    # Period 4
    {"Z":19,"sym":"K","name":"Potassium","group":1,"period":4,"cat":"alkali","ar":39.098},
    {"Z":20,"sym":"Ca","name":"Calcium","group":2,"period":4,"cat":"alkaline","ar":40.078},
    {"Z":21,"sym":"Sc","name":"Scandium","group":3,"period":4,"cat":"transition","ar":44.956},
    {"Z":22,"sym":"Ti","name":"Titanium","group":4,"period":4,"cat":"transition","ar":47.867},
    {"Z":23,"sym":"V","name":"Vanadium","group":5,"period":4,"cat":"transition","ar":50.942},
    {"Z":24,"sym":"Cr","name":"Chromium","group":6,"period":4,"cat":"transition","ar":51.996},
    {"Z":25,"sym":"Mn","name":"Manganese","group":7,"period":4,"cat":"transition","ar":54.938},
    {"Z":26,"sym":"Fe","name":"Iron","group":8,"period":4,"cat":"transition","ar":55.845},
    {"Z":27,"sym":"Co","name":"Cobalt","group":9,"period":4,"cat":"transition","ar":58.933},
    {"Z":28,"sym":"Ni","name":"Nickel","group":10,"period":4,"cat":"transition","ar":58.693},
    {"Z":29,"sym":"Cu","name":"Copper","group":11,"period":4,"cat":"transition","ar":63.546},
    {"Z":30,"sym":"Zn","name":"Zinc","group":12,"period":4,"cat":"transition","ar":65.38},
    {"Z":31,"sym":"Ga","name":"Gallium","group":13,"period":4,"cat":"posttransition","ar":69.723},
    {"Z":32,"sym":"Ge","name":"Germanium","group":14,"period":4,"cat":"metalloid","ar":72.630},
    {"Z":33,"sym":"As","name":"Arsenic","group":15,"period":4,"cat":"metalloid","ar":74.922},
    {"Z":34,"sym":"Se","name":"Selenium","group":16,"period":4,"cat":"nonmetal","ar":78.971},
    {"Z":35,"sym":"Br","name":"Bromine","group":17,"period":4,"cat":"nonmetal","ar":79.904},
    {"Z":36,"sym":"Kr","name":"Krypton","group":18,"period":4,"cat":"noble","ar":83.798},

    # Period 5
    {"Z":37,"sym":"Rb","name":"Rubidium","group":1,"period":5,"cat":"alkali","ar":85.468},
    {"Z":38,"sym":"Sr","name":"Strontium","group":2,"period":5,"cat":"alkaline","ar":87.62},
    {"Z":39,"sym":"Y","name":"Yttrium","group":3,"period":5,"cat":"transition","ar":88.906},
    {"Z":40,"sym":"Zr","name":"Zirconium","group":4,"period":5,"cat":"transition","ar":91.224},
    {"Z":41,"sym":"Nb","name":"Niobium","group":5,"period":5,"cat":"transition","ar":92.906},
    {"Z":42,"sym":"Mo","name":"Molybdenum","group":6,"period":5,"cat":"transition","ar":95.95},
    {"Z":43,"sym":"Tc","name":"Technetium","group":7,"period":5,"cat":"transition","ar":98},
    {"Z":44,"sym":"Ru","name":"Ruthenium","group":8,"period":5,"cat":"transition","ar":101.07},
    {"Z":45,"sym":"Rh","name":"Rhodium","group":9,"period":5,"cat":"transition","ar":102.91},
    {"Z":46,"sym":"Pd","name":"Palladium","group":10,"period":5,"cat":"transition","ar":106.42},
    {"Z":47,"sym":"Ag","name":"Silver","group":11,"period":5,"cat":"transition","ar":107.87},
    {"Z":48,"sym":"Cd","name":"Cadmium","group":12,"period":5,"cat":"transition","ar":112.41},
    {"Z":49,"sym":"In","name":"Indium","group":13,"period":5,"cat":"posttransition","ar":114.82},
    {"Z":50,"sym":"Sn","name":"Tin","group":14,"period":5,"cat":"posttransition","ar":118.71},
    {"Z":51,"sym":"Sb","name":"Antimony","group":15,"period":5,"cat":"metalloid","ar":121.76},
    {"Z":52,"sym":"Te","name":"Tellurium","group":16,"period":5,"cat":"metalloid","ar":127.60},
    {"Z":53,"sym":"I","name":"Iodine","group":17,"period":5,"cat":"nonmetal","ar":126.90},
    {"Z":54,"sym":"Xe","name":"Xenon","group":18,"period":5,"cat":"noble","ar":131.29},

    # Period 6 (including lanthanoids)
    {"Z":55,"sym":"Cs","name":"Caesium","group":1,"period":6,"cat":"alkali","ar":132.91},
    {"Z":56,"sym":"Ba","name":"Barium","group":2,"period":6,"cat":"alkaline","ar":137.33},
    {"Z":57,"sym":"La","name":"Lanthanum","group":0,"period":6,"cat":"lanth","ar":138.91},
    {"Z":58,"sym":"Ce","name":"Cerium","group":0,"period":6,"cat":"lanth","ar":140.12},
    {"Z":59,"sym":"Pr","name":"Praseodymium","group":0,"period":6,"cat":"lanth","ar":140.91},
    {"Z":60,"sym":"Nd","name":"Neodymium","group":0,"period":6,"cat":"lanth","ar":144.24},
    {"Z":61,"sym":"Pm","name":"Promethium","group":0,"period":6,"cat":"lanth","ar":145},
    {"Z":62,"sym":"Sm","name":"Samarium","group":0,"period":6,"cat":"lanth","ar":150.36},
    {"Z":63,"sym":"Eu","name":"Europium","group":0,"period":6,"cat":"lanth","ar":151.96},
    {"Z":64,"sym":"Gd","name":"Gadolinium","group":0,"period":6,"cat":"lanth","ar":157.25},
    {"Z":65,"sym":"Tb","name":"Terbium","group":0,"period":6,"cat":"lanth","ar":158.93},
    {"Z":66,"sym":"Dy","name":"Dysprosium","group":0,"period":6,"cat":"lanth","ar":162.50},
    {"Z":67,"sym":"Ho","name":"Holmium","group":0,"period":6,"cat":"lanth","ar":164.93},
    {"Z":68,"sym":"Er","name":"Erbium","group":0,"period":6,"cat":"lanth","ar":167.26},
    {"Z":69,"sym":"Tm","name":"Thulium","group":0,"period":6,"cat":"lanth","ar":168.93},
    {"Z":70,"sym":"Yb","name":"Ytterbium","group":0,"period":6,"cat":"lanth","ar":173.05},
    {"Z":71,"sym":"Lu","name":"Lutetium","group":3,"period":6,"cat":"transition","ar":174.97},
    {"Z":72,"sym":"Hf","name":"Hafnium","group":4,"period":6,"cat":"transition","ar":178.49},
    {"Z":73,"sym":"Ta","name":"Tantalum","group":5,"period":6,"cat":"transition","ar":180.95},
    {"Z":74,"sym":"W","name":"Tungsten","group":6,"period":6,"cat":"transition","ar":183.84},
    {"Z":75,"sym":"Re","name":"Rhenium","group":7,"period":6,"cat":"transition","ar":186.21},
    {"Z":76,"sym":"Os","name":"Osmium","group":8,"period":6,"cat":"transition","ar":190.23},
    {"Z":77,"sym":"Ir","name":"Iridium","group":9,"period":6,"cat":"transition","ar":192.22},
    {"Z":78,"sym":"Pt","name":"Platinum","group":10,"period":6,"cat":"transition","ar":195.08},
    {"Z":79,"sym":"Au","name":"Gold","group":11,"period":6,"cat":"transition","ar":196.97},
    {"Z":80,"sym":"Hg","name":"Mercury","group":12,"period":6,"cat":"transition","ar":200.59},
    {"Z":81,"sym":"Tl","name":"Thallium","group":13,"period":6,"cat":"posttransition","ar":204.38},
    {"Z":82,"sym":"Pb","name":"Lead","group":14,"period":6,"cat":"posttransition","ar":207.2},
    {"Z":83,"sym":"Bi","name":"Bismuth","group":15,"period":6,"cat":"posttransition","ar":208.98},
    {"Z":84,"sym":"Po","name":"Polonium","group":16,"period":6,"cat":"metalloid","ar":209},
    {"Z":85,"sym":"At","name":"Astatine","group":17,"period":6,"cat":"metalloid","ar":210},
    {"Z":86,"sym":"Rn","name":"Radon","group":18,"period":6,"cat":"noble","ar":222},

    # Period 7 (including actinoids)
    {"Z":87,"sym":"Fr","name":"Francium","group":1,"period":7,"cat":"alkali","ar":223},
    {"Z":88,"sym":"Ra","name":"Radium","group":2,"period":7,"cat":"alkaline","ar":226},
    {"Z":89,"sym":"Ac","name":"Actinium","group":0,"period":7,"cat":"act","ar":227},
    {"Z":90,"sym":"Th","name":"Thorium","group":0,"period":7,"cat":"act","ar":232.04},
    {"Z":91,"sym":"Pa","name":"Protactinium","group":0,"period":7,"cat":"act","ar":231.04},
    {"Z":92,"sym":"U","name":"Uranium","group":0,"period":7,"cat":"act","ar":238.03},
    {"Z":93,"sym":"Np","name":"Neptunium","group":0,"period":7,"cat":"act","ar":237},
    {"Z":94,"sym":"Pu","name":"Plutonium","group":0,"period":7,"cat":"act","ar":244},
    {"Z":95,"sym":"Am","name":"Americium","group":0,"period":7,"cat":"act","ar":243},
    {"Z":96,"sym":"Cm","name":"Curium","group":0,"period":7,"cat":"act","ar":247},
    {"Z":97,"sym":"Bk","name":"Berkelium","group":0,"period":7,"cat":"act","ar":247},
    {"Z":98,"sym":"Cf","name":"Californium","group":0,"period":7,"cat":"act","ar":251},
    {"Z":99,"sym":"Es","name":"Einsteinium","group":0,"period":7,"cat":"act","ar":252},
    {"Z":100,"sym":"Fm","name":"Fermium","group":0,"period":7,"cat":"act","ar":257},
    {"Z":101,"sym":"Md","name":"Mendelevium","group":0,"period":7,"cat":"act","ar":258},
    {"Z":102,"sym":"No","name":"Nobelium","group":0,"period":7,"cat":"act","ar":259},
    {"Z":103,"sym":"Lr","name":"Lawrencium","group":3,"period":7,"cat":"act","ar":266},
    {"Z":104,"sym":"Rf","name":"Rutherfordium","group":4,"period":7,"cat":"transition","ar":267},
    {"Z":105,"sym":"Db","name":"Dubnium","group":5,"period":7,"cat":"transition","ar":268},
    {"Z":106,"sym":"Sg","name":"Seaborgium","group":6,"period":7,"cat":"transition","ar":269},
    {"Z":107,"sym":"Bh","name":"Bohrium","group":7,"period":7,"cat":"transition","ar":270},
    {"Z":108,"sym":"Hs","name":"Hassium","group":8,"period":7,"cat":"transition","ar":277},
    {"Z":109,"sym":"Mt","name":"Meitnerium","group":9,"period":7,"cat":"transition","ar":278},
    {"Z":110,"sym":"Ds","name":"Darmstadtium","group":10,"period":7,"cat":"transition","ar":281},
    {"Z":111,"sym":"Rg","name":"Roentgenium","group":11,"period":7,"cat":"transition","ar":282},
    {"Z":112,"sym":"Cn","name":"Copernicium","group":12,"period":7,"cat":"transition","ar":285},
    {"Z":113,"sym":"Nh","name":"Nihonium","group":13,"period":7,"cat":"posttransition","ar":286},
    {"Z":114,"sym":"Fl","name":"Flerovium","group":14,"period":7,"cat":"posttransition","ar":289},
    {"Z":115,"sym":"Mc","name":"Moscovium","group":15,"period":7,"cat":"posttransition","ar":290},
    {"Z":116,"sym":"Lv","name":"Livermorium","group":16,"period":7,"cat":"posttransition","ar":293},
    {"Z":117,"sym":"Ts","name":"Tennessine","group":17,"period":7,"cat":"metalloid","ar":294},
    {"Z":118,"sym":"Og","name":"Oganesson","group":18,"period":7,"cat":"noble","ar":294}
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
.name {
  font-size: 10px;
  opacity: .85;
  display: block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;   /* the "..." effect */
  white-space: nowrap;       /* keeps it on one line */
}
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
  [...grid.children].forEach(x => { 
    x.className = "el spacer"; 
    x.innerHTML = ""; 
    x.onclick = null; 
  });
  for (const e of list) {
    const i = idx(e.period, e.group);
    if (i < 0 || i >= grid.children.length) continue;
    const cell = grid.children[i];
    cell.className = "el " + (e.cat || "");
    cell.innerHTML = `
  <div class="num">${e.Z}</div>
  <div class="sym">${e.sym}</div>
  <div class="name">${e.name}</div>`;
cell.title = `${e.name} (${e.sym})`;   // ← tooltip on the whole box
cell.onclick = () => show(e);
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
