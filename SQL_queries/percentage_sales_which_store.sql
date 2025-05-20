SELECT
    dim_store_details.store_type,
    SUM(orders_table.product_quantity * dim_products.product_price) AS total_sales,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS "sales_made(%)"
FROM
    orders_table
JOIN
    dim_store_details ON orders_table.store_code = dim_store_details.store_code
JOIN
    dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY
    dim_store_details.store_type
ORDER BY
    total_sales DESC;