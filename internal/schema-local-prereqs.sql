-- Local-only schema prerequisites for the G4br13l source mirror.
-- Review the existing schema first. Run only statements for missing objects.
-- This is NOT an official project migration. Keep for private/local review only.

ALTER TABLE course ADD COLUMN shift_id INT NULL;

CREATE TABLE shift (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    day_of_week INT NULL,
    start_time TIME NULL,
    end_time TIME NULL
);

CREATE TABLE users_courses (
    user_code VARCHAR(10) NOT NULL,
    course_code VARCHAR(25) NOT NULL,
    level VARCHAR(20) NOT NULL,
    is_abandoned TINYINT(1) NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(20) NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by VARCHAR(20) NULL,
    PRIMARY KEY (user_code, course_code, level)
);

ALTER TABLE user
    ADD COLUMN avatar_md VARCHAR(255) NULL,
    ADD COLUMN avatar_lg VARCHAR(255) NULL;
