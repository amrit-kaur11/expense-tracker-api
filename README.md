# Personal Expense Tracker API with Bill Attachments

A production-grade RESTful Personal Expense Tracker API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy ORM**, **Alembic**, **MinIO (S3-compatible Object Storage)**, and **Docker Compose**, adhering to strict **Clean Architecture** principles.

---

## 🌟 Architectural Overview

```text
Client (cURL / HTTP)
       │
       ▼
 Presentation Layer (FastAPI Routes: /api/v1/*)
       │
       ▼
 Business Logic Layer (Services: AuthService, ExpenseService, CategoryService, etc.)
       │
       ├───► Storage Repository (MinIO SDK -> S3 Object Storage for Bill Receipts)
       │
       ▼
 Data Access Layer (Repositories: UserRepository, ExpenseRepository, etc.)
       │
       ▼
 PostgreSQL Database (SQLAlchemy ORM + Alembic Migrations)
```

### Key Technical Highlights:
- **Clean Architecture:** Strict separation between Presentation (Routes), Domain Business Logic (Services), Data Access (Repositories), and Models.
- **User Data Isolation:** Every database operation guarantees strict multi-tenant data isolation by scoping queries with `user_id`.
- **MinIO Object Storage Integration:** Stores only object key references (e.g. `bills/user_1/expense_42_a1b2c3d4.jpg`) in PostgreSQL.
- **Dynamic Secure Signed URLs:** Generates time-limited, cryptographically signed GET URLs dynamically on expense retrieval without persisting temporary URLs in the database.
- **JWT Authentication & Token Revocation:** Implements JWT Bearer token authentication with bcrypt password hashing and database token blacklisting (`token_blacklist`) on logout.
- **Bonus Features Implemented:**
  1. **Budget Limits:** Set monthly category spending caps with automated `exceeds_budget: true` warning flags in monthly summary endpoints.
  2. **CSV Data Export:** Download monthly expense records directly as a CSV file.

---

## 🚀 Getting Started with Docker

### Prerequisites
- Docker Engine & Docker Compose installed.

### Execution Instructions

1. Clone or download the repository.
2. Launch all microservices (FastAPI application, PostgreSQL 15, MinIO, and bucket setup):
   ```bash
   docker-compose up --build
   ```
3. The API will be live at `http://localhost:8000`.
4. OpenAPI interactive documentation is available at `http://localhost:8000/docs`.

---

## 🧪 Comprehensive API Testing Instructions (cURL)

Follow these step-by-step cURL commands to test every single endpoint.

### 1. User Registration
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "password": "securepassword123"
  }'
```

### 2. User Login (Obtain JWT Access Token)
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@example.com",
    "password": "securepassword123"
  }'
```
*Save the returned `access_token` for subsequent requests:*
```bash
TOKEN="YOUR_JWT_ACCESS_TOKEN_HERE"
```

### 3. Get Current User Profile
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Create Category
```bash
curl -X POST "http://localhost:8000/api/v1/categories/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Groceries"
  }'
```

### 5. List Custom Categories
```bash
curl -X GET "http://localhost:8000/api/v1/categories/" \
  -H "Authorization: Bearer $TOKEN"
```

### 6. Set Monthly Category Budget Limit (Bonus Feature 1)
```bash
curl -X POST "http://localhost:8000/api/v1/budgets/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category_id": 1,
    "monthly_limit": 100.00
  }'
```

### 7. Create Expense
```bash
curl -X POST "http://localhost:8000/api/v1/expenses/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 150.75,
    "description": "Weekly supermarket shopping",
    "date": "2026-07-22",
    "category_id": 1
  }'
```

### 8. Upload Bill/Receipt Image to MinIO (`multipart/form-data`)
```bash
# Create a dummy image file for testing
echo "sample bill receipt data" > receipt.jpg

curl -X POST "http://localhost:8000/api/v1/expenses/1/bill" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@receipt.jpg;type=image/jpeg"
```

#### Example JSON Response (Including Dynamic Signed URL):
```json
{
  "amount": "150.75",
  "description": "Weekly supermarket shopping",
  "date": "2026-07-22",
  "category_id": 1,
  "id": 1,
  "user_id": 1,
  "bill_image_key": "bills/user_1/expense_1_a1b2c3d4.jpg",
  "bill_signed_url": "http://localhost:9000/expense-bills/bills/user_1/expense_1_a1b2c3d4.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minioadmin...",
  "created_at": "2026-07-22T01:59:00Z",
  "updated_at": "2026-07-22T01:59:10Z"
}
```

### 9. Retrieve Expense Details (With Signed URL)
```bash
curl -X GET "http://localhost:8000/api/v1/expenses/1" \
  -H "Authorization: Bearer $TOKEN"
```

### 10. Advanced Filtering & Pagination
```bash
curl -X GET "http://localhost:8000/api/v1/expenses/?start_date=2026-07-01&end_date=2026-07-31&category_id=1&limit=10&offset=0" \
  -H "Authorization: Bearer $TOKEN"
```

### 11. Monthly Expense Summary with Budget Warnings
```bash
curl -X GET "http://localhost:8000/api/v1/summary/monthly?year=2026&month=7" \
  -H "Authorization: Bearer $TOKEN"
```
#### Example Response:
```json
{
  "year": 2026,
  "month": 7,
  "total_monthly_expenses": "150.75",
  "categories_breakdown": [
    {
      "category_id": 1,
      "category_name": "Groceries",
      "total_amount": "150.75",
      "monthly_budget": "100.00",
      "exceeds_budget": true
    }
  ]
}
```

### 12. Export Monthly Expenses as CSV (Bonus Feature 2)
```bash
curl -X GET "http://localhost:8000/api/v1/expenses/export/csv?year=2026&month=7" \
  -H "Authorization: Bearer $TOKEN" \
  --output my_expenses_july_2026.csv
```

### 13. User Logout (Revoke Token)
```bash
curl -X POST "http://localhost:8000/api/v1/auth/logout" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🏗 Directory Structure

```text
.
├── alembic/                      # Database migrations configuration & scripts
│   ├── versions/                 # Alembic migration scripts
│   └── env.py                    # Alembic environment configuration
├── app/
│   ├── api/                      # Presentation Layer (Routers & Endpoints)
│   │   └── v1/
│   │       ├── endpoints/        # Auth, Categories, Expenses, Budgets, Summary
│   │       └── router.py         # Main V1 API Router aggregator
│   ├── core/                     # Core Configuration, Security, Exceptions, Logging
│   ├── db/                       # Database Base Model & Session factory
│   ├── models/                   # SQLAlchemy ORM Models
│   ├── repositories/             # Data Access Repositories (DB & MinIO)
│   ├── schemas/                  # Pydantic Request/Response validation models
│   ├── services/                 # Pure Business Logic Layer Services
│   └── main.py                   # FastAPI Application Entrypoint
├── docker-compose.yml            # Docker Orchestration (FastAPI, Postgres, MinIO)
├── Dockerfile                    # Container build configuration
├── requirements.txt              # Dependency specifications
└── README.md                     # Project Documentation
```
