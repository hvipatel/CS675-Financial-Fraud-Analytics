"""Sample EMR Serverless PySpark job - the easiest working version to build on.

Test-first workflow (recommended):
  1. Run it locally on a SMALL sample to check the logic:
         pip install pyspark
         spark-submit sample_job.py   # after pointing INPUT at a small local/S3 file
  2. When it works, submit it to EMR Serverless at full scale: `make submit`.

Use AI to extend this step by step - add columns, filters, joins, or a model -
testing locally on a sample each step before you run it on the big data.
"""
from pyspark.sql import SparkSession, functions as F

# Replace these with your dataset and your workspace bucket.
INPUT = "s3://<DATASET_S3_LOCATION>/"
OUTPUT = "s3://<YOUR_BUCKET>/output/sample/"

spark = SparkSession.builder.appName("ds-sample").getOrCreate()

df = spark.read.parquet(INPUT)

result = (
    df.groupBy("payment_type")
    .agg(
        F.count("*").alias("trips"),
        F.round(F.avg("fare_amount"), 2).alias("avg_fare"),
    )
    .orderBy(F.col("trips").desc())
)

result.show()
result.write.mode("overwrite").parquet(OUTPUT)

spark.stop()
