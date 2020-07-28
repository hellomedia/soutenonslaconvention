-- :result :*
SELECT
    created_at, id, contact_name, contact_email, contact_phone, contact_role,
    name, website, logo, state, size, sector, org_type, scope, theme
FROM organisations
ORDER BY created_at DESC
LIMIT :limit
OFFSET :offset
