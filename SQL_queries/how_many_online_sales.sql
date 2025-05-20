SELECT
    COUNT(*) AS number_of_sales,
    SUM(orders_table.product_quantity) AS product_quantity_count,
    CASE
        WHEN dim_store_details.store_type = 'Online' THEN 'Online'
        ELSE 'Offline'
    END AS store_category
FROM
    orders_table
LEFT JOIN
    dim_store_details ON orders_table.store_code = dim_store_details.store_code
GROUP BY 
    store_category;