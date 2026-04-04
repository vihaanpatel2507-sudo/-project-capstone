-- 1. Create the database
CREATE DATABASE IF NOT EXISTS college_event;
USE college_event;

-- 2. Create the table with columns matching your index.html fields
CREATE TABLE IF NOT EXISTS registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    student_id VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    department VARCHAR(100),
    year VARCHAR(50),
    event_type VARCHAR(50),
    event_name VARCHAR(100),
    category VARCHAR(50),
    team_size INT DEFAULT 1,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);