WITH full_timestamps AS (
    SELECT
        orders_table.index,
        dim_date_times.year,
        MAKE_TIMESTAMP(
            dim_date_times.year::INT,
            dim_date_times.month::INT,
            dim_date_times.day::INT,
            EXTRACT(HOUR FROM dim_date_times.timestamp)::INT,
            EXTRACT(MINUTE FROM dim_date_times.timestamp)::INT,
            EXTRACT(SECOND FROM dim_date_times.timestamp)
        ) AS full_timestamp
    FROM 
        orders_table
    JOIN
        dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
),
time_differences AS (
    SELECT
        year,
        full_timestamp,
        LEAD(full_timestamp) OVER (PARTITION BY year ORDER BY full_timestamp) AS next_timestamp
    FROM
        full_timestamps
),
time_diff_calc AS (
    SELECT
        year,
        next_timestamp - full_timestamp AS diff 
    FROM
        time_differences
    WHERE
        next_timestamp IS NOT NULL
),
avg_diff_by_year AS (
    SELECT
        year,
        AVG(diff) AS average_diff
    FROM
        time_diff_calc
    GROUP BY
        year
)
SELECT 
    year, 
    JUSTIFY_INTERVAL(average_diff) AS actual_time_taken
FROM
    avg_diff_by_year
ORDER BY
    average_diff
LIMIT 10;
