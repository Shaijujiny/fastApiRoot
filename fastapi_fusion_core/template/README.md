# FastAPI Fusion Core

A high-performance, scalable FastAPI boilerplate with multi-database support (PostgreSQL, MySQL, MongoDB), GraphQL integration, and a premium architecture.

## 🚀 Key Features

- **🛡️ Custom Response System**: Unified JSON response structure for success and errors.
- **🌍 Multi-Database Integration**:
  - **PostgreSQL**: Async support via SQLAlchemy + asyncpg.
  - **MySQL**: Async support via SQLAlchemy + aiomysql.
  - **MongoDB**: Async support via Motor.
- **📊 GraphQL Support**: Modern GraphQL API using Strawberry with authentication integration.
- **🔐 Robust Authentication**: JWT-based auth with Redis session management.
- **⚡ Advanced Error Handling**: Global exception handlers for Pydantic validation, HTTP exceptions, and custom business logic errors.
- **📜 Swagger & ReDoc**: Automated API documentation.
- **🏗️ Premium Architecture**: Clean separation of models, schemes, services, and routers.

---

## 🛠️ Project Structure

```text
app/
├── api/                # REST API Routers & Services
│   ├── auth/           # Login, Register, Profile
│   ├── products/       # MongoDB CRUD Reference
│   └── utils/          # Database utility routes
├── core/               # Global configurations & Middleware
│   ├── error/          # Error types and message codes
│   ├── middleware/     # Logging & Exception handling
│   └── response/       # Base schemas & Response builder
├── database/           # DB Drivers & Session management
├── depends/            # FastAPI Dependencies (Auth, DB, etc.)
├── graphql/            # Strawberry GraphQL Schema & Context
├── models/             # SQLAlchemy & MongoDB Models
└── utils/              # Helper utilities
```

---

## 🚦 Getting Started

### 1. Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env.development` or `.env.production` file using variables mapped to `app/config.py`:

```env
PROJECT_NAME="FastAPI Fusion"
API_VERSION="1.0.0"
ENVIRONMENT="development"

# PostgreSQL (Example)
POSTGRES_USER=myuser
POSTGRES_PASSWORD=secret
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_DB=fastapii

# MySQL
MYSQL_USER=...
MYSQL_PASSWORD=...

# MongoDB
MONGODB_URI=...

# Redis & JWT Core
REDIS_DB_HOST=127.0.0.1
APP_JWT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----..."
APP_JWT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----..."
```

### 3. Database Initialization

To automatically spawn the necessary tables defined in your SQLAlchemy models (PostgreSQL & MySQL), use the internal setup endpoint. 

*(Ensure your `fastapii` or specified DB catalog natively exists in Postgres before hitting this endpoint. Run `createdb fastapii` inside Postgres).*

1. Run the server (see step 4)
2. Visit `http://localhost:8000/utils/create-tables`

### 4. Running the Server

```bash
uvicorn app.main:app --reload
```

### 5. Running the Tests

A comprehensive test suite is scaffolded using `pytest`, `pytest-asyncio`, and `httpx`.

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run the test suite
pytest tests/ -v
```

---

## 📖 API Documentation

- **Swagger**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **GraphQL IDL**: [http://localhost:8000/graphql](http://localhost:8000/graphql)

---

## 🧪 Advanced Usage Examples

### MongoDB CRUD (REST)
Access the MongoDB-backed product management at `/api/products`. This implementation uses `Motor` for asynchronous operations.

### GraphQL Query Example
```graphql
query {
  me {
    username
    role
  }
  products {
    name
    price
  }
}
```

---

## 🤝 Contribution

Designed for high-performance enterprise applications. Feel free to extend the models or add new services in the `app/api` directory.
