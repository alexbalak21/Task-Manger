-- Comment table
CREATE TABLE IF NOT EXISTS `comment` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `content` LONGTEXT NOT NULL,
    `user_id` INT NOT NULL,
    `task_id` INT NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign keys
    CONSTRAINT `fk_comment_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_comment_task_id` FOREIGN KEY (`task_id`) REFERENCES `task` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create indexes for common queries
CREATE INDEX `idx_comment_user_id` ON `comment` (`user_id`);
CREATE INDEX `idx_comment_task_id` ON `comment` (`task_id`);
CREATE INDEX `idx_comment_created_at` ON `comment` (`created_at`);
