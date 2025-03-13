# configuration.py

# Main properties
TITLE = 'WeWorld Index Italia 2025'
BRAND_LINK = "https:/weworld.it/"
CREDITS_LINK = "https://github.com/aripiz"

TEMPLATE = 'journal'

# Themes and colors
TEMPLATE_CSS = f"https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/{TEMPLATE}/bootstrap.min.css"
FIGURE_TEMPLATE = TEMPLATE.lower()
DBC_CSS = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

BRAND_COLOR = '#005D9E'
TIER_COLORS = [
    "#D53A50",  # Red
    "#E97B4E",  # Orange
    "#F0B060",  # Yellow
    "#DECE58",  # Light Yellow
    "#64A972",  # Green
    "#3E876B"   # Dark Green
]
SEQUENCE_COLOR = [
    "#3c3c3c",  # Dark Gray
    "#d55350",  # Coral Red
    "#41c072",  # Emerald Green
    "#ffc15f",  # Light Yellow
    "#439acf",  # Sky Blue
    "#7b4c39",  # Warm Brown
    "#a64d79",  # Dark Pink
    "#2e8b57",  # Forest Green
    "#ff6f00",  # Vivid Orange
    "#1e90ff"   # Dodger Blue
]

# Tiers
TIER_LABELS = ['Limitato', 'Minimo', 'Base', 'Moderato', 'Forte', 'Avanzato']
TIER_BINS = [0, 45, 55, 65, 75, 85, 100]

# Map configuration
LAND_COLOR = "#3B3B3B"
OCEAN_COLOR = "#F2F2F2"
GEO_KEY = "properties.istat_code_num"
INDEX_KEY = "WeWorld Index Italia"

# Files link
DATA_FILE = "../data/weworld-index-2025_data.csv" 
META_FILE = "../data/weworld-index-2025_metadata.csv" 
GEO_FILE = "../data/italy_regions_low.json"
NOTES_FILE = "" 
REPORT_FILE =  ""
