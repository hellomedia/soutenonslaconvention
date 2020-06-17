-- :scalar
--
INSERT INTO supporters (email, social_provider, social_id, picture_url, first_name, last_name, account_confirmed)
VALUES (:email, :provider, :social_id, :picture_url, :first_name, :last_name, :account_confirmed)
RETURNING id;
