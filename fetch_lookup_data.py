#!/usr/bin/env python3
"""
Script to fetch element data from periodic-table-lookup.json
and generate an enhanced elements_data.py file.
"""

import json
import urllib.request

def fetch_lookup_data():
    """Fetch element data from GitHub using the lookup JSON"""
    url = "https://raw.githubusercontent.com/Bowserinator/Periodic-Table-JSON/master/periodic-table-lookup.json"
    
    print("Fetching element data from periodic-table-lookup.json...")
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    
    # The lookup JSON has an 'order' array and element data by name
    order = data.get('order', [])
    elements = []
    
    for element_name in order:
        if element_name in data:
            elements.append(data[element_name])
    
    return elements

def kelvin_to_celsius(k):
    """Convert Kelvin to Celsius"""
    if k is None:
        return None
    return round(k - 273.15, 2)

def format_element(e):
    """Format element data for our structure"""
    # Map category names to our short codes
    category_map = {
        "alkali metal": "alkali",
        "alkaline earth metal": "alkaline",
        "transition metal": "transition",
        "post-transition metal": "posttransition",
        "metalloid": "metalloid",
        "diatomic nonmetal": "nonmetal",
        "polyatomic nonmetal": "nonmetal",
        "reactive nonmetal": "nonmetal",
        "noble gas": "noble",
        "lanthanide": "lanth",
        "actinide": "act",
        "unknown, probably transition metal": "transition",
        "unknown, probably post-transition metal": "posttransition",
        "unknown, probably metalloid": "metalloid",
        "unknown, predicted to be noble gas": "noble"
    }
    
    cat = category_map.get(e.get('category', '').lower(), 'unknown')
    
    # Build the element dictionary with all available fields
    element = {
        "Z": e['number'],
        "sym": e['symbol'],
        "name": e['name'],
        "group": e.get('group', 0),
        "period": e['period'],
        "cat": cat,
        "ar": e.get('atomic_mass'),
        "appearance": e.get('appearance'),
        "phase": e.get('phase'),
        "density": e.get('density'),
        "melt": kelvin_to_celsius(e.get('melt')),
        "boil": kelvin_to_celsius(e.get('boil')),
        "molar_heat": e.get('molar_heat'),
        "discovered_by": e.get('discovered_by'),
        "named_by": e.get('named_by'),
        "electron_configuration": e.get('electron_configuration_semantic'),
        "electron_affinity": e.get('electron_affinity'),
        "electronegativity": e.get('electronegativity_pauling'),
        "ionization_energy": e.get('ionization_energies', [None])[0] if e.get('ionization_energies') else None,
        "shells": e.get('shells'),
        "summary": e.get('summary'),
        "source": e.get('source'),
        "spectral_img": e.get('spectral_img'),
        "bohr_model_image": e.get('bohr_model_image'),
        "bohr_model_3d": e.get('bohr_model_3d')
    }
    
    # Remove None values to keep data clean
    return {k: v for k, v in element.items() if v is not None}

def generate_python_file(elements):
    """Generate Python file with element data"""
    output = '''"""
Enhanced periodic table element data with comprehensive properties.
Data sourced from: https://github.com/Bowserinator/Periodic-Table-JSON
Original data from Wikipedia and various scientific sources.
"""

ELEMENTS = [
'''
    
    # Group elements by period
    for period in range(1, 8):
        period_elements = [e for e in elements if e['period'] == period]
        if period_elements:
            output += f"    # Period {period}\n"
            for e in period_elements:
                # Format as compact JSON for readability
                json_str = json.dumps(e, ensure_ascii=False, separators=(',', ':'))
                output += f"    {json_str},\n"
            output += "\n"
    
    # Remove trailing comma and newline
    output = output.rstrip(",\n") + "\n]"
    
    return output

def main():
    # Fetch data
    raw_elements = fetch_lookup_data()
    
    # Format elements
    elements = []
    for e in raw_elements:
        formatted = format_element(e)
        elements.append(formatted)
    
    # Sort by atomic number
    elements.sort(key=lambda x: x['Z'])
    
    # Generate Python file
    python_code = generate_python_file(elements)
    
    # Save to file
    with open('elements_data.py', 'w', encoding='utf-8') as f:
        f.write(python_code)
    
    print(f"Successfully generated elements_data.py with {len(elements)} elements")
    
    # Show sample element
    print("\nSample element (Titanium):")
    titanium = next(e for e in elements if e['sym'] == 'Ti')
    print(json.dumps(titanium, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()