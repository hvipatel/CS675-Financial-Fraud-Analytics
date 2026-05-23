"""Word-count on Shakespeare's complete works — the classic MapReduce demo.

The original MapReduce paper used word-count as its illustrating example: Map
emits (word, 1) for every word in the input; Reduce sums by key. Spark does the
same thing with `explode` + `groupBy` + `count`, but it lets us stay in the
DataFrame API instead of writing Mapper / Reducer classes.

Try this with the taxi Parquet's column names if you want to see how this
generalizes beyond text.
"""
import time

from pyspark.sql import functions as F

from constants import SHAKESPEARE_TXT
from spark_helper import get_spark, print_ui_urls, require_files


def main() -> None:
    require_files((SHAKESPEARE_TXT, "make download-shakespeare-data"))
    spark = get_spark("cs675-word-count")
    start = time.time()

    # Read the text file: one row per line, single column called "value".
    lines = spark.read.text(SHAKESPEARE_TXT)
    print(f"Lines: {lines.count():,}")

    words = (
        lines
        .select(F.lower(F.col("value")).alias("line"))            # normalize case
        .select(F.split("line", r"[^a-z']+").alias("tokens"))    # split on non-letters → array<string>
        .select(F.explode("tokens").alias("word"))                # one row per word (Map step)
        .filter(F.length("word") > 0)                             # drop empty strings from split artifacts
    )

    print(f"Total words (with repeats): {words.count():,}")

    # GroupBy + count is the Reduce step: sum (word, 1) tuples by key.
    counts = (
        words.groupBy("word").count()                             # aggregate per word
        .orderBy(F.col("count").desc())                           # most frequent first
    )

    print("\n--- Top 20 most-frequent words (no stopword removal) ---")
    counts.limit(20).show(truncate=False)                         # action: prints to stdout

    # The top of this list is dominated by stopwords (the, and, of, ...).
    # Filter them out to see the more interesting tail.
    STOPWORDS = {
        "the", "and", "of", "to", "a", "i", "my", "in", "you", "is", "that",
        "not", "with", "this", "his", "for", "but", "me", "be", "he", "your",
        "it", "as", "thou", "so", "him", "have", "her", "will", "what", "all",
        "thy", "are", "by", "we", "no", "do", "shall", "if", "thee", "on",
        "from", "or", "our", "they", "their", "she", "would", "she", "lord",
        "now", "more", "good", "us", "come", "let", "was", "an", "at", "had",
        "than", "may", "well", "yet", "go", "love", "did", "should", "make",
        "one", "know", "out", "like", "his", "up", "am", "o", "hath", "must",
        "doth",
    }
    interesting = counts.filter(~F.col("word").isin(list(STOPWORDS)))

    print("\n--- Top 20 after dropping common English stopwords ---")
    interesting.limit(20).show(truncate=False)                    # action

    print(f"\nDone in {time.time() - start:.2f}s.")
    print_ui_urls()
    spark.stop()


if __name__ == "__main__":
    main()
