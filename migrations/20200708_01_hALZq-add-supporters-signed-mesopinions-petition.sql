-- Add supporters.signed_mesopinions_petition
-- depends: 20200629_01_geQ3v-add-supporters-age-and-occupation

ALTER TABLE supporters ADD signed_mesopinions_petition BOOL NOT NULL DEFAULT false;
