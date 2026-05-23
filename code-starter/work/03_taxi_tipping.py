"""Tipping behavior on the yellow-taxi Parquet.

TLC reports cash tips as $0 (payment_type=2 always shows tip_amount=0).
Credit-card tips (payment_type=1) are the only reliable signal — most of
the analysis below filters to that subset.
"""
import time

from pyspark.sql import functions as F

from constants import TAXI_PARQUET
from spark_helper import get_spark, print_ui_urls, require_files


def main() -> None:
    require_files((TAXI_PARQUET, "make download-nyc-cab-data"))
    spark = get_spark("cs675-taxi-tipping")
    start = time.time()

    df = (
        spark.read.parquet(TAXI_PARQUET)
        .filter(F.col("fare_amount") > 0)                                          # drop zero/negative fares (avoid div-by-zero in tip_pct)
        .withColumn("tip_pct", F.col("tip_amount") / F.col("fare_amount") * 100)  # derived: tip as % of fare
    )

    print("--- Avg tip and tip % by payment type ---")
    print("  (1=credit, 2=cash, 3=no charge, 4=dispute, 5=unknown, 6=voided)")
    (
        df.groupBy("payment_type")
        .agg(
            F.round(F.avg("tip_pct"), 2).alias("avg_tip_pct"),                     # mean of derived column
            F.round(F.avg("tip_amount"), 2).alias("avg_tip_usd"),
            F.count("*").alias("n_trips"),
        )
        .orderBy("payment_type").show(truncate=False)
    )

    print("--- Credit-card tip % by pickup hour ---")
    (
        df.filter(F.col("payment_type") == 1)                                       # credit cards only — cash tips aren't recorded
        .withColumn("hour", F.hour("tpep_pickup_datetime"))                         # derived: hour bucket
        .groupBy("hour")
        .agg(
            F.round(F.avg("tip_pct"), 2).alias("avg_tip_pct"),
            F.count("*").alias("n_trips"),
        )
        .orderBy("hour").show(24, truncate=False)
    )

    print("--- Credit-card tip-percentage distribution ---")
    # approxQuantile uses a sketch algorithm — cheap percentile estimates on big data.
    pcts = (
        df.filter(F.col("payment_type") == 1)
        .approxQuantile("tip_pct", [0.10, 0.25, 0.50, 0.75, 0.90, 0.99], 0.01)
    )
    for label, value in zip(["p10", "p25", "p50", "p75", "p90", "p99"], pcts):
        print(f"  {label}: {value:.2f}%")

    print(f"\nDone in {time.time() - start:.2f}s.")
    print_ui_urls()
    spark.stop()


if __name__ == "__main__":
    main()
