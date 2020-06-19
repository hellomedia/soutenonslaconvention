UPDATE supporters
SET 
    display_name = COALESCE(:display_name, display_name),
    reason = COALESCE(:reason, reason),
    suggestion = COALESCE(:suggestion, suggestion),
    image_path = COALESCE(:image_path, image_path)
WHERE id = :id
