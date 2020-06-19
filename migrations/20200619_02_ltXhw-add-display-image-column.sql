-- Add display_image column
-- depends: 20200619_01_Em0mm-add-supporter-columns
ALTER TABLE supporters ADD display_image TEXT, ADD created_at TIMESTAMP DEFAULT NOW();
