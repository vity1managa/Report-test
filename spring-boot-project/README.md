# User Management System - Spring Boot

This is a Spring Boot application for managing users and their tasks with comprehensive reporting capabilities. The application uses PostgreSQL as the database and provides REST APIs for user and task management.

## Features

- **User Management**: Create, read, update, and delete users
- **Task Management**: Assign tasks to users with different statuses (PENDING, IN_PROGRESS, COMPLETED)
- **Reporting**: Generate comprehensive reports on user activities and task distributions
- **REST APIs**: Full CRUD operations via REST endpoints
- **Docker Support**: Easy deployment with Docker and docker-compose

## Technology Stack

- Spring Boot 3.2.0
- Java 17
- Spring Data JPA
- PostgreSQL
- Hibernate
- Docker & Docker Compose

## Prerequisites

- Java 17
- Maven
- Docker and Docker Compose
- PostgreSQL client (optional, for direct database access)

## Setup Instructions

### Option 1: Running with Docker (Recommended)

1. Navigate to the docker directory:
```bash
cd docker
```

2. Start the services:
```bash
docker-compose up -d
```

3. The application will be available at `http://localhost:8080`
4. The PostgreSQL database will be available at `http://localhost:5432`

### Option 2: Running locally

1. Make sure PostgreSQL is installed and running
2. Create a database named `usermanagement`
3. Update `application.properties` with your database credentials
4. Build and run the application:
```bash
mvn clean install
mvn spring-boot:run
```

## API Endpoints

### User Management
- `GET /api/users` - Get all users
- `GET /api/users/{id}` - Get user by ID
- `GET /api/users/username/{username}` - Get user by username
- `POST /api/users` - Create a new user
- `PUT /api/users/{id}` - Update a user
- `DELETE /api/users/{id}` - Delete a user
- `GET /api/users/{id}/tasks` - Get tasks for a specific user
- `GET /api/users/username/{username}/tasks` - Get tasks for a user by username

### Task Management
- `GET /api/tasks` - Get all tasks
- `GET /api/tasks/{id}` - Get task by ID
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `GET /api/tasks/status/{status}` - Get tasks by status
- `GET /api/tasks/user/{userId}` - Get tasks by user ID

### Reports
- `GET /api/reports/user-report` - Generate user activity report

## Sample Data

The application comes with sample data preloaded:
- Users: john_doe, jane_smith, bob_wilson, alice_brown
- Tasks assigned to various users with different statuses

## Database Schema

The application uses two main tables:

**users table:**
- id (Primary Key)
- username (Unique, Not Null)
- email (Not Null)
- first_name
- last_name

**tasks table:**
- id (Primary Key)
- title (Not Null)
- description
- status (PENDING, IN_PROGRESS, COMPLETED)
- user_id (Foreign Key referencing users.id)

## Testing the Application

Once the application is running, you can test the APIs using curl or a tool like Postman:

Get all users:
```bash
curl http://localhost:8080/api/users
```

Get user report:
```bash
curl http://localhost:8080/api/reports/user-report
```

## Project Structure

```
src/
├── main/
│   ├── java/com/example/usermanagement/
│   │   ├── UserManagementApplication.java
│   │   ├── controller/
│   │   │   ├── UserController.java
│   │   │   ├── TaskController.java
│   │   │   └── ReportController.java
│   │   ├── entity/
│   │   │   ├── User.java
│   │   │   ├── Task.java
│   │   │   └── TaskStatus.java
│   │   ├── repository/
│   │   │   ├── UserRepository.java
│   │   │   └── TaskRepository.java
│   │   └── service/
│   │       ├── UserService.java
│   │       ├── TaskService.java
│   │       └── ReportService.java
│   └── resources/
│       └── application.properties
├── docker/
│   ├── docker-compose.yml
│   └── init.sql
├── pom.xml
└── Dockerfile
```

## Docker Configuration

The docker-compose.yml sets up:
- A PostgreSQL database container
- The Spring Boot application container
- Network connectivity between containers
- Volume persistence for the database
- Environment variable configuration

## Error Handling

The application includes proper error handling:
- Returns HTTP 404 for resources not found
- Returns HTTP 409 for conflicts (like duplicate usernames)
- Returns HTTP 400 for bad requests
- Proper exception handling throughout the application

## Security Considerations

For production use, consider adding:
- Spring Security for authentication and authorization
- Input validation
- Rate limiting
- HTTPS/TLS encryption
- SQL injection prevention (already handled by JPA)