# CS-675 code-starter — Windows PowerShell parallel to the Makefile.
#
# Same target names as the Makefile so docs can refer to either:
#   macOS / Linux / WSL:   make <target>
#   Windows PowerShell:    .\make.ps1 <target>
#
# Usage:
#   .\make.ps1 up
#   .\make.ps1 hello
#   .\make.ps1 download-nyc-cab-data
#   .\make.ps1 analyze-nyc-cab-data-use-case-a
#   .\make.ps1 help

param([string]$Target = "help")

$ErrorActionPreference = "Stop"

# NYC TLC yellow-taxi Parquet (~48 MB / ~3 M rows) — the primary fact table.
$NycCabUrl       = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
$NycCabFile      = "/home/jovyan/work/data/yellow_tripdata_2024-01.parquet"

# NYC TLC taxi zone lookup CSV (~12 KB / 265 rows) — small dimension table.
$NycCabZonesUrl  = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
$NycCabZonesFile = "/home/jovyan/work/data/taxi_zone_lookup.csv"

# JC Citi Bike monthly trips (~10 MB CSV / ~50 K rows) — large standalone CSV.
$NycBikesUrl     = "https://s3.amazonaws.com/tripdata/JC-202401-citibike-tripdata.csv.zip"
$NycBikesZip     = "/tmp/JC-202401-citibike-tripdata.csv.zip"
$NycBikesFile    = "/home/jovyan/work/data/JC-202401-citibike-tripdata.csv"

function Show-Help {
    Write-Host "CS-675 Code Starter — make.ps1 targets"
    Write-Host ""
    Write-Host "Container lifecycle"
    Write-Host "  .\make.ps1 up                                  Start containers (Jupyter :8888, Spark UI :4040, History :18080)"
    Write-Host "  .\make.ps1 down                                Stop containers"
    Write-Host "  .\make.ps1 restart                             Restart containers"
    Write-Host "  .\make.ps1 logs                                Tail container logs"
    Write-Host "  .\make.ps1 shell                               Open a bash shell inside the pyspark container"
    Write-Host "  .\make.ps1 clean                               Stop and remove named volumes (drops event-log history too)"
    Write-Host ""
    Write-Host "Datasets (download once, reused by analyses)"
    Write-Host "  .\make.ps1 download-nyc-cab-data               NYC TLC yellow-taxi Parquet  (~48 MB / ~3 M rows)"
    Write-Host "  .\make.ps1 download-nyc-cab-zones-data         NYC TLC taxi zone lookup CSV (~12 KB / 265 rows)"
    Write-Host "  .\make.ps1 download-nyc-bikes-data             JC Citi Bike monthly CSV     (~10 MB / ~50 K rows)"
    Write-Host ""
    Write-Host "Analyses on NYC cab data (same Parquet, different questions)"
    Write-Host "  .\make.ps1 analyze-nyc-cab-data-use-case-a     Trip overview          (01_taxi_analysis.py)"
    Write-Host "  .\make.ps1 analyze-nyc-cab-data-use-case-b     Tipping behavior       (02_taxi_tipping.py)"
    Write-Host "  .\make.ps1 analyze-nyc-cab-data-use-case-c     Payment methods        (03_taxi_payments.py)"
    Write-Host "  .\make.ps1 analyze-nyc-cab-data-use-case-d     Zones broadcast join   (04_zones_analysis.py - also needs the zones CSV)"
    Write-Host ""
    Write-Host "Analyses on NYC bikes data"
    Write-Host "  .\make.ps1 analyze-nyc-bikes-data-use-case-a   CSV vs Parquet         (05_citibike_analysis.py)"
    Write-Host ""
    Write-Host "Other"
    Write-Host "  .\make.ps1 hello                               Smoke test (00_hello_spark.py)"
    Write-Host "  .\make.ps1 test                                Run pytest inside the container"
    Write-Host "  .\make.ps1 history                             Print the Spark History Server URL"
}

function Show-Endpoints {
    Write-Host ""
    Write-Host "Jupyter Lab:    http://localhost:8888   (token: cs675)"
    Write-Host "Live Spark UI:  http://localhost:4040   (active while a SparkSession runs)"
    Write-Host "History Server: http://localhost:18080  (always up; shows past runs)"
}

switch ($Target.ToLower()) {
    "help"    { Show-Help }
    "up"      { docker compose up -d;   Show-Endpoints }
    "down"    { docker compose down }
    "restart" { docker compose down; docker compose up -d; Show-Endpoints }
    "logs"    { docker compose logs -f }
    "shell"   { docker compose exec pyspark bash }
    "hello"   { docker compose exec pyspark python /home/jovyan/work/00_hello_spark.py }

    "download-nyc-cab-data" {
        docker compose exec pyspark bash -c "test -f $NycCabFile && echo 'Already downloaded: $NycCabFile' || (echo 'Downloading NYC cab data...' && curl -L --fail -o $NycCabFile $NycCabUrl && echo 'Saved: $NycCabFile')"
    }
    "download-nyc-cab-zones-data" {
        docker compose exec pyspark bash -c "test -f $NycCabZonesFile && echo 'Already downloaded: $NycCabZonesFile' || (echo 'Downloading NYC cab zones data...' && curl -L --fail -o $NycCabZonesFile $NycCabZonesUrl && echo 'Saved: $NycCabZonesFile')"
    }
    "download-nyc-bikes-data" {
        docker compose exec pyspark bash -c "test -f $NycBikesFile && echo 'Already downloaded: $NycBikesFile' || (echo 'Downloading NYC bikes data...' && curl -L --fail -o $NycBikesZip $NycBikesUrl && unzip -p $NycBikesZip 'JC-*.csv' > $NycBikesFile && rm -f $NycBikesZip && echo 'Saved: $NycBikesFile')"
    }

    "analyze-nyc-cab-data-use-case-a"   { docker compose exec pyspark python /home/jovyan/work/01_taxi_analysis.py }
    "analyze-nyc-cab-data-use-case-b"   { docker compose exec pyspark python /home/jovyan/work/02_taxi_tipping.py }
    "analyze-nyc-cab-data-use-case-c"   { docker compose exec pyspark python /home/jovyan/work/03_taxi_payments.py }
    "analyze-nyc-cab-data-use-case-d"   { docker compose exec pyspark python /home/jovyan/work/04_zones_analysis.py }
    "analyze-nyc-bikes-data-use-case-a" { docker compose exec pyspark python /home/jovyan/work/05_citibike_analysis.py }

    "test" {
        docker compose exec pyspark python -m pip install -q pytest
        docker compose exec pyspark python -m pytest /home/jovyan/tests -v
    }
    "history" {
        Write-Host "Spark History Server: http://localhost:18080"
        Write-Host "(Refresh after a script finishes — completed apps appear automatically.)"
    }
    "clean"   { docker compose down -v }

    default {
        Write-Host "Unknown target: $Target"
        Write-Host "Run .\make.ps1 help for the available targets."
        exit 1
    }
}
