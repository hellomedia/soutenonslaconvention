-- Create initial schema
-- depends: 


CREATE OR REPLACE TABLE supporters (
    id SERIAL,
    email TEXT UNIQUE,
    social_username TEXT UNIQUE,
    picture_url TEXT,
    first_name TEXT,
    last_name TEXT,
    account_confirmed BOOL NOT NULL DEFAULT false,
    PRIMARY KEY(id)
);
