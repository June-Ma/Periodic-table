let DATA = [];

async function loadData() {
    try {
        const response = await fetch('/api/elements');
        DATA = await response.json();
        initializeTable();
    } catch (error) {
        console.error('Failed to load element data:', error);
    }
}

function initializeTable() {
    const mainGrid = document.getElementById("table");
    const lanthGrid = document.getElementById("lanthanides");
    const actGrid = document.getElementById("actinides");

    // Create main grid cells (7 rows x 18 columns)
    for (let r = 1; r <= 7; r++) {
        for (let c = 1; c <= 18; c++) {
            const d = document.createElement("div");
            d.className = "el spacer";
            d.dataset.r = r;
            d.dataset.c = c;
            mainGrid.appendChild(d);
        }
    }

    // Create lanthanides grid cells (15 elements)
    for (let i = 0; i < 15; i++) {
        const d = document.createElement("div");
        d.className = "el spacer";
        lanthGrid.appendChild(d);
    }

    // Create actinides grid cells (15 elements)
    for (let i = 0; i < 15; i++) {
        const d = document.createElement("div");
        d.className = "el spacer";
        actGrid.appendChild(d);
    }

    // Paint initial elements
    paint(DATA);

    // Setup search functionality
    const searchBox = document.getElementById("search");
    searchBox.addEventListener("input", () => {
        const q = searchBox.value.trim().toLowerCase();
        if (!q) return paint(DATA);
        const filtered = DATA.filter(e =>
            e.name.toLowerCase().includes(q) || e.sym.toLowerCase().includes(q)
        );
        paint(filtered);
    });
}

function paint(list) {
    const mainGrid = document.getElementById("table");
    const lanthGrid = document.getElementById("lanthanides");
    const actGrid = document.getElementById("actinides");
    
    // Helper function to get cell index in main grid
    const idx = (r, c) => (r - 1) * 18 + (c - 1);

    // Reset all cells
    [...mainGrid.children].forEach(x => {
        x.className = "el spacer";
        x.innerHTML = "";
        x.onclick = null;
        x.title = "";
    });
    [...lanthGrid.children].forEach(x => {
        x.className = "el spacer";
        x.innerHTML = "";
        x.onclick = null;
        x.title = "";
    });
    [...actGrid.children].forEach(x => {
        x.className = "el spacer";
        x.innerHTML = "";
        x.onclick = null;
        x.title = "";
    });

    // Separate elements into main table, lanthanides, and actinides
    const lanthanides = [];
    const actinides = [];
    const mainElements = [];

    for (const e of list) {
        // Lanthanides: La (57) to Lu (71)
        if (e.Z >= 57 && e.Z <= 71) {
            lanthanides.push(e);
        }
        // Actinides: Ac (89) to Lr (103)
        else if (e.Z >= 89 && e.Z <= 103) {
            actinides.push(e);
        }
        // Main table elements
        else {
            mainElements.push(e);
        }
    }

    // Paint main table elements
    for (const e of mainElements) {
        const col = e.group;
        const row = e.period;
        
        const i = idx(row, col);
        if (i < 0 || i >= mainGrid.children.length) continue;
        
        const cell = mainGrid.children[i];
        cell.className = "el " + (e.cat || "");
        cell.innerHTML = `
            <div class="num">${e.Z}</div>
            <div class="sym">${e.sym}</div>
            <div class="name">${e.name}</div>`;
        cell.title = `${e.name} (${e.sym})`;
        cell.onclick = () => show(e);
    }

    // Paint lanthanides (57-71)
    lanthanides.sort((a, b) => a.Z - b.Z);
    for (let i = 0; i < lanthanides.length && i < 15; i++) {
        const e = lanthanides[i];
        const cell = lanthGrid.children[i];
        cell.className = "el " + (e.cat || "");
        cell.innerHTML = `
            <div class="num">${e.Z}</div>
            <div class="sym">${e.sym}</div>
            <div class="name">${e.name}</div>`;
        cell.title = `${e.name} (${e.sym})`;
        cell.onclick = () => show(e);
    }

    // Paint actinides (89-103)
    actinides.sort((a, b) => a.Z - b.Z);
    for (let i = 0; i < actinides.length && i < 15; i++) {
        const e = actinides[i];
        const cell = actGrid.children[i];
        cell.className = "el " + (e.cat || "");
        cell.innerHTML = `
            <div class="num">${e.Z}</div>
            <div class="sym">${e.sym}</div>
            <div class="name">${e.name}</div>`;
        cell.title = `${e.name} (${e.sym})`;
        cell.onclick = () => show(e);
    }

    // Add asterisk markers in periods 6 and 7 where lanthanides/actinides belong
    // Period 6, Group 3 (after Ba, before Hf)
    const lanthMarker = mainGrid.children[idx(6, 3)];
    lanthMarker.className = "el lanth";
    lanthMarker.innerHTML = `<div style="font-size: 24px; text-align: center; line-height: 40px;">*</div>`;
    lanthMarker.title = "Lanthanides (57-71)";
    
    // Period 7, Group 3 (after Ra, before Rf)
    const actMarker = mainGrid.children[idx(7, 3)];
    actMarker.className = "el act";
    actMarker.innerHTML = `<div style="font-size: 24px; text-align: center; line-height: 40px;">**</div>`;
    actMarker.title = "Actinides (89-103)";
}

function show(e) {
    const details = document.getElementById("details");
    details.innerHTML = `
        <b>${e.name} (${e.sym})</b><br>
        Atomic number: ${e.Z}<br>
        Group: ${e.group || "f-block"}, Period: ${e.period}<br>
        Category: ${e.cat || "—"}<br>
        Relative atomic mass: ${e.ar ?? "—"}`;
}

// Load data when page is ready
document.addEventListener('DOMContentLoaded', loadData);