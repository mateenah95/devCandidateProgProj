CREATE TABLE rates(
        id SERIAL PRIMARY KEY,
        address_line1 VARCHAR NOT NULL,
        address_line2 VARCHAR,
        city VARCHAR NOT NULL,
        state VARCHAR,
        zip INTEGER NOT NULL,
        country VARCHAR NOT NULL, 
        height DECIMAL NOT NULL,
        length DECIMAL NOT NULL,
        width DECIMAL NOT NULL,
        weight DECIMAL NOT NULL,
        cali_carrier VARCHAR NOT NULL,
        cali_service VARCHAR NOT NULL,
        cali_postage_fee MONEY NOT NULL,
        ohio_carrier VARCHAR NOT NULL,
        ohio_service VARCHAR NOT NULL,
        ohio_postage_fee MONEY NOT NULL           
    )