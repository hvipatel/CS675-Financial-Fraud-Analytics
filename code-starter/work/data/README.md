# `work/data/`

Drop downloaded datasets here. Everything in this folder is gitignored except this README — files won't be committed by accident.

## Three datasets, three shapes

| File | Format | Size | Source | Download |
|---|---|---|---|---|
| `yellow_tripdata_2024-01.parquet` | **Parquet** (primary fact table) | ~48 MB / ~3 M rows | NYC TLC | `make download-nyc-cab-data` |
| `taxi_zone_lookup.csv` | **Small CSV** (dimension table) | ~12 KB / 265 rows | NYC TLC | `make download-nyc-cab-zones-data` |
| `JC-202401-citibike-tripdata.csv` | **Large CSV** (standalone) | ~10 MB / ~50 K rows | Citi Bike | `make download-nyc-bikes-data` |
| `shakespeare_complete_works.txt` | **Plain text** (word-count demo) | ~5.6 MB | Project Gutenberg | `make download-shakespeare-data` |

All four live behind Make targets that are idempotent — re-running them is a no-op if the file is already present. The Make targets run `curl` inside the container, so you don't need any download tools on your host.

```bash
# Linux / macOS / WSL
make download-nyc-cab-data && make download-nyc-cab-zones-data && make download-nyc-bikes-data && make download-shakespeare-data

# Windows PowerShell
.\make.ps1 download-nyc-cab-data; .\make.ps1 download-nyc-cab-zones-data; .\make.ps1 download-nyc-bikes-data; .\make.ps1 download-shakespeare-data
```

### Why these four

- **`yellow_tripdata_2024-01.parquet`** — recurring across labs. Real, dirty, columnar. Single month at ~3 M rows is small enough for any laptop, big enough to feel like data.
- **`taxi_zone_lookup.csv`** — the dimension table for `PULocationID` / `DOLocationID` in the Parquet. Use it to teach CSV reading, **broadcast joins**, and the star-schema fact + dimension pattern. See `work/06_zones_analysis.py`.
- **`JC-202401-citibike-tripdata.csv`** — standalone Jersey City Citi Bike trips. Real timestamps, real station names, real member-vs-casual splits. Use it to teach **schema inference vs declared schema** (about 25× slower vs faster on this file) and **CSV → Parquet conversion** (Parquet is ~25% of CSV size on this data). See `work/07_citibike_analysis.py`.
- **`shakespeare_complete_works.txt`** — Shakespeare's complete works from Project Gutenberg. The canonical text corpus for the classic MapReduce **word-count** example. Use it to teach text reading, tokenization, and the Map → Reduce pattern in Spark. See `work/01_word_count.py`.

### Manual download (without Make)

If you want a different month or aren't using Docker:

```bash
# bash / WSL
curl -L -o yellow_tripdata_2024-01.parquet \
  https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet
curl -L -o taxi_zone_lookup.csv \
  https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
curl -L -o citibike.zip \
  https://s3.amazonaws.com/tripdata/JC-202401-citibike-tripdata.csv.zip
unzip -p citibike.zip "JC-*.csv" > JC-202401-citibike-tripdata.csv && rm citibike.zip
curl -L -o shakespeare_complete_works.txt \
  https://www.gutenberg.org/cache/epub/100/pg100.txt
```

```powershell
# PowerShell
Invoke-WebRequest -Uri "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet" -OutFile yellow_tripdata_2024-01.parquet
Invoke-WebRequest -Uri "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv" -OutFile taxi_zone_lookup.csv
Invoke-WebRequest -Uri "https://s3.amazonaws.com/tripdata/JC-202401-citibike-tripdata.csv.zip" -OutFile citibike.zip
Expand-Archive citibike.zip -DestinationPath . ; Remove-Item citibike.zip
Invoke-WebRequest -Uri "https://www.gutenberg.org/cache/epub/100/pg100.txt" -OutFile shakespeare_complete_works.txt
```

Other months for taxi / Citi Bike: change the date in the URL. The full lists are at the [NYC TLC trip record page](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) and the [Citi Bike data page](https://citibikenyc.com/system-data).

### Reading from a notebook

```python
trips = spark.read.parquet("/home/jovyan/work/data/yellow_tripdata_2024-01.parquet")
zones = spark.read.option("header", "true").option("inferSchema", "true").csv(
    "/home/jovyan/work/data/taxi_zone_lookup.csv"
)
bikes = spark.read.option("header", "true").option("inferSchema", "true").csv(
    "/home/jovyan/work/data/JC-202401-citibike-tripdata.csv"
)
shake = spark.read.text("/home/jovyan/work/data/shakespeare_complete_works.txt")
```

(Native non-Docker path: replace `/home/jovyan/work/data/...` with `work/data/...` relative to the project root.)
