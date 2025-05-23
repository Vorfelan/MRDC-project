ALTER TABLE dim_date_times
    ADD PRIMARY KEY (date_uuid);

ALTER TABLE dim_users
    ADD PRIMARY KEY (user_uuid);

ALTER TABLE dim_card_details
    ADD PRIMARY KEY (card_number_id);

ALTER TABLE dim_store_details
    ADD PRIMARY KEY (store_code);

ALTER TABLE dim_products
    ADD PRIMARY KEY (product_code);

ALTER TABLE orders_table
    ADD CONSTRAINT fk_date_uuid
    FOREIGN KEY (date_uuid) REFERENCES dim_date_times (date_uuid);

ALTER TABLE orders_table
    ADD CONSTRAINT fk_user_uuid
    FOREIGN KEY (user_uuid) REFERENCES dim_users (user_uuid);

DELETE FROM orders_table
WHERE card_number_id NOT IN (
    SELECT card_number_id FROM dim_card_details);

ALTER TABLE orders_table
    ADD CONSTRAINT fk_card_number
    FOREIGN KEY (card_number_id) REFERENCES dim_card_details (card_number_id);

INSERT INTO dim_store_details (store_code, store_type)
VALUES ('WEB-1388012W', 'Online');

DELETE FROM orders_table
WHERE store_code NOT IN (
    SELECT store_code FROM dim_store_details);

ALTER TABLE orders_table
    ADD CONSTRAINT fk_store_code
    FOREIGN KEY (store_code) REFERENCES dim_store_details (store_code);

ALTER TABLE orders_table
    ADD CONSTRAINT fk_product_code
    FOREIGN KEY (product_code) REFERENCES dim_products (product_code);
