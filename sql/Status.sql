-- Status table
CREATE TABLE IF NOT EXISTS `status` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create index for name lookups
CREATE INDEX `idx_status_name` ON `status` (`name`);
