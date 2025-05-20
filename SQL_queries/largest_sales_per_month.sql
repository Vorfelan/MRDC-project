SELECT
    SUM(orders_table.product_quantity * dim_products.product_price) total_sales,
    dim_date_times.month
FROM
    orders_table
LEFT JOIN
    dim_products ON orders_table.product_code = dim_products.product_code
LEFT JOIN
    dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
GROUP BY
    dim_date_times.month
ORDER BY
    total_sales DESC;