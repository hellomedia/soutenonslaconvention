-- :result :1
SELECT id, created_at, name, state, logo, website, org_type,
sector, size, scope, theme::text[], contact_name, contact_email, contact_phone,
contact_role
FROM organisations
WHERE id=:id
