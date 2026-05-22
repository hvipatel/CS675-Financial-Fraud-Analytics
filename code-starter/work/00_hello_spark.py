"""Smoke test: confirm PySpark is wired up and a tiny DataFrame runs end-to-end."""
import pyspark

from spark_helper import get_spark, print_ui_urls

print(f"PySpark version: {pyspark.__version__}")

spark = get_spark("cs675-hello")
print(f"Default parallelism: {spark.sparkContext.defaultParallelism}")
print(f"Spark master:        {spark.sparkContext.master}")
print_ui_urls()

df = spark.createDataFrame([(i, i * i) for i in range(10)], ["x", "x_squared"])
df.show()
print(f"Row count: {df.count()}")
print("\nSmoke test passed.")

spark.stop()
