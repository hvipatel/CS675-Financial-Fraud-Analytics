"""Broadcast-join the taxi zone lookup CSV with the yellow-taxi Parquet:
top 10 pickup zones and average fare per pickup borough.

The lookup is ~265 rows; the fact table is ~3 M. `F.broadcast()` documents
intent — Spark would auto-broadcast a dimension this small anyway, but the
explicit hint avoids a shuffle if the auto-broadcast threshold ever changes.
"""
import time

from pyspark.sql import functions as F

from constants import TAXI_PARQUET, ZONES_CSV
from spark_helper import get_spark, print_ui_urls, require_files


def main() -> None:
    require_files(
        (TAXI_PARQUET, "make download-nyc-cab-data"),
        (ZONES_CSV,    "make download-nyc-cab-zones-data"),
    )
    spark = get_spark("cs675-zones-join")
    start = time.time()

    # Small CSV: schema inference is cheap because the file is tiny.
    zones = (
        spark.read
        .option("header", "true").option("inferSchema", "true")             # read CSV w/ header + types inferred
        .csv(ZONES_CSV)
    )
    trips = spark.read.parquet(TAXI_PARQUET)                                 # big fact table from Parquet
    print(f"Zones: {zones.count()} rows    Trips: {trips.count():,} rows")

    # F.broadcast() sends the small dim table to every executor → no shuffle on the big fact.
    joined = trips.join(
        F.broadcast(zones),
        trips["PULocationID"] == zones["LocationID"],                        # join on the foreign key
        "left",                                                               # keep all trips even if no zone matches
    )

    print("\n--- Top 10 pickup zones by trip count ---")
    (
        joined.groupBy("Borough", "Zone").count()                            # aggregate at zone granularity
        .orderBy(F.col("count").desc()).limit(10)
        .show(truncate=False)
    )

    print("--- Average fare by pickup borough ---")
    (
        joined.groupBy("Borough")                                             # roll up one level to borough
        .agg(
            F.round(F.avg("fare_amount"), 2).alias("avg_fare_usd"),
            F.count("*").alias("n_trips"),
        )
        .orderBy(F.col("n_trips").desc()).show(truncate=False)
    )

    print(f"\nDone in {time.time() - start:.2f}s.")
    print_ui_urls()
    spark.stop()


if __name__ == "__main__":
    main()
