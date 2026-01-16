# Project Report: User Management System

## Overview
This report documents the implementation of a user management system with PostgreSQL database (simulated with SQLite for this demonstration). The system allows for user management, task assignment, and reporting capabilities.

## Database Schema

### Users Table
- `id`: Primary key, auto-incrementing integer
- `username`: Unique text identifier
- `email`: Unique email address
- `full_name`: Full name of the user
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

### Tasks Table
- `id`: Primary key, auto-incrementing integer
- `user_id`: Foreign key referencing users table
- `title`: Task title
- `description`: Detailed task description
- `status`: Task status (pending, in_progress, completed)
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

## Features Implemented

### 1. User Management
- Find users by username
- Retrieve all users
- View user details

### 2. Task Management
- Assign tasks to users
- Track task status
- Retrieve user-specific tasks

### 3. Reporting System
- Generate summary reports
- Export data to JSON and CSV formats
- Task status breakdown
- User-task relationship mapping

## Sample Data
The system was initialized with 4 users and 6 tasks:

**Users:**
1. John Doe (john_doe)
2. Jane Smith (jane_smith)
3. Bob Wilson (bob_wilson)
4. Alice Brown (alice_brown)

**Task Distribution:**
- Completed: 2 tasks
- In Progress: 2 tasks
- Pending: 2 tasks

## Report Generation
The system can generate multiple types of reports:

### Summary Report
- Total users count
- Total tasks count
- Task status breakdown

### Detailed Reports
- User-task relationships
- Export to JSON format
- Export to CSV format

## Files Generated
- `user_summary_report.json`: Summary statistics
- `user_task_report.json`: Detailed user-task relationships
- `user_task_report.csv`: CSV export of user-task data

## Technical Implementation
- **Database**: SQLite (as a simulation of PostgreSQL)
- **Language**: Python
- **Reports**: JSON and CSV exports
- **Structure**: Modular design with separate modules for database operations and reporting

## Conclusion
The user management system provides a complete solution for tracking users and their associated tasks. The modular design allows for easy extension and maintenance. The reporting system enables data analysis and export capabilities.