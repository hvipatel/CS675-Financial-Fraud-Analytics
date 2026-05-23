"""Citi Bike CSV analysis:
schema inference vs declared schema (timed), aggregations, CSV → Parquet conversion.

At ~50K rows declared-schema CSV is competitive with Parquet on read time.
Parquet's columnar layout + predicate pushdown + compression pay off as the
file grows and as queries touch fewer columns — the disk-size win is already
visible here (Parquet is ~25% of the CSV size).
"""
import os
import time

from pyspark.sql import functions as F
from pyspark.sql.types import (
    DoubleType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

from constants import CITIBIKE_CSV
from spark_helper import get_spark, print_ui_urls, require_files


def declared_schema() -> StructType:
    """Explicit schema — single-pass CSV parse, no type sniffing."""
    return StructType([
        StructField("ride_id", StringType()),
        StructField("rideable_type", StringType()),
        StructField("started_at", TimestampType()),
        StructField("ended_at", TimestampType()),
        StructField("start_station_name", StringType()),
        StructField("start_station_id", StringType()),
        StructField("end_station_name", StringType()),
        StructField("end_station_id", StringType()),
        StructField("start_lat", DoubleType()),
        StructField("start_lng", DoubleType()),
        StructField("end_lat", DoubleType()),
        StructField("end_lng", DoubleType()),
        StructField("member_casual", StringType()),
    ])


def dir_size_mb(path: str) -> float:
    total = sum(
        os.path.getsize(os.path.join(root, f))
        for root, _, files in os.walk(path) for f in files
    )
    return total / 1_048_576


def main() -> None:
    require_files((CITIBIKE_CSV, "make download-nyc-bikes-data"))
    spark = get_spark("cs675-citibike")

    csv_mb = os.path.getsize(CITIBIKE_CSV) / 1_048_576
    print(f"CSV on disk: {csv_mb:.2f} MB")

    # ----- Schema inference: Spark reads the file TWICE (sniff + parse) -----
    t0 = time.time()
    n_inferred = (
        spark.read
        .option("header", "true").option("inferSchema", "true")          # inference makes 2 passes over the file
        .csv(CITIBIKE_CSV).count()                                         # count() forces the read
    )
    t_inferred = time.time() - t0

    # ----- Declared schema: one pass, no inference -----
    t0 = time.time()
    df = (
        spark.read
        .option("header", "true").schema(declared_schema())                # explicit schema → single pass
        .csv(CITIBIKE_CSV)
    )
    n_declared = df.count()
    t_declared = time.time() - t0

    print(f"inferSchema=true:  {n_inferred:,} rows in {t_inferred:.2f}s")
    print(f"declared schema:   {n_declared:,} rows in {t_declared:.2f}s "
          f"(~{t_inferred / t_declared:.0f}x faster)")

    print("\n--- Top 5 start stations ---")
    (
        df.filter(F.col("start_station_name").isNotNull())                # drop rows missing station name
        .groupBy("start_station_name").count()
        .orderBy(F.col("count").desc()).limit(5).show(truncate=False)
    )

    print("--- Rideable type by member status ---")
    (
        df.groupBy("rideable_type", "member_casual").count()              # group by two keys at once
        .orderBy("rideable_type", "member_casual").show(truncate=False)
    )

    print("--- Trips by hour of day ---")
    (
        df.withColumn("hour", F.hour("started_at"))                       # derived column from timestamp
        .groupBy("hour").count().orderBy("hour").show(24, truncate=False)
    )

    # ----- Write Parquet and compare sizes + read times -----
    parquet_path = CITIBIKE_CSV.replace(".csv", ".parquet")
    df.write.mode("overwrite").parquet(parquet_path)                      # write same data in columnar Parquet
    parquet_mb = dir_size_mb(parquet_path)

    t0 = time.time()
    n_pq = spark.read.parquet(parquet_path).count()                       # action: re-read Parquet
    t_pq = time.time() - t0

    print("--- CSV vs Parquet ---")
    print(f"  CSV:     {csv_mb:.2f} MB    declared-schema read: {t_declared:.2f}s")
    print(f"  Parquet: {parquet_mb:.2f} MB ({100 * parquet_mb / csv_mb:.0f}% of CSV)"
          f"    Parquet read: {t_pq:.2f}s ({n_pq:,} rows)")

    print_ui_urls()
    spark.stop()


if __name__ == "__main__":
    main()
