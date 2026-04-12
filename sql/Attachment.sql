CREATE TABLE IF NOT EXISTS `attachment` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `text` LONGTEXT NOT NULL,
    `created_by` INT NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT `fk_attachment_created_by`
        FOREIGN KEY (`created_by`)
        REFERENCES `user` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
