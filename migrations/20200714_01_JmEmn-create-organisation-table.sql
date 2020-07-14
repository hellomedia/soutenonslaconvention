-- create organisation table
-- depends: 20200708_01_hALZq-add-supporters-signed-mesopinions-petition
CREATE TYPE organisation_size AS ENUM ('S', 'M', 'L');
CREATE TYPE organisation_state AS ENUM ('PENDING', 'CONFIRMED', 'CANCELLED');
CREATE TYPE organisation_type AS ENUM ('ENTREPRISE', 'ASSOCIATION', 'AUTRE');
CREATE TYPE organisation_sector AS ENUM ('SECTEUR 1', 'SECTEUR 2', 'AUTRE');

CREATE TABLE organisations (
    id SERIAL,
    contact_email TEXT,
    contact_name TEXT,
    contact_phone TEXT,
    name TEXT,
    website TEXT,
    image_path TEXT,
    size organisation_size,
    state organisation_state,
    org_type organisation_type,
    sector organisation_sector,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY(id)
);
