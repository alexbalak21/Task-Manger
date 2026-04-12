-- User profile image table
CREATE TABLE IF NOT EXISTS `user_profile_images` (
    `user_id` INT PRIMARY KEY,
    `blob` MEDIUMBLOB NOT NULL,
    CONSTRAINT `fk_user_profile_images_user`
        FOREIGN KEY (`user_id`) REFERENCES `user`(`id`)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
