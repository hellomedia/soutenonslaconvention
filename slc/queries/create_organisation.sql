-- :result :one
--
INSERT INTO organisations (
    contact_email,
    contact_name,
    contact_phone,
    image_path,
    website,
    name,
    sector,
    org_type,
    size
) VALUES (
    :contact_email,
    :contact_name,
    :contact_phone,
    :name,
    :website,
    :image_path,
    :sector,
    :org_type,
    :size
)
RETURNING id;
