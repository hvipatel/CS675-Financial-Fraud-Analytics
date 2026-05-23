"""Step-by-step word count on Shakespeare's complete works — the classic MapReduce demo.

Walk through every transformation in turn so you can see how the data changes:
   raw lines  →  lowercased  →  tokenized  →  exploded  →  counted  →  sorted

Each step shows 5 rows of the intermediate result. The shape of the table
literally changes between steps (one row per line → one row per word).

If you know SQL, the SQL equivalent is shown alongside each PySpark call.

The original MapReduce paper used word-count as its illustrating example:
Map emits (word, 1) for every word in the input; Reduce sums by key.
Spark does the same thing in the DataFrame API: `explode` is the Map, and
`groupBy + count` is the Reduce.
"""
import time

from pyspark.sql import functions as F

from constants import SHAKESPEARE_TXT
from spark_helper import get_spark, print_ui_urls, require_files


def main() -> None:
    require_files((SHAKESPEARE_TXT, "make download-shakespeare-data"))
    spark = get_spark("cs675-word-count")
    start = time.time()

    print(">>> Step 1: Read the text file — one row per line, single column 'value'")
    print("PySpark: spark.read.text(SHAKESPEARE_TXT)")
    print("SQL    : SELECT * FROM read_text('shakespeare.txt')   -- (e.g. DuckDB)")
    lines = spark.read.text(SHAKESPEARE_TXT)              # one row per line of the file
    print(f"Total lines: {lines.count():,}")
    lines.show(5, truncate=False)

    print("\n>>> Step 2: Lowercase each line — F.lower()")
    print("PySpark: lines.select(F.lower('value').alias('line'))")
    print("SQL    : SELECT LOWER(value) AS line FROM lines")
    lowered = lines.select(F.lower(F.col("value")).alias("line"))    # case-fold so 'The' and 'the' match later
    lowered.show(5, truncate=False)

    print("\n>>> Step 3: Split each line into an array of tokens — F.split()")
    print(r"PySpark: lowered.select(F.split('line', r\"[^a-z']+\").alias('tokens'))")
    print(r"SQL    : SELECT REGEXP_SPLIT_TO_ARRAY(line, '[^a-z'']+') AS tokens FROM lowered")
    tokenized = lowered.select(F.split("line", r"[^a-z']+").alias("tokens"))  # produces array<string>
    tokenized.show(5, truncate=False)
    print("(Each row's 'tokens' column is now an *array* of words.)")

    print("\n>>> Step 4: Explode the array — one row per word (the Map step)")
    print("PySpark: tokenized.select(F.explode('tokens').alias('word'))")
    print("SQL    : SELECT UNNEST(tokens) AS word FROM tokenized   -- (Postgres / DuckDB)")
    print("         SELECT word FROM tokenized LATERAL VIEW EXPLODE(tokens) t AS word   -- (Hive)")
    words = tokenized.select(F.explode("tokens").alias("word"))     # explode: array column → many rows
    print(f"Total word tokens: {words.count():,}")
    words.show(5, truncate=False)
    print("(Shape changed: was N rows of arrays, now sum-of-array-lengths rows of single words.)")

    print("\n>>> Step 5: Drop empty strings (artifacts from splitting on punctuation)")
    print("PySpark: words.filter(F.length('word') > 0)")
    print("SQL    : SELECT * FROM words WHERE LENGTH(word) > 0")
    words_clean = words.filter(F.length("word") > 0)                # punctuation-only "splits" leave empty strings
    print(f"After cleanup: {words_clean.count():,} words")

    print("\n>>> Step 6: Group by word, count occurrences — the Reduce step")
    print("PySpark: words_clean.groupBy('word').count()")
    print("SQL    : SELECT word, COUNT(*) AS count FROM words_clean GROUP BY word")
    counts = words_clean.groupBy("word").count()                     # sum the (word, 1) tuples by key
    counts.show(5, truncate=False)
    print("(Order is non-deterministic until we sort.)")

    print("\n>>> Step 7: Sort by count descending, take the top 20")
    print("PySpark: counts.orderBy(F.col('count').desc()).limit(20)")
    print("SQL    : SELECT word, count FROM counts ORDER BY count DESC LIMIT 20")
    top20 = counts.orderBy(F.col("count").desc()).limit(20)         # sort then truncate
    top20.show(truncate=False)

    print("\n>>> Step 8: Same query, but drop common English stopwords first")
    STOPWORDS = {
        "the", "and", "of", "to", "a", "i", "my", "in", "you", "is", "that",
        "not", "with", "this", "his", "for", "but", "me", "be", "he", "your",
        "it", "as", "thou", "so", "him", "have", "her", "will", "what", "all",
        "thy", "are", "by", "we", "no", "do", "shall", "if", "thee", "on",
        "from", "or", "our", "they", "their", "she", "would", "lord",
        "now", "more", "good", "us", "come", "let", "was", "an", "at", "had",
        "than", "may", "well", "yet", "go", "love", "did", "should", "make",
        "one", "know", "out", "like", "up", "am", "o", "hath", "must", "doth",
    }
    print("PySpark: counts.filter(~F.col('word').isin(STOPWORDS)).orderBy(... desc).limit(20)")
    print("SQL    : SELECT word, count FROM counts")
    print("         WHERE word NOT IN ('the', 'and', 'of', …)")
    print("         ORDER BY count DESC LIMIT 20")
    interesting = (
        counts.filter(~F.col("word").isin(list(STOPWORDS)))          # negate isin to drop stopwords
        .orderBy(F.col("count").desc()).limit(20)
    )
    interesting.show(truncate=False)

    print(f"\nDone in {time.time() - start:.2f}s.")
    print_ui_urls()
    spark.stop()


if __name__ == "__main__":
    main()
