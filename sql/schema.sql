-- Combined schema script - execute all table creates in order
-- Run these individually or as a batch to set up the complete database schema

-- Priority and Status first (no dependencies)
CREATE TABLE IF NOT EXISTS `priority` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `status` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- User table (no dependencies)
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(120) NOT NULL,
    `email` VARCHAR(120) NOT NULL UNIQUE,
    `password_hash` VARCHAR(200) NOT NULL,
    `role` VARCHAR(50) DEFAULT 'user',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Task table (depends on Priority and Status)
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
    
    CONSTRAINT `fk_task_priority_id` FOREIGN KEY (`priority_id`) REFERENCES `priority` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_task_status_id` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Association table for many-to-many (depends on User and Task)
CREATE TABLE IF NOT EXISTS `users_tasks` (
    `user_id` INT NOT NULL,
    `task_id` INT NOT NULL,
    
    PRIMARY KEY (`user_id`, `task_id`),
    CONSTRAINT `fk_users_tasks_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_users_tasks_task_id` FOREIGN KEY (`task_id`) REFERENCES `task` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Comment table (depends on User and Task)
CREATE TABLE IF NOT EXISTS `comment` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `content` LONGTEXT NOT NULL,
    `user_id` INT NOT NULL,
    `task_id` INT NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT `fk_comment_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_comment_task_id` FOREIGN KEY (`task_id`) REFERENCES `task` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Todo table (depends on User and Task)
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
    
    CONSTRAINT `fk_todo_worked_by` FOREIGN KEY (`worked_by`) REFERENCES `user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT `fk_todo_task_id` FOREIGN KEY (`task_id`) REFERENCES `task` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create indexes
CREATE INDEX `idx_user_email` ON `user` (`email`);
CREATE INDEX `idx_priority_name` ON `priority` (`name`);
CREATE INDEX `idx_status_name` ON `status` (`name`);
CREATE INDEX `idx_task_priority_id` ON `task` (`priority_id`);
CREATE INDEX `idx_task_status_id` ON `task` (`status_id`);
CREATE INDEX `idx_task_due_date` ON `task` (`due_date`);
CREATE INDEX `idx_users_tasks_task_id` ON `users_tasks` (`task_id`);
CREATE INDEX `idx_comment_user_id` ON `comment` (`user_id`);
CREATE INDEX `idx_comment_task_id` ON `comment` (`task_id`);
CREATE INDEX `idx_comment_created_at` ON `comment` (`created_at`);
CREATE INDEX `idx_todo_task_id` ON `todo` (`task_id`);
CREATE INDEX `idx_todo_worked_by` ON `todo` (`worked_by`);
CREATE INDEX `idx_todo_completed` ON `todo` (`completed`);
