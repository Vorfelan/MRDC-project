SELECT 
    country_code as country,
    COUNT(*) AS total_no_stores
FROM
    dim_store_details
GROUP BY
    country_code
ORDER BY
    total_no_stores DESC;