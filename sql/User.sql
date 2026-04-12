-- User table
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(120) NOT NULL,
    `email` VARCHAR(120) NOT NULL UNIQUE,
    `password_hash` VARCHAR(200) NOT NULL,
    `role` VARCHAR(50) DEFAULT 'user',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create index for email lookups
CREATE INDEX `idx_user_email` ON `user` (`email`);
