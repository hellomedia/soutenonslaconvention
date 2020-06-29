UPDATE supporters
SET 
    display_name = COALESCE(:display_name, display_name),
    reason = COALESCE(:reason, reason),
    suggestion = COALESCE(:suggestion, suggestion),
    image_path = COALESCE(:image_path, image_path),
    display_image = COALESCE(:display_image, display_image),
    occupation_id = COALESCE(:occupation_id, occupation_id),
    year_of_birth = COALESCE(:year_of_birth, year_of_birth)
WHERE id = :id
