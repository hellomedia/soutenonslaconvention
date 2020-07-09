UPDATE supporters
SET
    display_name = COALESCE(:display_name, display_name),
    reason = COALESCE(:reason, reason),
    suggestion = COALESCE(:suggestion, suggestion),
    image_path = COALESCE(:image_path, image_path),
    display_image =
        CASE WHEN :photo_option = 'none' THEN
            NULL
        WHEN :photo_option = 'existing' THEN
            image_path
        ELSE
            COALESCE(:image_path, image_path)
        END,
    occupation_id = COALESCE(:occupation_id, occupation_id),
    year_of_birth = COALESCE(:year_of_birth, year_of_birth),
    signed_mesopinions_petition = COALESCE(:signed_mesopinions_petition, signed_mesopinions_petition)
WHERE id = :id
