"""Binary classification with Spark MLlib — covers Lecture 2b (Data Mining tasks).

Question: can we predict whether a credit-card trip received any tip at all,
using features available at the start of the trip (distance, fare, hour,
passenger count)?

Pipeline:
  1. Filter to credit-card trips (cash tips aren't recorded — they'd be a
     guaranteed `0`, which leaks the answer).
  2. Build a binary target `tipped = 1 if tip_amount > 0 else 0`.
  3. Assemble features into a single vector column (MLlib's input format).
  4. Train/test split.
  5. Fit Logistic Regression.
  6. Evaluate with AUC (area under the ROC curve).

This is the canonical *Classification* task from Lecture 2b §4.4 — the model
sees labeled training rows, learns the pattern, then assigns predicted labels
to records where the outcome is unknown.
"""
import time

from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import functions as F

from constants import TAXI_PARQUET
from spark_helper import get_spark, print_ui_urls, require_files


FEATURE_COLS = ["trip_distance", "fare_amount", "passenger_count", "hour"]


def main() -> None:
    require_files((TAXI_PARQUET, "make download-nyc-cab-data"))
    spark = get_spark("cs675-taxi-classification")
    start = time.time()

    df = (
        spark.read.parquet(TAXI_PARQUET)
        .filter(F.col("payment_type") == 1)                              # credit-card only — cash tips not recorded
        .filter(F.col("fare_amount") > 0)                                # drop bad fares
        .filter(F.col("trip_distance") > 0)                              # drop bad distances
        .withColumn("hour", F.hour("tpep_pickup_datetime"))              # derived feature: hour-of-day
        .withColumn("tipped", (F.col("tip_amount") > 0).cast("int"))     # binary target: 1 if any tip
        .na.drop(subset=FEATURE_COLS + ["tipped"])                       # drop rows with nulls in features/target
    )
    n_total = df.count()
    print(f"Modelling rows: {n_total:,}")

    # Class balance — important to know before claiming "X% accuracy".
    print("\n--- Class distribution ---")
    df.groupBy("tipped").count().orderBy("tipped").show(truncate=False)

    # ----- Feature assembly -----
    # MLlib expects ALL features in a single vector column called "features".
    assembler = VectorAssembler(inputCols=FEATURE_COLS, outputCol="features")

    # ----- Model -----
    # featuresCol/labelCol tell LR which columns to use.
    lr = LogisticRegression(featuresCol="features", labelCol="tipped", maxIter=10)

    # Pipeline chains stages — fit() runs them in order, transform() applies them.
    pipeline = Pipeline(stages=[assembler, lr])

    # ----- Train/test split -----
    # randomSplit shuffles + slices; seed makes it reproducible across runs.
    train, test = df.randomSplit([0.8, 0.2], seed=42)
    print(f"\nTrain rows: {train.count():,}    Test rows: {test.count():,}")

    print("\nFitting LogisticRegression...")
    t0 = time.time()
    model = pipeline.fit(train)                                          # training step: lazy → action via fit()
    print(f"  trained in {time.time() - t0:.2f}s")

    # ----- Inference + evaluation -----
    predictions = model.transform(test)                                  # add prediction columns to test set
    print("\n--- Sample predictions ---")
    predictions.select(
        "trip_distance", "fare_amount", "hour", "tipped", "prediction", "probability",
    ).limit(5).show(truncate=False)

    # AUC: area under the ROC curve. 1.0 = perfect, 0.5 = random guessing.
    evaluator = BinaryClassificationEvaluator(
        labelCol="tipped", rawPredictionCol="rawPrediction", metricName="areaUnderROC",
    )
    auc = evaluator.evaluate(predictions)
    print(f"\nTest AUC: {auc:.4f}")

    # Coefficients tell us which features push toward "tipped". For LR they're
    # log-odds — positive coefficient → higher predicted probability of tipping.
    lr_model = model.stages[-1]                                          # the trained LR stage
    print("\n--- Feature coefficients (log-odds) ---")
    for col, coef in zip(FEATURE_COLS, lr_model.coefficients):
        print(f"  {col:>18}: {coef:+.4f}")
    print(f"  {'intercept':>18}: {lr_model.intercept:+.4f}")

    print(f"\nDone in {time.time() - start:.2f}s.")
    print_ui_urls()
    spark.stop()


if __name__ == "__main__":
    main()
