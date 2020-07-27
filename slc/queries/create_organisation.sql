-- :result :one
--
INSERT INTO organisations (
    contact_email,
    contact_name,
    contact_phone,
    contact_role,
    image_path,
    website,
    name,
    sector,
    org_type,
    size,
    scope,
    theme
) VALUES (
    :contact_email,
    :contact_name,
    :contact_phone,
    :contact_role,
    :name,
    :website,
    :image_path,
    :sector,
    :org_type,
    :size,
    :scope,
    :theme
)
RETURNING id;
