# CS-675 Code Starter

PySpark dev environment for CS-675. Choose your path:

- **Docker** (recommended) → [README-docker.md](README-docker.md)
- **Native macOS** → [README-mac.md](README-mac.md)
- **Native Windows** → [README-windows.md](README-windows.md)

All three paths run the same scripts and pass the same test suite. The Docker path adds an always-on **Spark History Server** at http://localhost:18080 alongside the live Spark UI; the native paths run the live UI only.

## What's in this directory

```
code-starter/
├── docker-compose.yml            # Docker setup: pyspark + Spark History Server
├── Makefile                      # workflow targets — macOS / Linux / WSL
├── make.ps1                      # workflow targets — Windows PowerShell
├── pyproject.toml                # Python deps for the native paths (uv)
├── .python-version               # pins Python 3.12 for native paths
├── tests/
│   ├── test_spark.py             # smoke tests (SparkSession, DataFrame, filter, group-by)
│   └── test_taxi_analysis.py     # integration tests against the NYC taxi Parquet
└── work/                         # your code goes here (bind-mounted into the container)
    ├── constants.py              # data paths, ports, container detection
    ├── spark_helper.py           # get_spark(), print_ui_urls(), require_files()
    ├── 00_hello_spark.py         # smoke test                  — make hello
    ├── 01_taxi_analysis.py       # cab trip overview           — make analyze-nyc-cab-data-use-case-a
    ├── 02_taxi_tipping.py        # cab tipping behavior        — make analyze-nyc-cab-data-use-case-b
    ├── 03_taxi_payments.py       # cab payment methods         — make analyze-nyc-cab-data-use-case-c
    ├── 04_zones_analysis.py      # cab × zones broadcast join  — make analyze-nyc-cab-data-use-case-d
    ├── 05_citibike_analysis.py   # CSV → Parquet on Citi Bike  — make analyze-nyc-bikes-data-use-case-a
    └── data/                     # downloaded datasets (gitignored)
        └── README.md             # what each dataset is and how to fetch it
```

Scripts are numbered `00` → `05` in **rising order of complexity** — start at `00`, work up. The three `taxi_*` scripts (`01`–`03`) all run against the same Parquet but ask different questions; `04` brings in a second dataset and a broadcast join; `05` introduces declared schemas and a CSV → Parquet conversion.

`Makefile` and `make.ps1` expose the **same target names**. Use whichever fits your shell:

| Group | Targets |
|---|---|
| Lifecycle | `up`, `down`, `restart`, `logs`, `shell`, `clean` |
| Datasets | `download-nyc-cab-data`, `download-nyc-cab-zones-data`, `download-nyc-bikes-data` |
| Analyses (cab data) | `analyze-nyc-cab-data-use-case-{a,b,c,d}` — same Parquet, different questions |
| Analyses (bikes data) | `analyze-nyc-bikes-data-use-case-a` |
| Other | `hello`, `test`, `history` |
