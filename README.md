# Order Management System

Order management system with state machine, audit logs, and transition management.

## 🔧 Environment Variables Setup

This project uses environment variables to handle sensitive data and environment-specific configurations.

### Backend

1. **Copy the example file:**
   ```bash
   cd Backend
   cp .env.example .env
   ```

2. **Edit the `.env` file with your credentials:**
   ```dotenv
   # Database Configuration
   DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
   DATABASE_HOST=your-database-host.rds.amazonaws.com
   DATABASE_PORT=5432
   DATABASE_USER=your_database_user
   DATABASE_PASSWORD=your_database_password
   DATABASE_NAME=your_database_name

   # CORS Configuration
   CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
   ```

### Frontend

1. **Copy the example file:**
   ```bash
   cd Frontend
   cp .env.example .env
   ```

2. **Edit the `.env` file:**
   ```dotenv
   # API Configuration
   VITE_API_BASE_URL=http://localhost:8000
   ```

## 🚀 Installation and Execution

### With Docker Compose (Recommended)

```bash
# Make sure you have the .env files configured
docker-compose up --build
```

### Manual

#### Backend
```bash
cd Backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd Frontend
npm install
npm run dev
```

## 🧪 Unit Tests

The backend includes a comprehensive suite of unit tests that cover critical business logic.

### Test Structure

```
Backend/tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_state_machine.py    # State machine tests
├── test_api_endpoints.py    # API integration tests
└── test_services.py         # Service layer tests
```

### Running Tests

#### Install Testing Dependencies

```bash
cd Backend
pip install -r requirements.txt  # Includes testing dependencies
```

#### Run All Tests

```bash
cd Backend
pytest
```

#### Run Tests with Coverage

```bash
cd Backend
pytest --cov=app --cov-report=html
```

The coverage report will be generated in `htmlcov/index.html`

#### Run Tests in Verbose Mode

```bash
pytest -v
```

#### Run a Specific Test File

```bash
pytest tests/test_state_machine.py
```

#### Run a Specific Test

```bash
pytest tests/test_state_machine.py::TestOrderStateMachine::test_pending_to_in_preparation_under_threshold -v
```

### Troubleshooting

**Tests fail with database errors:**
- Tests use in-memory SQLite, not the production database
- Verify that `conftest.py` is configured correctly

**Import errors:**
- Make sure to run from the `Backend` directory:
  ```bash
  cd Backend
  pytest
  ```

**Async warnings:**
- Install `pytest-asyncio`:
  ```bash
  pip install pytest-asyncio
  ```

## 📚 Main Endpoints

- `GET /orders` - List orders
- `POST /orders` - Create order
- `POST /orders/{id}/transition` - State transition
- `GET /orders/{id}/logs` - Order logs
- `GET /orders/logs` - All system logs

## 📊 Technologies Used

### Backend
- FastAPI (Async web framework)
- SQLAlchemy 2.0 (Async ORM)
- PostgreSQL (Database)
- Pydantic (Data validation)
- Pytest (Testing)
- Uvicorn (ASGI server)

### Frontend
- React 18
- TypeScript
- Vite (Build tool)
- Axios (HTTP client)
- Lucide React (Icons)
