-- :result :one
--
INSERT INTO organisations (
    contact_name,
    contact_role,
    contact_email,
    contact_phone,
    name,
    website,
    logo,
    sector,
    org_type,
    size,
    scope,
    theme
) VALUES (
    :contact_name,
    :contact_role,
    :contact_email,
    :contact_phone,
    :name,
    :website,
    :logo,
    :sector,
    :org_type,
    :size,
    :scope,
    :theme::organisation_theme[]
)
RETURNING id;
