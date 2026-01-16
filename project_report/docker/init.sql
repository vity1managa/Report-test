-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample users
INSERT INTO users (username, email, full_name) VALUES 
('john_doe', 'john@example.com', 'John Doe'),
('jane_smith', 'jane@example.com', 'Jane Smith'),
('bob_wilson', 'bob@example.com', 'Bob Wilson'),
('alice_brown', 'alice@example.com', 'Alice Brown')
ON CONFLICT DO NOTHING;

-- Insert sample tasks
INSERT INTO tasks (user_id, title, description, status) VALUES 
(1, 'Complete project documentation', 'Write comprehensive docs for the project', 'completed'),
(1, 'Review code changes', 'Review PR #123', 'in_progress'),
(2, 'Update user interface', 'Redesign login page', 'pending'),
(2, 'Fix bug in payment module', 'Resolve issue with payment processing', 'in_progress'),
(3, 'Prepare monthly report', 'Compile sales data for reporting', 'completed'),
(4, 'Conduct user interviews', 'Gather feedback from beta users', 'pending');