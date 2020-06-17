-- :scalar
--
INSERT INTO supporters (
    email,
    social_provider,
    social_id,
    picture_url,
    full_name,
    first_name,
    last_name,
    account_confirmed
) VALUES (
    :email,
    :provider,
    :social_id,
    :picture_url,
    :full_name,
    :first_name,
    :last_name,
    :account_confirmed)
ON CONFLICT DO NOTHING
RETURNING id;
