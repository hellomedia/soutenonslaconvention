-- Create initial schema
-- depends: 


CREATE TABLE supporters (
    id SERIAL,
    email TEXT UNIQUE,
    social_provider TEXT,
    social_id TEXT UNIQUE,
    picture_url TEXT,
    full_name TEXT,
    first_name TEXT,
    last_name TEXT,
    locale TEXT,
    account_confirmed BOOL NOT NULL DEFAULT false,
    PRIMARY KEY(id)
);
