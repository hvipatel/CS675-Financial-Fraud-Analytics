"""Yellow-taxi headline stats: busiest pickup hours, fare vs passenger count, longest trips."""
import time

from pyspark.sql import functions as F

from constants import TAXI_PARQUET
from spark_helper import get_spark, print_ui_urls, require_files


def main() -> None:
    require_files((TAXI_PARQUET, "make download-nyc-cab-data"))
    spark = get_spark("cs675-taxi-analysis")
    start = time.time()

    df = spark.read.parquet(TAXI_PARQUET)
    print(f"Rows: {df.count():,}    Columns: {len(df.columns)}")

    print("\n--- Top 5 pickup hours by trip count ---")
    (
        df.withColumn("hour", F.hour("tpep_pickup_datetime"))
        .groupBy("hour").count()
        .orderBy(F.col("count").desc()).limit(5)
        .show(truncate=False)
    )

    print("--- Average fare and trip count by passenger count ---")
    (
        df.groupBy("passenger_count")
        .agg(
            F.round(F.avg("fare_amount"), 2).alias("avg_fare_usd"),
            F.count("*").alias("n_trips"),
        )
        .orderBy("passenger_count").show(truncate=False)
    )

    print("--- Top 10 longest trips by distance ---")
    (
        df.select("trip_distance", "fare_amount", "total_amount")
        .orderBy(F.col("trip_distance").desc()).limit(10)
        .show(truncate=False)
    )

    print(f"\nDone in {time.time() - start:.2f}s.")
    print_ui_urls()
    spark.stop()


if __name__ == "__main__":
    main()
