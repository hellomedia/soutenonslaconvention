-- :result :*
SELECT
    created_at, id, contact_name, contact_email, contact_phone, name, website,
    image_path, size, state, sector, org_type
FROM organisations
ORDER BY created_at DESC
LIMIT :limit
OFFSET :offset
