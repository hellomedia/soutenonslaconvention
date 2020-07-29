-- create organisation table
-- depends: 20200708_01_hALZq-add-supporters-signed-mesopinions-petition
CREATE TYPE organisation_size AS ENUM ('S', 'M', 'L');
CREATE TYPE organisation_state AS ENUM ('PENDING', 'CONFIRMED', 'CANCELLED');
CREATE TYPE organisation_type AS ENUM (
    'Entreprise', 'Association', 'Collectivité territoriale', 'ONG', 'Autre'
);
CREATE TYPE organisation_sector AS ENUM (
    'Agriculture et agroalimentaire', 'Industrie', 'Energie',
    'Commerce et artisanat', 'Santé', 'Education', 'Tourisme',
    'Télécom et internet', 'Hôtellerie restauration', 'Recherche',
    'Finance et Assurances', 'Autre'
);
CREATE TYPE organisation_scope AS ENUM (
    'Locale', 'Régionale', 'Nationale', 'Internationale'
);
CREATE TYPE organisation_theme AS ENUM (
    'Se déplacer', 'Consommer', 'Se loger', 'Produire/Travailler', 'Se nourrir'
);

CREATE TABLE organisations (
    id SERIAL,
    contact_email TEXT,
    contact_name TEXT,
    contact_phone TEXT,
    contact_role TEXT,
    name TEXT,
    website TEXT,
    logo TEXT,
    size organisation_size,
    state organisation_state DEFAULT 'PENDING',
    theme organisation_theme[],
    org_type organisation_type,
    sector organisation_sector,
    scope organisation_scope,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY(id)
);
