# CS-675 — Midterm Study Guide

This guide tells you what topics the midterm covers and what the question
types look like.

## What the exam covers (Lectures 1–7)

| #   | Topic                  |
| --- | ---------------------- |
| L1  | Why Big Data           |
| L2  | Hadoop                 |
| L2b | Data Mining            |
| L3  | Data Preparation       |
| L4  | Storage & File Types   |
| L5  | HDFS, YARN, MapReduce  |
| L6  | Spark Foundations      |
| L7  | Code Starter (PySpark labs) |

---

## Question types & examples

The exam mixes five formats. One or two samples of each are below.

### Breakdown (tentative, subject to change)

| Question type                 | # of questions | Points each | Total    |
| ----------------------------- | -------------- | ----------- | -------- |
| Multiple choice (MCQ)         | 50             | 1           | 50       |
| Fill in the blanks            | 50             | 1           | 50       |
| Short answers / explanations  | 20             | 3           | 60       |
| Spark code snippets           | 10             | 4           | 40       |
| Design questions              | 5              | 6           | 30       |
| **Total**                     | **135**        |             | **230**  |

### 1. Multiple choice (MCQ)

> **Q.** In Spark, which of the following is an **action** (triggers execution)?
>
> a) `filter()` &nbsp; b) `select()` &nbsp; c) `count()` &nbsp; d) `withColumn()`
>
> **Answer:** c. `count()` is an action; the rest are transformations that only extend the plan.

> **Q.** Which workload is an RDBMS designed for?
>
> a) OLAP &nbsp; b) OLTP &nbsp; c) Batch ETL &nbsp; d) Iterative ML
>
> **Answer:** b. Short, frequent, consistent (ACID) transactions.

### 2. Fill in the blanks

- HDFS splits every file into fixed-size __________ (default __________ MB),
  and keeps __________ replicas of each by default.
  *(blocks; 128; 3)*
- A stage boundary in Spark is always a __________.
  *(shuffle)*
- The IQR rule flags a value as an outlier if it sits more than
  __________ × IQR below Q1 or above Q3. *(1.5)*

### 3. Short answers / explanations
Explain a concept in 2–4 sentences, in your own words.

> **Q.** Why does Hadoop send the program to the data instead of the data to
> the program? Name the principle and the problem it solves.
>
> **Answer:** The principle is **data locality**: run the computation on the
> node that already holds the data. It solves the problem that moving large data
> across the network is slow and expensive. Since the program is only a few
> kilobytes, it is much cheaper to send the code to the data than the data to the
> code.

> **Q.** In MapReduce, why must a "compute the average" job emit both a sum and a
> count from the mapper, rather than emitting a partial average?
>
> **Answer:** Because averages cannot be combined directly. Averaging a set of
> partial averages gives the wrong result when each one covers a different number
> of records. If the mapper sends the sum and the count, the reducer can add all
> the sums, add all the counts, and divide once at the end to get the correct
> average.

### 4. Spark code snippets
Write a short snippet for a small task, answer an MCQ about a snippet, or fill
in a blanked-out line. **Snippets are drawn directly from the lab code in
`code-starter/work/`**: the same scripts you ran in the labs. Re-run them, read
them line by line, and make sure you can explain every transformation, action,
and aggregation. Expect snippets that are lightly edited or have a line blanked
out.

> **Q.** Given a DataFrame `trips` with columns `trip_distance` and
> `fare_amount`, write the Spark code that keeps only trips longer than 50
> miles and shows the average fare. Which operation triggers execution?

```python
(trips
    .filter(trips.trip_distance > 50)   # transformation (lazy)
    .agg(F.avg("fare_amount"))          # transformation (lazy)
    .show())                            # ACTION: runs the whole chain
```

> **Q.** This is the classic word-count. Fill in the two blanks (the Map step
> and the Reduce step):

```python
words = (lines
    .select(F.split(F.lower("value"), r"[^a-z']+").alias("tokens"))
    .select(F.________("tokens").alias("word")))   # MAP: array -> one row per word
result = words.groupBy("word").________()          # REDUCE: sum 1 per word
```

> **Answer:** `explode` (first blank), `count` (second blank).

### 5. Design questions
Sketch and label a small architecture or process, and explain the key idea in a
sentence or two. Most design questions ask for both a diagram and a short
explanation.

> **Q.** Draw the CRISP-DM lifecycle. Label all six phases and show at least one
> "loop back" arrow that makes it iterative rather than a straight pipeline.

> **Q.** Draw a 2-stage Spark job for `groupBy("payment_type").avg("fare_amount")`.
> Show the partitions, mark where the shuffle happens, and label the stage
> boundary.

**Example answers are intentionally left out for this section.** Draw them in a
proper diagramming tool (draw.io, Google Slides, Excalidraw, etc.), then
attach/include a screenshot of your diagram with your answer.
