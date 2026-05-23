"""Step-by-step smoke test — a tour of SparkSession, DataFrame, and the basic ops.

We walk through each operation slowly and show the intermediate result so
you can see exactly what each function does. If you already know SQL, the
SQL equivalent is shown alongside each PySpark call. Later scripts (04+)
start chaining operations together; that's idiomatic Spark, but it's much
harder to read until you've done a few step-by-step walks.
"""
import pyspark
from pyspark.sql import functions as F

from spark_helper import get_spark, print_ui_urls

print(f"PySpark version: {pyspark.__version__}")

# The SparkSession is the entry point to every Spark program.
spark = get_spark("cs675-hello")
print(f"Default parallelism: {spark.sparkContext.defaultParallelism}")
print(f"Spark master:        {spark.sparkContext.master}")
print_ui_urls()


print("\n>>> Step 1: Start with a plain Python list of tuples")
data = [(i, i * i) for i in range(10)]
print(f"Python data (first 3 of {len(data)}): {data[:3]}")


print("\n>>> Step 2: Turn the list into a Spark DataFrame")
print('PySpark: spark.createDataFrame(data, ["x", "x_squared"])')
print("SQL    : CREATE TABLE df (x BIGINT, x_squared BIGINT); INSERT INTO df VALUES …;")
df = spark.createDataFrame(data, ["x", "x_squared"])     # convert Python data into a Spark DataFrame
print("Schema (PySpark's printSchema — same idea as SQL's DESCRIBE TABLE):")
df.printSchema()                                          # printSchema: column names + types
print("Contents:")
df.show()                                                  # show: action — triggers compute and prints


print("\n>>> Step 3: Add a derived column with withColumn()")
print('PySpark: df.withColumn("x_cubed", F.col("x") * F.col("x") * F.col("x"))')
print("SQL    : SELECT *, x * x * x AS x_cubed FROM df")
df_cubed = df.withColumn("x_cubed", F.col("x") * F.col("x") * F.col("x"))    # add new column based on existing ones
df_cubed.show()


print("\n>>> Step 4: Filter rows with filter()")
print('PySpark: df_cubed.filter(F.col("x") > 5)')
print("SQL    : SELECT * FROM df_cubed WHERE x > 5")
df_filtered = df_cubed.filter(F.col("x") > 5)             # keep rows where the predicate is true
df_filtered.show()


print("\n>>> Step 5: Count rows in the filtered DataFrame")
print("PySpark: df_filtered.count()")
print("SQL    : SELECT COUNT(*) FROM df_filtered")
n = df_filtered.count()                                    # count: action — forces a full pass through the data
print(f"Filtered row count: {n}")

print("\nSmoke test passed.")
spark.stop()
