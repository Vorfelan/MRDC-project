SELECT
    ROUND(SUM(orders_table.product_quantity * dim_products.product_price), 2) AS total_sales,
    dim_date_times.year,
    dim_date_times.month
FROM
    orders_table
JOIN
    dim_products ON orders_table.product_code = dim_products.product_code
JOIN
    dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
GROUP BY
    year, month
ORDER BY
    total_sales DESC
LIMIT 10;