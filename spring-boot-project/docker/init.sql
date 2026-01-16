-- Initial database setup script
-- This will be run when the PostgreSQL container starts

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL,
    user_id BIGINT REFERENCES users(id)
);

-- Insert sample users
INSERT INTO users (username, email, first_name, last_name) VALUES
('john_doe', 'john@example.com', 'John', 'Doe'),
('jane_smith', 'jane@example.com', 'Jane', 'Smith'),
('bob_wilson', 'bob@example.com', 'Bob', 'Wilson'),
('alice_brown', 'alice@example.com', 'Alice', 'Brown')
ON CONFLICT (username) DO NOTHING;

-- Insert sample tasks
INSERT INTO tasks (title, description, status, user_id) VALUES
('Complete Project', 'Finish the Spring Boot project', 'PENDING', 1),
('Review Code', 'Review team members'' code', 'IN_PROGRESS', 1),
('Write Documentation', 'Document the API endpoints', 'COMPLETED', 2),
('Fix Bugs', 'Fix reported bugs', 'IN_PROGRESS', 2),
('Update UI', 'Update user interface', 'PENDING', 3),
('Deploy Application', 'Deploy to production server', 'COMPLETED', 4);