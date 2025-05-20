UPDATE dim_products
    SET product_price = REPLACE(product_price, '£', '');

ALTER TABLE dim_products
    RENAME COLUMN removed TO availability;

UPDATE dim_products
SET availability = CASE
    WHEN availability = 'Still_available' THEN TRUE
    WHEN availability = 'Removed' THEN FALSE
END;

ALTER TABLE dim_products
    ALTER COLUMN product_name TYPE VARCHAR(255),
    ALTER COLUMN product_price TYPE NUMERIC USING product_price::NUMERIC,
    ALTER COLUMN weight TYPE NUMERIC USING weight::NUMERIC,
    ALTER COLUMN category TYPE VARCHAR(18),
    ALTER COLUMN "EAN" TYPE VARCHAR(17),
    ALTER COLUMN date_added TYPE DATE,
    ALTER COLUMN uuid TYPE UUID USING uuid::UUID,
    ALTER COLUMN product_code TYPE VARCHAR(11),
    ALTER COLUMN availability TYPE BOOLEAN USING availability::BOOLEAN;

ALTER TABLE dim_products
    ADD COLUMN weight_class VARCHAR(20);

UPDATE dim_products
SET weight_class = CASE
    WHEN weight < 2 THEN 'Light'
    WHEN weight >= 2 AND weight < 40 THEN 'Mid_Sized'
    WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
    WHEN weight >= 140 THEN 'Truck_Required'
END;