-- Association table for many-to-many relationship between User and Task
CREATE TABLE IF NOT EXISTS `users_tasks` (
    `user_id` INT NOT NULL,
    `task_id` INT NOT NULL,
    
    -- Composite primary key
    PRIMARY KEY (`user_id`, `task_id`),
    
    -- Foreign keys
    CONSTRAINT `fk_users_tasks_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_users_tasks_task_id` FOREIGN KEY (`task_id`) REFERENCES `task` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create indexes for reverse lookups
CREATE INDEX `idx_users_tasks_task_id` ON `users_tasks` (`task_id`);
