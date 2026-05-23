"""Smoke test: confirm PySpark is wired up and a tiny DataFrame runs end-to-end."""
import pyspark

from spark_helper import get_spark, print_ui_urls

print(f"PySpark version: {pyspark.__version__}")

# Build (or attach to) a SparkSession — the entry point to every Spark program.
spark = get_spark("cs675-hello")
print(f"Default parallelism: {spark.sparkContext.defaultParallelism}")
print(f"Spark master:        {spark.sparkContext.master}")
print_ui_urls()

# Create a tiny DataFrame in memory — no file I/O, just enough to prove Spark works.
df = spark.createDataFrame([(i, i * i) for i in range(10)], ["x", "x_squared"])
df.show()                       # action: triggers compute, prints the DataFrame
print(f"Row count: {df.count()}")  # action: count() also forces evaluation

print("\nSmoke test passed.")
spark.stop()
