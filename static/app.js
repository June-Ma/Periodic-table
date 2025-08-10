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
    
    // Build detailed information HTML
    let html = `<h3>${e.name} (${e.sym})</h3>`;
    html += `<div class="detail-grid">`;
    
    // Basic properties
    html += `<div class="detail-section">`;
    html += `<h4>Basic Properties</h4>`;
    html += `<p><strong>Atomic Number:</strong> ${e.Z}</p>`;
    html += `<p><strong>Atomic Mass:</strong> ${e.ar ? e.ar.toFixed(4) + ' u' : '—'}</p>`;
    html += `<p><strong>Group:</strong> ${e.group || "f-block"}</p>`;
    html += `<p><strong>Period:</strong> ${e.period}</p>`;
    html += `<p><strong>Category:</strong> ${getCategoryName(e.cat)}</p>`;
    html += `</div>`;
    
    // Physical properties
    if (e.phase || e.density || e.melt || e.boil) {
        html += `<div class="detail-section">`;
        html += `<h4>Physical Properties</h4>`;
        if (e.phase) html += `<p><strong>Phase at STP:</strong> ${e.phase}</p>`;
        if (e.appearance) html += `<p><strong>Appearance:</strong> ${e.appearance}</p>`;
        if (e.density) html += `<p><strong>Density:</strong> ${e.density} ${e.phase === 'Gas' ? 'g/L' : 'g/cm³'}</p>`;
        if (e.melt) html += `<p><strong>Melting Point:</strong> ${e.melt}°C</p>`;
        if (e.boil) html += `<p><strong>Boiling Point:</strong> ${e.boil}°C</p>`;
        html += `</div>`;
    }
    
    // Discovery & History
    if (e.discovered_by || e.named_by) {
        html += `<div class="detail-section">`;
        html += `<h4>Discovery & History</h4>`;
        if (e.discovered_by) html += `<p><strong>Discovered by:</strong> ${e.discovered_by}</p>`;
        if (e.named_by) html += `<p><strong>Named by:</strong> ${e.named_by}</p>`;
        html += `</div>`;
    }
    
    // Electron configuration
    if (e.electron_configuration || e.shells) {
        html += `<div class="detail-section">`;
        html += `<h4>Electron Configuration</h4>`;
        if (e.electron_configuration) html += `<p><strong>Configuration:</strong> ${e.electron_configuration}</p>`;
        if (e.shells) html += `<p><strong>Electrons per shell:</strong> ${e.shells.join(', ')}</p>`;
        html += `</div>`;
    }
    
    // Chemical properties
    if (e.electron_affinity || e.electronegativity || e.ionization_energy) {
        html += `<div class="detail-section">`;
        html += `<h4>Chemical Properties</h4>`;
        if (e.electron_affinity) html += `<p><strong>Electron Affinity:</strong> ${e.electron_affinity} kJ/mol</p>`;
        if (e.electronegativity) html += `<p><strong>Electronegativity:</strong> ${e.electronegativity} (Pauling scale)</p>`;
        if (e.ionization_energy) html += `<p><strong>Ionization Energy:</strong> ${e.ionization_energy} kJ/mol</p>`;
        html += `</div>`;
    }
    
    html += `</div>`;
    
    // Media section with images and 3D model
    if (e.bohr_model_image || e.bohr_model_3d || e.spectral_img) {
        html += `<div class="media-section">`;
        html += `<h4>Visual Resources</h4>`;
        html += `<div class="media-grid">`;
        
        // Bohr model image
        if (e.bohr_model_image) {
            html += `<div class="media-item">`;
            html += `<h5>Bohr Model</h5>`;
            html += `<img src="${e.bohr_model_image}" alt="${e.name} Bohr Model" class="element-image" onerror="this.style.display='none'">`;
            html += `</div>`;
        }
        
        // Spectral image
        if (e.spectral_img) {
            html += `<div class="media-item">`;
            html += `<h5>Emission Spectrum</h5>`;
            html += `<img src="${e.spectral_img}" alt="${e.name} Spectrum" class="element-image spectrum-img" onerror="this.style.display='none'">`;
            html += `</div>`;
        }
        
        // 3D model viewer
        if (e.bohr_model_3d) {
            html += `<div class="media-item model-item">`;
            html += `<h5>3D Model</h5>`;
            html += `<model-viewer 
                src="${e.bohr_model_3d}" 
                alt="${e.name} 3D Model"
                auto-rotate 
                camera-controls 
                shadow-intensity="1"
                class="model-viewer">
            </model-viewer>`;
            html += `</div>`;
        }
        
        html += `</div>`;
        html += `</div>`;
    }
    
    // Summary
    if (e.summary) {
        html += `<div class="summary-section">`;
        html += `<h4>Summary</h4>`;
        html += `<p>${e.summary}</p>`;
        html += `</div>`;
    }
    
    // Wikipedia link
    if (e.source) {
        html += `<div class="source-section">`;
        html += `<a href="${e.source}" target="_blank" class="wikipedia-link">`;
        html += `<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">`;
        html += `<path d="M12.09 13.119c-.936 1.932-2.217 4.548-2.853 5.728-.616 1.074-1.127.931-1.532.029-1.406-3.321-4.293-9.144-5.651-12.409-.251-.601-.441-.987-.619-1.139-.181-.15-.554-.24-1.122-.271C.103 5.033 0 4.982 0 4.898v-.455l.052-.045c.924.013 5.166.013 5.166.013l.062.045v.434c0 .119-.099.182-.297.194-.691.047-1.047.141-1.066.285-.016.122.051.315.199.58l3.621 8.437C8.752 12.184 9.827 9.979 10.885 7.764c.485-1.011.539-1.354.539-1.354-.104-.209-.566-1.449-1.391-3.72-.225-.617-.458-1.243-.697-1.876-.154-.407-.363-.678-.624-.812-.263-.135-.695-.21-1.307-.229C7.202 5.761 7.1 5.7 7.1 5.581v-.453l.056-.045h7.076l.052.045v.434c0 .119-.098.184-.295.196-.615.038-.947.085-.994.144-.061.07-.031.209.086.414.449.788 1.268 2.289 2.458 4.505 1.189-2.216 2.008-3.718 2.459-4.505.116-.205.145-.343.084-.414-.046-.059-.378-.106-.994-.144-.196-.012-.294-.077-.294-.196v-.434l.051-.045h4.709l.056.045v.453c0 .119-.102.181-.304.194-.612.019-1.044.094-1.307.229-.261.134-.469.405-.624.812-.238.633-.472 1.259-.697 1.876-.825 2.271-1.287 3.511-1.391 3.72 0 0 .055.343.54 1.354 1.058 2.215 2.133 4.421 3.148 6.623l3.622-8.437c.147-.265.215-.458.198-.58-.019-.144-.374-.238-1.066-.285-.198-.012-.296-.075-.296-.194v-.434l.06-.045s4.242 0 5.167-.013l.052.045v.455c0 .084-.103.135-.313.159-.57.031-.942.121-1.123.271-.177.152-.368.538-.618 1.139-1.358 3.265-4.245 9.088-5.651 12.409-.406.902-.918 1.045-1.533-.029-.636-1.18-1.918-3.796-2.853-5.728z"></path>`;
        html += `</svg>`;
        html += `Read more on Wikipedia`;
        html += `</a>`;
        html += `</div>`;
    }
    
    details.innerHTML = html;
}

function getCategoryName(cat) {
    const categories = {
        'alkali': 'Alkali metal',
        'alkaline': 'Alkaline earth metal',
        'transition': 'Transition metal',
        'posttransition': 'Post-transition metal',
        'metalloid': 'Metalloid',
        'nonmetal': 'Non-metal',
        'noble': 'Noble gas',
        'lanth': 'Lanthanide',
        'act': 'Actinide',
        'unknown': 'Unknown'
    };
    return categories[cat] || cat || '—';
}

// Load data when page is ready
document.addEventListener('DOMContentLoaded', loadData);