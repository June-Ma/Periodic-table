# 🧪Periodic Table🧪

An interactive periodic table web application built with Flask and vanilla JavaScript.

## Features

- **Interactive UI**: Click on any element to view detailed information
- **Search functionality**: Filter elements by name or symbol
- **Complete dataset**: All 118 elements including lanthanides and actinides
- **Color-coded categories**: Visual distinction between element types
- **Responsive design**: Clean, modern interface with hover effects
- **Auto-launch**: Opens browser automatically when starting the server

## Requirements

- Python 3.x
- Flask

## Installation

1. Install Flask:
```bash
pip install flask
```

## Usage

Run the application:
```bash
python Periodic-table.py
```

The application will automatically open in your default browser at `http://127.0.0.1:5000`

## Element Categories

- **Alkali metals** - Highly reactive metals (Li, Na, K, etc.)
- **Alkaline earth metals** - Reactive metals (Be, Mg, Ca, etc.)
- **Transition metals** - Large central block of metals
- **Post-transition metals** - Metals after the transition series
- **Metalloids** - Elements with properties between metals and non-metals
- **Non-metals** - Elements lacking metallic properties
- **Noble gases** - Inert gases (He, Ne, Ar, etc.)
- **Lanthanides** - Rare earth elements (La-Lu)
- **Actinides** - Radioactive elements (Ac-Lr)

## Project Structure

- `Periodic-table.py` - Single-file Flask application containing:
  - Complete element data (atomic number, symbol, name, group, period, category, atomic mass)
  - HTML/CSS/JavaScript for the interactive interface
  - Flask routes for serving the application

## License

MIT
