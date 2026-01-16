import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import os


class UserDatabaseManager:
    def __init__(self, db_path: str = "/workspace/project_report/users.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with tables and sample data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                full_name TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)
        
        # Insert sample users if they don't exist
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, email, full_name) VALUES 
            ('john_doe', 'john@example.com', 'John Doe'),
            ('jane_smith', 'jane@example.com', 'Jane Smith'),
            ('bob_wilson', 'bob@example.com', 'Bob Wilson'),
            ('alice_brown', 'alice@example.com', 'Alice Brown')
        """)
        
        # Insert sample tasks if they don't exist
        cursor.execute("""
            INSERT OR IGNORE INTO tasks (user_id, title, description, status) VALUES 
            (1, 'Complete project documentation', 'Write comprehensive docs for the project', 'completed'),
            (1, 'Review code changes', 'Review PR #123', 'in_progress'),
            (2, 'Update user interface', 'Redesign login page', 'pending'),
            (2, 'Fix bug in payment module', 'Resolve issue with payment processing', 'in_progress'),
            (3, 'Prepare monthly report', 'Compile sales data for reporting', 'completed'),
            (4, 'Conduct user interviews', 'Gather feedback from beta users', 'pending')
        """)
        
        conn.commit()
        conn.close()
    
    def find_user_by_username(self, username: str) -> Optional[Dict]:
        """Find a user by username"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        user = dict(result) if result else None
        conn.close()
        return user
    
    def get_all_users(self) -> List[Dict]:
        """Get all users from the database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        results = cursor.fetchall()
        
        users = [dict(row) for row in results]
        conn.close()
        return users
    
    def get_user_tasks(self, user_id: int) -> List[Dict]:
        """Get all tasks for a specific user"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        results = cursor.fetchall()
        
        tasks = [dict(row) for row in results]
        conn.close()
        return tasks
    
    def get_all_users_with_tasks(self) -> List[Dict]:
        """Get all users along with their tasks"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT u.*, t.id as task_id, t.title as task_title, 
                   t.description as task_description, t.status as task_status,
                   t.created_at as task_created_at
            FROM users u
            LEFT JOIN tasks t ON u.id = t.user_id
            ORDER BY u.username, t.created_at DESC
        """)
        results = cursor.fetchall()
        
        # Group tasks by user
        users_dict = {}
        for row in results:
            user_id = row['id']
            if user_id not in users_dict:
                users_dict[user_id] = {
                    'id': row['id'],
                    'username': row['username'],
                    'email': row['email'],
                    'full_name': row['full_name'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at'],
                    'tasks': []
                }
            
            # Add task if it exists
            if row['task_id']:
                users_dict[user_id]['tasks'].append({
                    'id': row['task_id'],
                    'title': row['task_title'],
                    'description': row['task_description'],
                    'status': row['task_status'],
                    'created_at': row['task_created_at']
                })
        
        return list(users_dict.values())


def main():
    db_manager = UserDatabaseManager()
    
    print("=== User Management System Report ===")
    print(f"Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Get all users
    all_users = db_manager.get_all_users()
    print(f"Total Users: {len(all_users)}\n")
    
    print("--- User Details ---")
    for user in all_users:
        print(f"ID: {user['id']}")
        print(f"Username: {user['username']}")
        print(f"Email: {user['email']}")
        print(f"Full Name: {user['full_name']}")
        print(f"Created At: {user['created_at']}")
        
        # Get tasks for this user
        tasks = db_manager.get_user_tasks(user['id'])
        print(f"Number of Tasks: {len(tasks)}")
        if tasks:
            print("Tasks:")
            for task in tasks:
                print(f"  - {task['title']} [{task['status']}]")
        print("-" * 40)
    
    # Find a specific user example
    print("\n--- Finding Specific User ---")
    specific_user = db_manager.find_user_by_username('jane_smith')
    if specific_user:
        print(f"Found user: {specific_user['full_name']} ({specific_user['username']})")
        tasks = db_manager.get_user_tasks(specific_user['id'])
        print(f"User has {len(tasks)} tasks:")
        for task in tasks:
            print(f"  - {task['title']}: {task['status']}")
    else:
        print("User not found")


if __name__ == "__main__":
    main()