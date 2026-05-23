"""Payment-method analysis on the yellow-taxi Parquet:
trip count, revenue, average ticket size, and credit-vs-cash by hour of day.
"""
import time

from pyspark.sql import functions as F

from constants import TAXI_PARQUET
from spark_helper import get_spark, print_ui_urls, require_files


# TLC payment_type codes (1–6); anything else is "other".
PAYMENT_LABELS = {
    1: "credit_card",
    2: "cash",
    3: "no_charge",
    4: "dispute",
    5: "unknown",
    6: "voided",
}


def payment_label_col(code_col: str = "payment_type"):
    """Build a CASE-WHEN chain that turns numeric payment codes into label strings."""
    expr = F.lit("other")                                                # default arm: anything not matched below
    for code, label in PAYMENT_LABELS.items():
        expr = F.when(F.col(code_col) == code, label).otherwise(expr)   # stack when/otherwise
    return expr


def main() -> None:
    require_files((TAXI_PARQUET, "make download-nyc-cab-data"))
    spark = get_spark("cs675-taxi-payments")
    start = time.time()

    df = (
        spark.read.parquet(TAXI_PARQUET)
        .withColumn("payment_label", payment_label_col())                # derive readable label column
    )
    total_rows = df.count()

    print("--- Trip count, revenue, average ticket by payment method ---")
    (
        df.groupBy("payment_label")
        .agg(                                                             # multiple aggregates in one pass
            F.count("*").alias("n_trips"),
            F.round(F.sum("total_amount"), 0).alias("revenue_usd"),
            F.round(F.avg("total_amount"), 2).alias("avg_total_usd"),
            F.round(F.avg("fare_amount"), 2).alias("avg_fare_usd"),
        )
        .orderBy(F.col("n_trips").desc()).show(truncate=False)
    )

    print("--- Credit vs. cash share by hour ---")
    (
        df.filter(F.col("payment_label").isin("credit_card", "cash"))    # only the two big payment types
        .withColumn("hour", F.hour("tpep_pickup_datetime"))
        .groupBy("hour")
        .pivot("payment_label", ["credit_card", "cash"]).count()         # pivot: long → wide (one column per label)
        .orderBy("hour").show(24, truncate=False)
    )

    # Suspicious-row sanity check — refund-like trips.
    n_negative = df.filter(F.col("total_amount") < 0).count()
    print(f"Trips with total_amount < 0 (likely refunds): "
          f"{n_negative:,} of {total_rows:,} ({100 * n_negative / total_rows:.2f}%)")

    print(f"\nDone in {time.time() - start:.2f}s.")
    print_ui_urls()
    spark.stop()


if __name__ == "__main__":
    main()
