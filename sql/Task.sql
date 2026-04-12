-- Task table
CREATE TABLE IF NOT EXISTS `task` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(255) NOT NULL,
    `description` LONGTEXT,
    `priority_id` INT NOT NULL,
    `status_id` INT NOT NULL,
    `start_date` DATETIME,
    `due_date` DATETIME,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign keys
    CONSTRAINT `fk_task_priority_id` FOREIGN KEY (`priority_id`) REFERENCES `priority` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_task_status_id` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create indexes for common queries
CREATE INDEX `idx_task_priority_id` ON `task` (`priority_id`);
CREATE INDEX `idx_task_status_id` ON `task` (`status_id`);
CREATE INDEX `idx_task_due_date` ON `task` (`due_date`);
