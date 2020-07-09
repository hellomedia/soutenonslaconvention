-- :result :*
SELECT
    created_at, id, social_id, display_name, email, account_confirmed, picture_url, image_path, full_name, reason, suggestion, display_image, year_of_birth, occupation_id, signed_mesopinions_petition
FROM supporters
ORDER BY created_at DESC
LIMIT :limit
OFFSET :offset
