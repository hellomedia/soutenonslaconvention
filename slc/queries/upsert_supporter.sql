-- :result :one
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
ON CONFLICT (email) DO UPDATE SET
    email=:email,
    social_provider=:provider,
    social_id=:social_id,
    picture_url=:picture_url,
    full_name=:full_name,
    first_name=:first_name,
    last_name=:last_name,
    account_confirmed=supporters.account_confirmed or :account_confirmed
RETURNING id, created_at=now();
