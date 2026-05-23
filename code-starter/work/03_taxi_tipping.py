"""Step-by-step tipping analysis on the yellow-taxi data.

We walk through filter → derive → group → aggregate, showing the
intermediate DataFrame at each step. Then we look at how tipping
varies by hour, and finally a percentile distribution of tip %.

If you know SQL, the SQL equivalent is shown alongside each PySpark call.

Note: TLC reports cash tips as $0 (payment_type=2 always shows
tip_amount=0). Most of the analysis below filters to credit-card trips
(payment_type=1) because that's the only honest tip signal.
"""
import time

from pyspark.sql import functions as F

from constants import TAXI_PARQUET
from spark_helper import get_spark, print_ui_urls, require_files


def main() -> None:
    require_files((TAXI_PARQUET, "make download-nyc-cab-data"))
    spark = get_spark("cs675-taxi-tipping")
    start = time.time()

    print(">>> Step 1: Read the Parquet — peek at payment + tip columns")
    print("PySpark: spark.read.parquet(TAXI_PARQUET)")
    print("SQL    : SELECT payment_type, fare_amount, tip_amount FROM 'yellow.parquet' LIMIT 5")
    df = spark.read.parquet(TAXI_PARQUET)                                   # load fact table
    df.select("payment_type", "fare_amount", "tip_amount").show(5, truncate=False)
    print(f"Starting rows: {df.count():,}")

    print("\n>>> Step 2: Drop rows with fare_amount <= 0 (avoid div-by-zero in the next step)")
    print("PySpark: df.filter(F.col('fare_amount') > 0)")
    print("SQL    : SELECT * FROM df WHERE fare_amount > 0")
    df = df.filter(F.col("fare_amount") > 0)                                # data-quality filter
    print(f"After filter: {df.count():,} rows")

    print("\n>>> Step 3: Derive a new column tip_pct = tip / fare * 100")
    print("PySpark: df.withColumn('tip_pct', F.col('tip_amount') / F.col('fare_amount') * 100)")
    print("SQL    : SELECT *, tip_amount / fare_amount * 100 AS tip_pct FROM df")
    df = df.withColumn(
        "tip_pct",
        F.col("tip_amount") / F.col("fare_amount") * 100,                   # tip as % of fare
    )
    df.select("payment_type", "fare_amount", "tip_amount", "tip_pct").show(5, truncate=False)

    print("\n>>> Step 4: Group by payment_type and aggregate")
    print("PySpark: df.groupBy('payment_type').agg(avg tip_pct, avg tip_usd, count)")
    print("SQL    : SELECT payment_type,")
    print("                ROUND(AVG(tip_pct), 2)    AS avg_tip_pct,")
    print("                ROUND(AVG(tip_amount), 2) AS avg_tip_usd,")
    print("                COUNT(*)                  AS n_trips")
    print("         FROM df GROUP BY payment_type ORDER BY payment_type")
    print("Legend: 1=credit, 2=cash, 3=no charge, 4=dispute, 5=unknown, 6=voided")
    (
        df.groupBy("payment_type")
        .agg(                                                                 # multiple aggregates in one pass
            F.round(F.avg("tip_pct"), 2).alias("avg_tip_pct"),
            F.round(F.avg("tip_amount"), 2).alias("avg_tip_usd"),
            F.count("*").alias("n_trips"),
        )
        .orderBy("payment_type").show(truncate=False)
    )
    print("Notice: cash trips (payment_type=2) show avg tip = $0. TLC doesn't record cash tips.")

    print("\n>>> Step 5: Filter to credit cards only (the only honest tip signal)")
    print("PySpark: df.filter(F.col('payment_type') == 1)")
    print("SQL    : SELECT * FROM df WHERE payment_type = 1")
    cc = df.filter(F.col("payment_type") == 1)                              # credit-card subset
    print(f"Credit-card rows: {cc.count():,}")

    print("\n>>> Step 6: Derive hour-of-day, group, aggregate")
    print("PySpark: cc.withColumn('hour', F.hour('tpep_pickup_datetime')).groupBy('hour').agg(...)")
    print("SQL    : SELECT EXTRACT(HOUR FROM tpep_pickup_datetime) AS hour,")
    print("                ROUND(AVG(tip_pct), 2) AS avg_tip_pct,")
    print("                COUNT(*)               AS n_trips")
    print("         FROM cc GROUP BY 1 ORDER BY 1")
    by_hour = (
        cc.withColumn("hour", F.hour("tpep_pickup_datetime"))               # extract hour from timestamp
        .groupBy("hour")
        .agg(
            F.round(F.avg("tip_pct"), 2).alias("avg_tip_pct"),
            F.count("*").alias("n_trips"),
        )
        .orderBy("hour")
    )
    by_hour.show(24, truncate=False)

    print("\n>>> Step 7: Approximate quantiles of credit-card tip percentage")
    print("PySpark: cc.approxQuantile('tip_pct', [...], 0.01)")
    print("SQL    : SELECT APPROX_PERCENTILE(tip_pct, 0.5) FROM cc   -- (Spark SQL / Trino)")
    # approxQuantile uses a sketch algorithm — cheap percentile estimates on big data.
    pcts = cc.approxQuantile("tip_pct", [0.10, 0.25, 0.50, 0.75, 0.90, 0.99], 0.01)
    print("Distribution of tip_pct (credit-card trips only):")
    for label, value in zip(["p10", "p25", "p50", "p75", "p90", "p99"], pcts):
        print(f"  {label}: {value:.2f}%")
    print("\nNotice: the median (p50) is much smaller than the mean from Step 4 —")
    print("a few outliers (huge tip% on tiny fares) drag the mean up. This is exactly")
    print("the case where mean is misleading and median is the honest summary.")

    print(f"\nDone in {time.time() - start:.2f}s.")
    print_ui_urls()
    spark.stop()


if __name__ == "__main__":
    main()
