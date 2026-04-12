-- Todo table (subtasks)
CREATE TABLE IF NOT EXISTS `todo` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `text` VARCHAR(255) NOT NULL,
    `in_progress` BOOLEAN DEFAULT FALSE,
    `completed` BOOLEAN DEFAULT FALSE,
    `worked_by` INT,
    `completed_at` DATETIME,
    `task_id` INT NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign keys
    CONSTRAINT `fk_todo_worked_by` FOREIGN KEY (`worked_by`) REFERENCES `user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT `fk_todo_task_id` FOREIGN KEY (`task_id`) REFERENCES `task` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create indexes for common queries
CREATE INDEX `idx_todo_task_id` ON `todo` (`task_id`);
CREATE INDEX `idx_todo_worked_by` ON `todo` (`worked_by`);
CREATE INDEX `idx_todo_completed` ON `todo` (`completed`);
