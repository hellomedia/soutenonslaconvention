-- Add supporters age and occupation
-- depends: 20200619_02_ltXhw-add-display-image-column
CREATE TABLE occupations (
    id SERIAL,
    name TEXT NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

INSERT INTO occupations (name) 
VALUES 
    ('Artisan - Commerçant - Chef d''entreprise'),
    ('Agriculteur'),
    ('Cadre supérieur - Profession libérale'),
    ('Profession intermédiaire'),
    ('Employé'),
    ('Ouvrier'),
    ('Retraité'),
    ('Inactif'),
    ('Etudiant');


ALTER TABLE supporters ADD occupation_id INT;
ALTER TABLE supporters ADD year_of_birth int4range;
ALTER TABLE supporters ADD CONSTRAINT supporters_occupation_id_fkey FOREIGN KEY (occupation_id) REFERENCES occupations (id);
