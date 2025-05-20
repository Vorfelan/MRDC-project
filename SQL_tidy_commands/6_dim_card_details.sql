ALTER TABLE dim_card_details
    ALTER COLUMN card_number TYPE VARCHAR(19),
    ALTER COLUMN expiry_date TYPE VARCHAR(10) USING TO_CHAR(expiry_date, 'YYYY-MM-DD'),
    ALTER COLUMN date_payment_confirmed TYPE DATE;