# Task Management API

A RESTful API for managing tasks with user authentication, categories,
priorities, and due dates.

------------------------------------------------------------------------

## Project Overview

The Task Management API project allows users to create, update, delete, 
and manage tasks efficiently.

------------------------------------------------------------------------


## Folder Structure
- config/: Django project settings
- tasks/: API app with models, views, serializers, and URLs
- manage.py: Django management file

------------------------------------------------------------------------


## Features

- User authentication (Login & Registration)
- Create, read, update, and delete tasks (CRUD)
- Task status management (Pending / In Progress / Completed)
- Secure API endpoints
- PostgreSQL database integration
- RESTful API design

------------------------------------------------------------------------

## Technologies Used

- Backend: Python, Django
- API Framework: Django Rest Framework (DRF)
- Database: PostgreSQL
- Authentication: Django Authentication / Token-based Auth
- Version: Git & GitHub

------------------------------------------------------------------------

## Database Design (ERD)

### User

-   id (PK)
-   username (Unique)
-   email (Unique)
-   password

### Task

-   id (PK)
-   title
-   description
-   status
-   priority
-   due_date
-   created_at
-   updated_at
-   user_id (FK)
-   category_id (FK)

### Category

-   id (PK)
-   name
-   user_id (FK)

------------------------------------------------------------------------

## Relationships

-   One User → Many Tasks
-   One User → Many Categories
-   One Category → Many Tasks

------------------------------------------------------------------------

## Installation

1.  Clone the repository
2.  Install dependencies
3.  Configure .env
4.  Run server

------------------------------------------------------------------------

## API Endpoints

### Authentication
Base URL: https://eddymyk.pythonanywhere.com/api
Register a New User Endpoint: https://eddymyk.pythonanywhere.com/api/register/
Login: https://eddymyk.pythonanywhere.com/api/login/
username: "eddymyk"
password: "Password123"

### Tasks

-   GET - /api/tasks/
-   POST - /api/tasks/
-   GET - /api/tasks/{id}/
-   PUT - /api/tasks/{id}/
-   DELETE - /api/tasks/{id}/


### Categories

-   GET /api/categories/
-   POST /api/categories/

Example Task JSON
{
  "title": "Finish project",
  "description": "Complete the API project",
  "due_date": "2026-03-01T12:00:00Z",
  "priority": "High",
  "status": "Pending"
}
------------------------------------------------------------------------

## Author

Edidiong Archibong


