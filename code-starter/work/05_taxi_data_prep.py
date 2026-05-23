"""Data-preparation pipeline on the yellow-taxi Parquet — covers Lecture 3 (Data Prep).

Walks through the core preprocessing operations every project hits before any
modelling can start: missing-value inspection + imputation, IQR-based outlier
detection, z-score normalization, equal-frequency binning, and one-hot encoding
of a categorical column.

Larose's "60% of effort is data prep" claim — this script demonstrates the
actual operations that 60% is made of.
"""
import time

from pyspark.sql import functions as F

from constants import TAXI_PARQUET
from spark_helper import get_spark, print_ui_urls, require_files


def main() -> None:
    require_files((TAXI_PARQUET, "make download-nyc-cab-data"))
    spark = get_spark("cs675-taxi-data-prep")
    start = time.time()

    df = spark.read.parquet(TAXI_PARQUET)                              # read Parquet fact table
    total = df.count()
    print(f"Starting rows: {total:,}")

    # ----- 1. Missing-value inspection -----------------------------------
    print("\n--- Missing-value counts per column ---")
    # F.col(c).isNull().cast("int") yields 0/1; sum over the column → null count.
    null_counts = df.select([
        F.sum(F.col(c).isNull().cast("int")).alias(c)                  # null-count per column
        for c in ["passenger_count", "trip_distance", "fare_amount", "RatecodeID"]
    ])
    null_counts.show(truncate=False)                                    # action

    # ----- 2. Imputation: fill missing passenger_count with the median ---
    # approxQuantile returns a list of percentile estimates; [0.5] is the median.
    median_passengers = df.approxQuantile("passenger_count", [0.5], 0.01)[0]
    print(f"\nMedian passenger_count = {median_passengers}")
    df = df.fillna({"passenger_count": median_passengers})              # fill with median
    print("After fillna, passenger_count nulls:", df.filter(F.col("passenger_count").isNull()).count())

    # ----- 3. Outlier detection via IQR rule -----------------------------
    # IQR rule: a value is an outlier if it sits >1.5*IQR below Q1 or above Q3.
    # More robust than the z-score rule when outliers exist (which they do here).
    q1, q3 = df.approxQuantile("trip_distance", [0.25, 0.75], 0.01)
    iqr = q3 - q1
    low_cutoff  = q1 - 1.5 * iqr
    high_cutoff = q3 + 1.5 * iqr
    print(f"\ntrip_distance quartiles: Q1={q1:.2f}  Q3={q3:.2f}  IQR={iqr:.2f}")
    print(f"  outlier cutoffs: [{low_cutoff:.2f}, {high_cutoff:.2f}]")

    df_with_flag = df.withColumn(                                       # flag (don't drop) outliers
        "is_distance_outlier",
        (F.col("trip_distance") < low_cutoff) | (F.col("trip_distance") > high_cutoff)
    )
    n_outliers = df_with_flag.filter(F.col("is_distance_outlier")).count()
    print(f"  flagged {n_outliers:,} of {total:,} rows ({100 * n_outliers / total:.2f}%) as distance outliers")

    # ----- 4. Z-score normalization of fare_amount -----------------------
    # Z = (X - mean) / sd — puts the column on a comparable scale (mean 0, sd 1).
    stats = df.agg(
        F.avg("fare_amount").alias("mean_fare"),
        F.stddev("fare_amount").alias("sd_fare"),
    ).collect()[0]                                                       # action: collect the one-row result
    mean_fare, sd_fare = stats["mean_fare"], stats["sd_fare"]
    print(f"\nfare_amount stats: mean={mean_fare:.2f}  sd={sd_fare:.2f}")

    df_normalized = df.withColumn(
        "fare_z",
        (F.col("fare_amount") - F.lit(mean_fare)) / F.lit(sd_fare),     # derived: standardized fare
    )

    print("--- Sample of normalized fare (5 rows) ---")
    df_normalized.select("fare_amount", "fare_z").limit(5).show(truncate=False)

    # ----- 5. Equal-frequency binning of trip_distance --------------------
    # Equal-frequency binning splits the data into buckets with the same row
    # count each, so outliers don't drag the bin widths around (unlike equal-width).
    # We pick the quartile boundaries explicitly so each bin holds ~25% of rows.
    p25, p50, p75 = df.approxQuantile("trip_distance", [0.25, 0.5, 0.75], 0.01)
    print(f"\nDistance bin boundaries (quartile-based): "
          f"<{p25:.2f}, <{p50:.2f}, <{p75:.2f}, >=")

    df_binned = df.withColumn(
        "distance_bin",
        F.when(F.col("trip_distance") < p25, "Q1_short")                 # bottom 25%
         .when(F.col("trip_distance") < p50, "Q2_medium")
         .when(F.col("trip_distance") < p75, "Q3_long")
         .otherwise("Q4_very_long"),                                     # top 25%
    )

    print("--- Trip count per distance bin ---")
    df_binned.groupBy("distance_bin").count().orderBy("distance_bin").show(truncate=False)

    # ----- 6. One-hot encoding of payment_type ----------------------------
    # k - 1 indicator columns for k categories (drop one as the reference).
    # payment_type codes 1–6; we treat 1 (credit_card) as the reference.
    df_onehot = (
        df
        .withColumn("pay_cash",      (F.col("payment_type") == 2).cast("int"))  # 0/1 flag
        .withColumn("pay_no_charge", (F.col("payment_type") == 3).cast("int"))
        .withColumn("pay_dispute",   (F.col("payment_type") == 4).cast("int"))
        .withColumn("pay_unknown",   (F.col("payment_type") == 5).cast("int"))
        .withColumn("pay_voided",    (F.col("payment_type") == 6).cast("int"))
    )

    print("--- One-hot encoding sample (5 rows) ---")
    df_onehot.select(
        "payment_type", "pay_cash", "pay_no_charge",
        "pay_dispute", "pay_unknown", "pay_voided",
    ).limit(5).show(truncate=False)

    print(f"\nData-prep pipeline complete in {time.time() - start:.2f}s.")
    print_ui_urls()
    spark.stop()


if __name__ == "__main__":
    main()
