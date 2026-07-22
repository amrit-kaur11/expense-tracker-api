<div align="center">

# 💰 Personal Expense Tracker API

### A Production-Ready Expense Management Backend built with FastAPI, PostgreSQL, JWT Authentication, Docker & MinIO

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?style=for-the-badge&logo=docker)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?style=for-the-badge)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange?style=for-the-badge)
![MinIO](https://img.shields.io/badge/MinIO-S3_Compatible-red?style=for-the-badge)

</p>

---

*A secure, scalable, and containerized RESTful Expense Tracker API designed with Clean Architecture principles. The application enables users to securely manage expenses, organize custom categories, upload bill images, and generate monthly financial summaries while following modern backend development practices.*

</div>

---

# 📖 Project Overview

Managing personal expenses is an everyday requirement, but many applications only focus on recording transactions without emphasizing secure backend architecture, scalable storage, or maintainable code organization.

This project demonstrates how to build a **production-style backend service** using **FastAPI**, **PostgreSQL**, **JWT Authentication**, **Docker**, and **MinIO** while following Clean Architecture principles.

The API allows authenticated users to:

- Securely register and log in.
- Organize expenses using custom categories.
- Perform complete CRUD operations on expenses.
- Upload receipt or bill images.
- Retrieve bill images through secure signed URLs.
- View monthly spending summaries categorized by expense type.
- Maintain complete data isolation between users.

The application is fully containerized using Docker and designed to be easily deployable and scalable.

---

# 🎯 Assignment Objective

The objective of this project is to design and implement a secure RESTful backend API that demonstrates:

- Authentication & Authorization
- Database Design
- REST API Development
- File Storage
- Object Storage Integration
- Docker Containerization
- Clean Code Architecture
- Scalable Backend Design
- API Documentation
- Secure Development Practices

The project emphasizes maintainability, modularity, and production-ready backend engineering principles.

---

# ✨ Key Features

## 🔐 Authentication

- User Registration
- User Login
- JWT Authentication
- Password Hashing (bcrypt)
- Secure Logout using Token Blacklisting
- Protected Endpoints

---

## 📂 Category Management

Users can create their own custom categories such as:

- Groceries
- Rent
- Utilities
- Entertainment
- Transportation
- Shopping

Each user can only access their own categories.

---

## 💵 Expense Management

Users can:

- Create Expenses
- Retrieve Expenses
- Update Expenses
- Delete Expenses

Each expense contains:

- Amount
- Description
- Expense Date
- Category
- Receipt Image
- Creation Timestamp

---

## 🧾 Receipt Upload

The API supports uploading receipt images.

Uploaded images are:

- Stored in MinIO
- Referenced using object keys
- Never stored directly inside PostgreSQL
- Retrieved using secure signed URLs

---

## 📊 Monthly Financial Summary

The application provides financial insights including:

- Current Month Total Spending
- Category-wise Expense Breakdown
- Budget Monitoring (Bonus)
- CSV Export (Bonus)

---

# 🛠 Technology Stack

| Layer | Technology |
|---------|------------|
| Backend Framework | FastAPI |
| Programming Language | Python 3 |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database Migration | Alembic |
| Authentication | JWT |
| Password Security | bcrypt |
| Object Storage | MinIO |
| Validation | Pydantic |
| API Documentation | Swagger UI |
| Containerization | Docker |
| Multi-container Orchestration | Docker Compose |

---

# 💡 Why These Technologies?

## FastAPI

FastAPI was selected because it provides:

- High performance
- Automatic OpenAPI documentation
- Dependency Injection
- Excellent type validation
- Asynchronous request handling

making it one of the most suitable frameworks for modern REST APIs.

---

## PostgreSQL

PostgreSQL provides:

- ACID Compliance
- Strong Relational Modeling
- Efficient Aggregation Queries
- Excellent Foreign Key Support
- High Scalability

making it an ideal database for financial applications.

---

## SQLAlchemy

SQLAlchemy separates business logic from persistence while providing:

- ORM Mapping
- Relationship Management
- Database Portability
- Clean Query Construction

---

## MinIO

Instead of storing image files inside PostgreSQL, receipt images are stored inside MinIO because:

- S3 Compatible
- Lightweight
- Supports Signed URLs
- Easy Docker Integration
- No External Cloud Credentials Required

---

## Docker

Docker ensures the application behaves consistently across environments by containerizing:

- FastAPI Application
- PostgreSQL Database
- MinIO Storage

This allows the project to be executed with a single command.

---

# 🏗 System Architecture

```text
                    Client
                       │
        ───────────────┼───────────────
                       │
                       ▼
                 FastAPI Backend
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
 Authentication   Business Logic   File Storage
        │              │              │
        ▼              ▼              ▼
      JWT         Service Layer     MinIO
        │              │
        └──────────────┼──────────────┘
                       │
                       ▼
                Repository Layer
                       │
                       ▼
                  PostgreSQL
```

---

# 📂 Project Structure

```text
expense-tracker-api/
│
├── app/
│   ├── api/
│   │   ├── routes/
│   │   └── dependencies.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── auth.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── expense.py
│   │   ├── blacklist.py
│   │   └── budget.py
│   │
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── storage/
│   ├── utils/
│   └── main.py
│
├── alembic/
├── docs/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

# 🎯 Design Principles

The project follows the following engineering principles:

- Clean Architecture
- Separation of Concerns
- Repository Pattern
- Service Layer Pattern
- Dependency Injection
- RESTful API Design
- Secure Authentication
- Containerized Deployment
- Scalable Code Organization
- Modular Development

---

# 🗄 Database Design

The application follows a normalized relational database design to ensure data integrity, efficient querying, and scalability.

## Entity Relationship Diagram (ERD)

```text
                        +----------------------+
                        |        Users         |
                        +----------------------+
                        | id (PK)             |
                        | name               |
                        | email             |
                        | password_hash     |
                        | created_at        |
                        +---------+----------+
                                  |
                     One User
                                  |
                         Many Categories
                                  |
                                  ▼
                     +----------------------+
                     |     Categories       |
                     +----------------------+
                     | id (PK)             |
                     | name               |
                     | user_id (FK)       |
                     +---------+----------+
                               |
                     One Category
                               |
                         Many Expenses
                               |
                               ▼
                     +----------------------+
                     |      Expenses        |
                     +----------------------+
                     | id (PK)             |
                     | user_id (FK)        |
                     | category_id (FK)    |
                     | amount              |
                     | description         |
                     | expense_date        |
                     | bill_image_key      |
                     | created_at          |
                     +----------------------+

Users
   │
   └──────────────► Token Blacklist

Users
   │
   └──────────────► Budget
```

---

## Database Tables

### 👤 Users

Stores authentication and account information.

| Column | Description |
|---------|-------------|
| id | Primary Key |
| name | User Name |
| email | Unique Email Address |
| password_hash | bcrypt Password |
| created_at | Registration Timestamp |

---

### 📂 Categories

Stores user-defined expense categories.

Examples:

- Groceries
- Rent
- Entertainment
- Shopping
- Utilities

Each category belongs to exactly one user.

---

### 💵 Expenses

Stores expense records.

Each expense references:

- User
- Category
- Receipt Image

Fields:

| Field | Description |
|---------|-------------|
| Amount | Expense Amount |
| Description | Expense Description |
| Expense Date | Date of Expense |
| Category | Expense Category |
| Bill Image Key | MinIO Object Key |

---

### 🚫 Token Blacklist

Used during logout.

Instead of deleting JWT tokens, invalidated tokens are stored until expiration.

Benefits:

- Secure Logout
- Stateless Authentication
- Token Revocation

---

### 💰 Budget (Bonus)

Stores monthly spending limits.

Fields include:

- User
- Category
- Monthly Limit

Used by the Monthly Summary endpoint to detect budget violations.

---

# 🔄 Application Workflow

The request lifecycle follows a layered architecture.

```text
          HTTP Request
                │
                ▼
        FastAPI Router
                │
                ▼
        Dependency Injection
                │
                ▼
         Authentication
                │
                ▼
         Service Layer
                │
                ▼
      Repository Layer
                │
                ▼
        PostgreSQL Database
                │
                ▼
       JSON API Response
```

---

# 🔐 Authentication Flow

The application implements stateless JWT authentication.

```text
              Register
                  │
                  ▼
         Password Hashing
          (bcrypt)
                  │
                  ▼
         Store in PostgreSQL
                  │

──────────────────────────────────

               Login
                  │
                  ▼
      Verify Email & Password
                  │
                  ▼
          Generate JWT Token
                  │
                  ▼
          Return Access Token

──────────────────────────────────

         Protected Endpoint
                  │
                  ▼
      Validate JWT Signature
                  │
                  ▼
      Extract Current User
                  │
                  ▼
        Execute API Request

──────────────────────────────────

               Logout
                  │
                  ▼
      Store Token in Blacklist
                  │
                  ▼
        Future Requests Rejected
```

---

# 🧾 Receipt Upload Flow

Receipt images are stored outside the relational database.

```text
             Client
                │
                │ Upload Receipt
                ▼
         FastAPI Endpoint
                │
                ▼
        Validate File Type
                │
                ▼
      Upload to MinIO Bucket
                │
                ▼
     Generate Object Key
                │
                ▼
 Store Object Key in PostgreSQL
                │
                ▼
     Expense Successfully Saved
```

---

# 🔗 Signed URL Generation

Images are **never exposed directly**.

Whenever an expense is requested:

```text
Fetch Expense
      │
      ▼
Retrieve Object Key
      │
      ▼
Generate Signed URL
      │
      ▼
Return Secure Temporary URL
```

Advantages:

- No public image exposure
- Time-limited access
- Secure object storage
- Prevents unauthorized downloads

---

# 📊 Monthly Summary Workflow

```text
Fetch Current Month Expenses
              │
              ▼
Aggregate Total Amount
              │
              ▼
Group by Category
              │
              ▼
Compare with Budget Limits
              │
              ▼
Generate JSON Response
```

Example Response

```json
{
  "month": "July 2026",
  "total_spent": 15420,
  "categories": [
    {
      "category": "Groceries",
      "amount": 5100
    },
    {
      "category": "Rent",
      "amount": 8000
    },
    {
      "category": "Transport",
      "amount": 2320
    }
  ]
}
```

---

# 📡 REST API Reference

## 🔐 Authentication

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Authenticate user |
| POST | `/auth/logout` | Logout current user |

---

## 📂 Categories

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/categories` | Create category |
| GET | `/categories` | List categories |
| DELETE | `/categories/{id}` | Delete category |

---

## 💵 Expenses

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/expenses` | Create expense |
| GET | `/expenses` | List expenses |
| GET | `/expenses/{id}` | Expense details |
| PUT | `/expenses/{id}` | Update expense |
| DELETE | `/expenses/{id}` | Delete expense |

---

## 🧾 Receipt Upload

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/expenses/{id}/receipt` | Upload bill image |

---

## 📊 Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/summary/current-month` | Monthly expense summary |

---

# ⚙️ Getting Started

This guide walks you through setting up and running the project locally using Docker or a standard Python environment.

---

# 📋 Prerequisites

Before running the application, ensure the following software is installed on your system.

| Software | Version |
|----------|----------|
| Python | 3.12+ |
| Docker Desktop | Latest |
| Docker Compose | Latest |
| Git | Latest |
| PostgreSQL | 16+ (Only if not using Docker) |

---

# 📥 Clone the Repository

```bash
git clone https://github.com/amrit-kaur11/expense-tracker-api.git

cd expense-tracker-api
```

---

# 🐍 Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🌍 Environment Variables

Create a `.env` file inside the project root.

```env
DATABASE_URL=postgresql://postgres:password@db:5432/expense_db

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

MINIO_ENDPOINT=minio:9000

MINIO_ACCESS_KEY=minioadmin

MINIO_SECRET_KEY=minioadmin

MINIO_BUCKET=expense-bills

MINIO_SECURE=False
```

---

# 🐳 Running with Docker

The project is fully containerized using Docker Compose.

Start all required services:

```bash
docker compose up --build
```

or run in detached mode:

```bash
docker compose up -d --build
```

Docker Compose starts:

- FastAPI Application
- PostgreSQL Database
- MinIO Object Storage

without requiring any external cloud services.

---

# 🛑 Stop Containers

```bash
docker compose down
```

To remove volumes as well:

```bash
docker compose down -v
```

---

# 🗄 Database Migration

The project uses Alembic for schema migrations.

Create a migration:

```bash
alembic revision --autogenerate -m "Initial Migration"
```

Apply migration:

```bash
alembic upgrade head
```

Rollback one version:

```bash
alembic downgrade -1
```

---

# ▶️ Running Without Docker

If Docker is unavailable, the application can be started locally.

Run the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://localhost:8000
```

---

# 📖 Interactive API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

These interfaces allow developers to:

- Test APIs
- View request models
- Explore response schemas
- Authenticate using JWT
- Debug endpoints

without external tools.

---

# 🧪 Testing the API

Example Register Request

```bash
curl -X POST "http://localhost:8000/auth/register" \
-H "Content-Type: application/json" \
-d '{
"name":"Amrit",
"email":"amrit@example.com",
"password":"Password123"
}'
```

---

## Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
-H "Content-Type: application/json" \
-d '{
"email":"amrit@example.com",
"password":"Password123"
}'
```

---

## Create Category

```bash
curl -X POST "http://localhost:8000/categories" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-H "Content-Type: application/json" \
-d '{
"name":"Groceries"
}'
```

---

## Create Expense

```bash
curl -X POST "http://localhost:8000/expenses" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-H "Content-Type: application/json" \
-d '{
"amount":450,
"description":"Weekly Grocery Shopping",
"category_id":"CATEGORY_ID",
"expense_date":"2026-07-22"
}'
```

---

## Upload Receipt

```bash
curl -X POST \
"http://localhost:8000/expenses/EXPENSE_ID/receipt" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-F "file=@receipt.jpg"
```

---

## Get Monthly Summary

```bash
curl -X GET \
"http://localhost:8000/summary/current-month" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

# 📄 Example JSON Response

```json
{
    "expense_id": "b93dff...",
    "amount": 450,
    "category": "Groceries",
    "description": "Weekly Grocery Shopping",
    "receipt_url": "https://minio/signed-url",
    "created_at": "2026-07-22T10:35:12"
}
```

---

# 📊 Logging

The application logs:

- Authentication events
- Request validation errors
- Database exceptions
- Storage operations
- Internal server errors

Logging improves debugging and production monitoring.

---

# 📂 Error Handling

The API returns standardized HTTP responses.

| Status Code | Meaning |
|------------|---------|
| 200 | Success |
| 201 | Resource Created |
| 400 | Invalid Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource Not Found |
| 409 | Conflict |
| 422 | Validation Error |
| 500 | Internal Server Error |

---

# 🔄 API Development Workflow

```text
Developer
     │
     ▼
GitHub Repository
     │
     ▼
Docker Compose
     │
     ▼
FastAPI Application
     │
     ▼
Swagger Testing
     │
     ▼
PostgreSQL
     │
     ▼
MinIO
```

---

# 🧪 Code Quality

The project emphasizes:

- Modular Design
- Reusable Components
- Dependency Injection
- Repository Pattern
- Service Layer Pattern
- Type Safety
- Input Validation
- Consistent Error Responses

---

# 🔒 Security Features

Security has been considered throughout the application's design to protect user data and ensure secure API interactions.

## Authentication & Authorization

- JWT-based stateless authentication
- Secure password hashing using bcrypt
- Protected API endpoints
- User-specific resource access
- Token validation for every authenticated request
- Token blacklisting for secure logout

---

## Password Security

Passwords are never stored in plaintext.

The application uses **bcrypt** to:

- Salt passwords automatically
- Prevent rainbow table attacks
- Secure user credentials

---

## Database Security

The project follows secure database practices:

- Parameterized ORM queries
- Foreign key constraints
- Input validation
- Normalized relational schema
- User data isolation

---

## Object Storage Security

Receipt images are stored securely using MinIO.

Security measures include:

- Images are never stored inside PostgreSQL.
- Only object references are stored in the database.
- Files are accessed through temporary signed URLs.
- Objects remain private by default.
- Direct public access is disabled.

---

## API Security

The API includes:

- Request validation using Pydantic
- HTTP status code standardization
- Exception handling
- Input sanitization
- Authentication middleware
- Authorization checks

---

# 🏛 Engineering Decisions

Several architectural decisions were made to improve maintainability, scalability, and security.

---

## Why FastAPI?

FastAPI was selected because it offers:

- High-performance asynchronous request handling
- Automatic OpenAPI documentation
- Built-in dependency injection
- Strong type validation
- Excellent developer experience

---

## Why PostgreSQL?

PostgreSQL was chosen due to:

- ACID compliance
- Strong relational modeling
- Excellent aggregation capabilities
- Reliable foreign key enforcement
- Production-grade scalability

---

## Why SQLAlchemy?

SQLAlchemy provides:

- ORM abstraction
- Relationship management
- Database portability
- Clean repository implementation
- Easier schema migrations

---

## Why MinIO?

Instead of storing files inside PostgreSQL:

- Images are stored separately
- Database remains lightweight
- Faster database queries
- S3-compatible API
- Easy migration to AWS S3 in production

---

## Why Repository Pattern?

Separating database operations into repositories provides:

- Better separation of concerns
- Easier testing
- Reusable queries
- Cleaner service layer
- Improved maintainability

---

## Why Service Layer?

Business logic is isolated from API routes.

Benefits include:

- Reusable logic
- Cleaner endpoints
- Easier debugging
- Improved scalability

---

# 📈 Scalability Considerations

The project has been designed with future scalability in mind.

Potential improvements include:

- Redis Caching
- Refresh Tokens
- Role-Based Access Control (RBAC)
- Pagination
- Rate Limiting
- Background Tasks
- Celery Workers
- Email Notifications
- Multi-Currency Support
- Cloud Object Storage (AWS S3)
- Kubernetes Deployment
- CI/CD Pipelines

---

# 📋 Assignment Requirement Coverage

| Requirement | Status |
|-------------|--------|
| User Registration | ✅ |
| User Login | ✅ |
| User Logout | ✅ |
| JWT Authentication | ✅ |
| Category CRUD | ✅ |
| Expense CRUD | ✅ |
| Receipt Upload | ✅ |
| Signed URL Generation | ✅ |
| Monthly Summary | ✅ |
| PostgreSQL Database | ✅ |
| Docker Support | ✅ |
| Docker Compose | ✅ |
| API Documentation | ✅ |
| Alembic Migration | ✅ |
| Budget Limits (Bonus) | ✅ |
| CSV Export (Bonus) | ✅ |

---

# 📌 Challenges Addressed

During development, several common backend challenges were considered.

- Designing a normalized relational database
- Implementing secure JWT authentication
- Isolating user-specific resources
- Managing object storage separately from structured data
- Generating secure signed URLs
- Containerizing multiple services
- Organizing the project using Clean Architecture

---

# 🚀 Future Improvements

The current implementation provides a strong backend foundation while leaving room for future enhancements.

Possible improvements include:

- Expense Analytics Dashboard
- AI-powered Expense Categorization
- OCR-based Receipt Data Extraction
- Email Reports
- Push Notifications
- Multi-user Shared Expense Groups
- Recurring Expenses
- Expense Forecasting
- Mobile API Versioning
- Cloud Deployment (AWS/GCP/Azure)

---

# 🧪 Testing Strategy

The application is designed to support testing at multiple levels.

### Unit Tests

- Services
- Repository Layer
- Authentication

### Integration Tests

- Database Operations
- File Uploads
- Authentication Flow

### API Tests

- CRUD Operations
- Authorization
- Validation
- Error Responses

---

# 📚 Learning Outcomes

This project demonstrates practical experience with:

- REST API Development
- Authentication & Authorization
- PostgreSQL Database Design
- SQLAlchemy ORM
- Docker & Docker Compose
- Object Storage Integration
- Secure Backend Development
- Clean Architecture
- Repository Pattern
- Service Layer Pattern
- API Documentation
- Production-ready Project Organization

---

# 👨‍💻 Author

## Amrit Kaur

Backend & AI Engineer

### Connect with me

- GitHub: https://github.com/amrit-kaur11
- LinkedIn: www.linkedin.com/in/amrit-kaur-a31b50251 

---

# 📄 License

This project was developed as part of a backend engineering technical assessment.

The repository is intended for demonstration, learning, and evaluation purposes.

---

<div align="center">

### ⭐ If you found this project interesting, consider giving it a star!

Made with ❤️ using FastAPI, PostgreSQL, Docker & MinIO

</div>