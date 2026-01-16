import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os
from typing import List, Dict, Optional


class UserDatabaseManager:
    def __init__(self):
        self.connection_params = {
            'host': 'localhost',
            'database': 'user_management',
            'user': 'admin',
            'password': 'password123',
            'port': 5432
        }
    
    def get_connection(self):
        """Establish connection to PostgreSQL database"""
        try:
            conn = psycopg2.connect(**self.connection_params)
            return conn
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            return None
    
    def find_user_by_username(self, username: str) -> Optional[Dict]:
        """Find a user by username"""
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE username = %s", 
                    (username,)
                )
                result = cursor.fetchone()
                return dict(result) if result else None
        except psycopg2.Error as e:
            print(f"Error querying user: {e}")
            return None
        finally:
            conn.close()
    
    def get_all_users(self) -> List[Dict]:
        """Get all users from the database"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
                results = cursor.fetchall()
                return [dict(row) for row in results]
        except psycopg2.Error as e:
            print(f"Error fetching users: {e}")
            return []
        finally:
            conn.close()
    
    def get_user_tasks(self, user_id: int) -> List[Dict]:
        """Get all tasks for a specific user"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM tasks WHERE user_id = %s ORDER BY created_at DESC", 
                    (user_id,)
                )
                results = cursor.fetchall()
                return [dict(row) for row in results]
        except psycopg2.Error as e:
            print(f"Error fetching user tasks: {e}")
            return []
        finally:
            conn.close()
    
    def get_all_users_with_tasks(self) -> List[Dict]:
        """Get all users along with their tasks"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
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
        except psycopg2.Error as e:
            print(f"Error fetching users with tasks: {e}")
            return []
        finally:
            conn.close()


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