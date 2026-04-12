CREATE TABLE IF NOT EXISTS `task_attachments` (
    `task_id` INT NOT NULL,
    `attachment_id` INT NOT NULL,

    PRIMARY KEY (`task_id`, `attachment_id`),

    CONSTRAINT `fk_task_attachments_task_id`
        FOREIGN KEY (`task_id`)
        REFERENCES `task` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT `fk_task_attachments_attachment_id`
        FOREIGN KEY (`attachment_id`)
        REFERENCES `attachment` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
