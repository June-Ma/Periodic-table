# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask web application that displays an interactive periodic table of elements. The application has been refactored to follow a standard MVC structure with separate files for data, templates, and static assets.

## Project Structure

```
Periodic-table/
├── Periodic-table.py      # Main Flask application
├── elements_data.py       # Element data (all 118 elements)
├── templates/
│   └── index.html        # HTML template
├── static/
│   ├── app.js           # JavaScript functionality
│   └── styles.css       # CSS styling
└── README.md            # Project documentation
```

## Commands

### Running the Application
```bash
python Periodic-table.py
```
The application runs on port 5000 by default and automatically opens in the browser.

### Installing Dependencies
```bash
pip install flask
```
Flask is the only required dependency.

## Architecture

### File Organization

1. **elements_data.py**: Contains the ELEMENTS list with all 118 chemical elements. Each element has:
   - `Z`: Atomic number
   - `sym`: Element symbol
   - `name`: Element name
   - `group`: Group number (1-18, or 0 for lanthanides/actinides)
   - `period`: Period number (1-7)
   - `cat`: Category (alkali, alkaline, transition, posttransition, metalloid, nonmetal, noble, lanth, act)
   - `ar`: Atomic mass

2. **templates/index.html**: HTML template with:
   - Legend for element categories
   - Search input field
   - Grid container for periodic table
   - Details panel for selected element

3. **static/styles.css**: CSS styling including:
   - Grid layout (18 columns for groups)
   - Color coding for element categories
   - Responsive design

4. **static/app.js**: JavaScript handling:
   - Fetching element data from API
   - Dynamic rendering of periodic table
   - Search functionality
   - Element detail display on click

### Flask Routes

- `/` - Renders the main HTML template
- `/api/elements` - Returns element data as JSON

### Key Design Features

- **Asynchronous Data Loading**: Elements are fetched via API on page load
- **Client-Side Filtering**: Search is performed in the browser for instant results
- **Grid Layout**: CSS Grid with 18 columns corresponding to periodic table groups
- **Element Positioning**: Elements placed using `(period, group)` coordinates
- **Auto-launch**: Browser opens automatically when server starts

### Port Configuration

Default port is 5000. To change, modify line 25 in `Periodic-table.py`:
```python
port = 5000  # Change this value if needed
```

## Element Categories

- `alkali`: Alkali metals (Group 1)
- `alkaline`: Alkaline earth metals (Group 2)
- `transition`: Transition metals
- `posttransition`: Post-transition metals
- `metalloid`: Metalloids
- `nonmetal`: Non-metals
- `noble`: Noble gases (Group 18)
- `lanth`: Lanthanides (57-71)
- `act`: Actinides (89-103)