# CS-675 — Big Data Management

Course materials for CS-675 (Big Data Management).

## What's here

- **`Lecture 1/`** — week 1 slides and notes. Future weeks: `week_02/`, `week_03/`, …
- **`hadoop-yarn-cluster/`** — runnable HDFS + Spark stack used for labs and assignments.
- **`docker-essentials/`** — quick Docker tutorial (prerequisite for the lab stack).
- **`git-essentials/`** — quick Git tutorial.

## Running the lab stack

From `hadoop-yarn-cluster/`:

```bash
make up        # start HDFS + Spark (5 containers)
make hello     # quick PySpark smoke test
make down      # stop everything (keeps your HDFS data)
```

Windows users: replace `make` with `.\make.ps1`. Full details are in `hadoop-yarn-cluster/README.md`.

## Questions

Bring them to office hours or post on the course site.
