kaziranga-sar-change-detector/
├── .github/
│   └── workflows/
│       └── ci-pages.yml            # tests + deploy frontend to GitHub Pages
├── The_Larpers/
│   ├── backend/
│   │   ├── processing/
│   │   │   ├── 01_inspect_tifs.py          # check grid and stats
│   │   │   ├── 02_process_nisar.py         # masks, frequency, vegetation, metrics
│   │   │   ├── 03_validate_gsw.py          # compare with JRC Global Surface Water
│   │   │   ├── 04_update_readme_table.py   # rebuild README results table
│   │   │   └── sar_utils.py                # shared helpers
│   │   └── tests/
│   │       └── test_sar_utils.py           # unit tests (no rasters needed)
│   ├── docs/
│   │   ├── DATA.md                         # how to get the input data
│   │   ├── hh_histogram.png                # backscatter histogram
│   │   └── project_diagram.svg             # pipeline diagram
│   ├── frontend/                           # this folder is what gets deployed
│   │   ├── index.html                      # the web app
│   │   └── data/
│   │       ├── nisar_metrics.json
│   │       ├── inundation_frequency.png
│   │       ├── water_<date>.png            # 10 files
│   │       ├── rgb_<date>.webp             # 10 files
│   │       ├── veg_<date>.png              # 10 files
│   │       └── context_series.example.json
│   └── data/                               # local only, not committed
│       ├── raw_tifs/                       # the 20 input GeoTIFFs
│       └── gsw/                            # JRC GSW tile for validation
├── .gitignore
├── LICENSE
├── PROJECT_STRUCTURE.md
└── README.md
