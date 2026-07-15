-- Sample Athena query. This is the "easiest working version" to start from -
-- get it running, then use AI to extend it step by step.
--
-- Step 1 (run once): define a table over a dataset. Replace <DATASET_S3_LOCATION>
-- with an instructor-shared dataset or your own data uploaded to this bucket.
-- Adjust the columns/format to match your dataset.
--
-- CREATE EXTERNAL TABLE IF NOT EXISTS trips (
--   payment_type   int,
--   fare_amount    double,
--   trip_distance  double,
--   passenger_count int
-- )
-- STORED AS PARQUET
-- LOCATION 's3://<DATASET_S3_LOCATION>/';

-- Step 2: query it. (This simple aggregation is the starting point; grow it.)
SELECT payment_type,
       count(*)            AS trips,
       round(avg(fare_amount), 2) AS avg_fare
FROM trips
GROUP BY payment_type
ORDER BY trips DESC;
