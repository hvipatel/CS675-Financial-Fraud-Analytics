"""Step-by-step yellow-taxi headline analysis.

We answer three questions:
  Q1. What hour-of-day has the most pickups?
  Q2. How does average fare vary with passenger count?
  Q3. What are the top-10 longest trips?

Q1 is fully step-by-step — read, peek, derive, group, sort. Q2 and Q3 use
the same shape of code more compactly once you've seen the building blocks.

If you know SQL, the SQL equivalent is shown alongside each PySpark call.
The script ends with the *same* Q1 written as a single SQL statement via
`spark.sql(...)` — both APIs run on the same engine and produce identical
plans, so use whichever feels natural.
"""
import time

from pyspark.sql import functions as F

from constants import TAXI_PARQUET
from spark_helper import get_spark, print_ui_urls, require_files


def main() -> None:
    require_files((TAXI_PARQUET, "make download-nyc-cab-data"))
    spark = get_spark("cs675-taxi-analysis")
    start = time.time()

    print(">>> Step 1: Read the Parquet fact table")
    print("PySpark: spark.read.parquet(TAXI_PARQUET)")
    print("SQL    : SELECT * FROM 'yellow_tripdata_2024-01.parquet'   -- (e.g. DuckDB / Athena)")
    df = spark.read.parquet(TAXI_PARQUET)                          # read Parquet → Spark DataFrame
    print(f"Rows: {df.count():,}    Columns: {len(df.columns)}")
    print("Schema (PySpark's printSchema; same idea as SQL's DESCRIBE):")
    df.printSchema()

    print("\n>>> Step 2: Peek at a few raw rows (just the columns we'll use)")
    print('PySpark: df.select("tpep_pickup_datetime", "fare_amount", "passenger_count", "trip_distance").show(5)')
    print("SQL    : SELECT tpep_pickup_datetime, fare_amount, passenger_count, trip_distance FROM df LIMIT 5")
    df.select(
        "tpep_pickup_datetime", "fare_amount", "passenger_count", "trip_distance",
    ).show(5, truncate=False)

    # ===================================================================
    # Q1. Busiest pickup hour — step-by-step
    # ===================================================================
    print("\n========= Q1. What hour-of-day has the most pickups? =========")

    print("\n>>> Step 3: Derive a 'hour' column from the timestamp")
    print('PySpark: df.withColumn("hour", F.hour("tpep_pickup_datetime"))')
    print("SQL    : SELECT *, EXTRACT(HOUR FROM tpep_pickup_datetime) AS hour FROM df")
    df_hour = df.withColumn("hour", F.hour("tpep_pickup_datetime"))   # extract hour-of-day (0–23)
    df_hour.select("tpep_pickup_datetime", "hour").show(5, truncate=False)

    print("\n>>> Step 4: Group by hour, count rows per hour")
    print("PySpark: df_hour.groupBy('hour').count()")
    print("SQL    : SELECT hour, COUNT(*) AS count FROM df_hour GROUP BY hour")
    hour_counts = df_hour.groupBy("hour").count()                     # one row per hour with a count column
    hour_counts.show(5, truncate=False)
    print("(24 hours → 24 groups; sample above is unsorted.)")

    print("\n>>> Step 5: Sort descending by count, take the top 5")
    print("PySpark: hour_counts.orderBy(F.col('count').desc()).limit(5)")
    print("SQL    : SELECT hour, count FROM hour_counts ORDER BY count DESC LIMIT 5")
    hour_counts.orderBy(F.col("count").desc()).limit(5).show(truncate=False)

    # ===================================================================
    # Q2. Average fare by passenger count — same pattern, compact form
    # ===================================================================
    print("\n========= Q2. Average fare and trip count by passenger count =========")
    print("PySpark: df.groupBy('passenger_count').agg(F.avg('fare_amount'), F.count('*'))")
    print("SQL    : SELECT passenger_count, ROUND(AVG(fare_amount), 2) AS avg_fare_usd,")
    print("                COUNT(*) AS n_trips")
    print("         FROM df GROUP BY passenger_count ORDER BY passenger_count")
    (
        df.groupBy("passenger_count")                                  # one group per passenger-count value
        .agg(                                                           # multiple aggregates in one pass
            F.round(F.avg("fare_amount"), 2).alias("avg_fare_usd"),
            F.count("*").alias("n_trips"),
        )
        .orderBy("passenger_count")
        .show(truncate=False)
    )

    # ===================================================================
    # Q3. Longest trips by distance
    # ===================================================================
    print("\n========= Q3. Top 10 longest trips by distance =========")
    print("PySpark: df.select(...).orderBy(F.col('trip_distance').desc()).limit(10)")
    print("SQL    : SELECT trip_distance, fare_amount, total_amount FROM df")
    print("         ORDER BY trip_distance DESC LIMIT 10")
    (
        df.select("trip_distance", "fare_amount", "total_amount")     # narrow projection (cheap in Parquet)
        .orderBy(F.col("trip_distance").desc())                        # sort descending
        .limit(10)
        .show(truncate=False)
    )
    print("Notice: the top entry is obviously bad data (300K+ miles). We'll handle outliers in Lecture 3.")

    # ===================================================================
    # Bonus: Q1 written as raw SQL via spark.sql()
    # ===================================================================
    print("\n========= Bonus: Q1 again, written as a single SQL statement =========")
    print("PySpark's DataFrame API and Spark SQL are two front-ends to the same engine —")
    print("they produce the same plan. Use whichever feels natural.")
    df.createOrReplaceTempView("trips")                                # register the DataFrame as a SQL-queryable view
    print("\nPySpark: spark.sql('SELECT EXTRACT(HOUR FROM ...) AS hour, COUNT(*) FROM trips GROUP BY 1 ORDER BY 2 DESC LIMIT 5')")
    spark.sql(
        """
        SELECT EXTRACT(HOUR FROM tpep_pickup_datetime) AS hour,
               COUNT(*) AS count
        FROM trips
        GROUP BY 1
        ORDER BY 2 DESC
        LIMIT 5
        """
    ).show(truncate=False)

    print(f"\nDone in {time.time() - start:.2f}s.")
    print_ui_urls()
    spark.stop()


if __name__ == "__main__":
    main()
