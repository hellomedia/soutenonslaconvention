-- Add supporter columns
-- depends: 20200617_01_bkBbe-create-initial-schema

ALTER TABLE supporters 
ADD COLUMN display_name TEXT,
ADD COLUMN reason TEXT,
ADD COLUMN image_path TEXT,
ADD COLUMN suggestion TEXT
;
