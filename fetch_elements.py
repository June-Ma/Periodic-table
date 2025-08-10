#!/usr/bin/env python3
"""
Script to fetch detailed element data from Bowserinator's Periodic-Table-JSON
and update our elements_data.py with additional information.
"""

import json
import urllib.request

def fetch_element_data():
    """Fetch element data from GitHub"""
    url = "https://raw.githubusercontent.com/Bowserinator/Periodic-Table-JSON/master/PeriodicTableJSON.json"
    
    print("Fetching element data from GitHub...")
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    
    return data['elements']

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
    
    # Build the element dictionary
    element = {
        "Z": e['number'],
        "sym": e['symbol'],
        "name": e['name'],
        "group": e.get('group', 0),
        "period": e['period'],
        "cat": cat,
        "ar": e.get('atomic_mass', None),
        "appearance": e.get('appearance'),
        "phase": e.get('phase'),
        "density": e.get('density'),
        "melt": kelvin_to_celsius(e.get('melt')),
        "boil": kelvin_to_celsius(e.get('boil')),
        "molar_heat": e.get('molar_heat'),
        "discovered_by": e.get('discovered_by'),
        "named_by": e.get('named_by'),
        "electron_configuration": e.get('electron_configuration_semantic'),
        "shells": e.get('shells'),
        "summary": e.get('summary')
    }
    
    # Remove None values to keep data clean
    return {k: v for k, v in element.items() if v is not None}

def generate_python_file(elements):
    """Generate Python file with element data"""
    output = '''"""
Enhanced periodic table element data with detailed properties.
Data sourced from Wikipedia and Bowserinator's Periodic-Table-JSON.
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
    raw_elements = fetch_element_data()
    
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
    with open('elements_data_enhanced.py', 'w', encoding='utf-8') as f:
        f.write(python_code)
    
    print(f"Successfully generated elements_data_enhanced.py with {len(elements)} elements")
    print("\nSample element (Titanium):")
    titanium = next(e for e in elements if e['sym'] == 'Ti')
    print(json.dumps(titanium, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()