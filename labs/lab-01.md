# Lab 1 — Run your first PySpark analysis

By the end of this lab you'll have the course's Spark playground running on your laptop, you'll have analyzed about 3 million real NYC yellow-taxi trips, and you'll have seen your run land in a real Spark History Server. None of this is busy-work — every piece comes back as we move through the semester.

**Anchors on:** Lecture 4 (HDFS, MapReduce, Spark intro).

---

## Setup checklist

If you've already done this, skip ahead.

1. Install Docker Desktop on your laptop. See [`code-starter/README-docker.md`](../code-starter/README-docker.md) → *Step 0* for per-platform instructions (macOS, Windows, Linux).
2. Clone the course repo or pull the latest if you already have it.
3. From the `code-starter/` directory, run `make up`. Wait for the image to download (~1.5 GB, one-time).
4. Open <http://localhost:8888> in your browser. Token is `cs675`. You should see Jupyter Lab.

If any of the four above didn't work, post in the course channel — don't try to debug it alone.

---

## Part A — Guided walkthrough

Work through these five steps in order. Each one ends with a concrete thing you should see — if you don't, post in the course channel before moving on.

> All commands assume your terminal is in the `code-starter/` directory. On Windows PowerShell, replace `make` with `.\make.ps1` (the targets are identical).

### Step 1 — Confirm the lab is running

```
make up
```

**You should see**: three URLs printed at the end — Jupyter (`:8888`), Live Spark UI (`:4040`), History Server (`:18080`).

### Step 2 — Smoke test

```
make hello
```

**You should see**: a few lines about PySpark version + a tiny DataFrame with `x` and `x_squared` columns, ending in `Smoke test passed.` If you see this, your Spark setup is healthy.

### Step 3 — Download the taxi data

```
make download-nyc-cab-data
```

**You should see**: a progress bar pulling about 48 MB from `d37ci6vzurychx.cloudfront.net`, finishing in a few seconds, then `Saved: /home/jovyan/work/data/yellow_tripdata_2024-01.parquet`. This is real data: every yellow-taxi trip in NYC in January 2024 (~3 million rides).

### Step 4 — Run the first analysis

```
make analyze-nyc-cab-data-use-case-a
```

**You should see**: three tables printed — top 5 pickup hours, average fare by passenger count, top 10 longest trips. The "longest trip" is going to look ridiculous. That's not a bug.

### Step 5 — Find your run in the History Server

Open <http://localhost:18080> in your browser. You should see a row for `cs675-taxi-analysis` from a few seconds ago. **Click into it.** You'll land on a page showing the run's *jobs*, with sub-tabs for *Stages*, *SQL / DataFrame*, *Executors*. You'll come back to this view many times this semester — this is where Spark shows you what actually happened.

---

## Part B — Questions to answer (scaffold tier)

Everyone does these four.

### B1. The peak pickup hour
What was the busiest pickup hour from Step 4's output? Roughly what fraction of all trips happened in that hour? Why does that hour-of-day make sense given what New York is like? (30–50 words. 2 pts.)

### B2. The 312,000-mile trip
Look at the "Top 10 longest trips by distance" table. The top entry will read something like `312,722.0` miles. In your own words, what's probably going on — and what does this tell us about the dataset we're about to spend the semester working with? (30–50 words. 2 pts.)

### B3. The Spark UI is real
Open <http://localhost:18080>, click into your `cs675-taxi-analysis` run, click the **SQL / DataFrame** tab. Screenshot the page. You don't need to interpret it yet; reading the Spark UI comes later in the course. (2 pts.)

### B4. Make it your own
Open `code-starter/work/01_taxi_analysis.py` in Jupyter Lab. Find the line `.limit(5)` in the *Top 5 pickup hours* block. Change `5` to `10`. Save. Run `make analyze-nyc-cab-data-use-case-a` again. Screenshot the new output table, and screenshot the History Server now showing **two** completed runs side by side. (4 pts.)

---

## Part C — Stretch goal (extension tier, optional)

Open-ended. Worth 2 pts of extra credit if attempted and reasonable. Cap your write-up at 100 words per part.

### C1. Top 10 longest trips by duration
The script ranks longest trips by `trip_distance`. Modify it to rank by trip *duration* instead — compute `(tpep_dropoff_datetime - tpep_pickup_datetime)` and sort by that descending. Submit your modified code and the new output. One sentence: how does this top-10 differ from the distance-based one?

### C2. Tip percentage
Add a derived column `tip_pct = tip_amount / fare_amount * 100`. Print the mean tip percentage across the whole dataset, filtered to trips where `fare_amount > 0`. Submit your code and the printed value. One sentence: do you trust this number? Why or why not?

---

## How to submit

A single Google Doc or Google Slides link with public read access, containing:

- One section per question (B1, B2, B3, B4, and C1/C2 if attempted).
- Screenshots for B3 and B4 (and C1/C2 if applicable).
- Prose answers within the stated word limits.

**Not accepted:** raw markdown files, mermaid diagrams, AI-generated diagrams. Screenshots must come from *your* History Server (`localhost:18080`) — runs from someone else's machine won't match the timestamps and app IDs.

Submit the link via Blackboard by the lab's due date listed in the course schedule.

---

## AI policy

AI assistants are **allowed** to help you understand concepts, look up Python or Spark syntax, or explain an error message. They are **not allowed** to write your answers or your modified code for you.

The questions in this lab require a specific thing to appear in *your* Spark History Server, with *your* timestamp. A screenshot from an AI-generated mockup is recognizable next to a real one. Use AI to learn; do the lab with your own brain and your own running stack.

Using AI for learning is good practice — just don't paste your prompt as your answer. AI-detection tools will run on submissions; flagged work may be graded as 0.
