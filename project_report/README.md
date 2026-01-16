# User Management System

A Python-based user management system that demonstrates database operations, user-task relationships, and report generation.

## Features

- User management with CRUD operations
- Task assignment and tracking
- Report generation in JSON and CSV formats
- Modular architecture for easy maintenance

## Structure

```
project_report/
├── db/
│   └── user_queries_sqlite.py    # Database operations
├── reports/
│   └── generate_reports_sqlite.py # Report generation
├── users.db                      # SQLite database file
├── project_report.md             # Main project report
├── reports/
│   ├── user_summary_report.json  # Summary report
│   ├── user_task_report.json     # Detailed report
│   └── user_task_report.csv      # CSV export
└── README.md                     # This file
```

## Setup

The project uses SQLite to simulate PostgreSQL functionality. No additional setup is required beyond the included files.

## Usage

To run the report generation:

```bash
cd /workspace/project_report
python -c "
import sys
sys.path.insert(0, './db')
sys.path.insert(0, './reports')
from reports.generate_reports_sqlite import main
main()
"
```

## Reports Generated

After running the application, the following reports will be generated:

- `reports/user_summary_report.json` - Summary statistics
- `reports/user_task_report.json` - Detailed user-task relationships  
- `reports/user_task_report.csv` - CSV export of user-task data

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