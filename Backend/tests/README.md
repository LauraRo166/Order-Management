# Backend Unit Tests

## Overview

Comprehensive test suite for the TecSai Order Management System backend.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures and configuration
├── test_state_machine.py    # State machine logic tests
├── test_api_endpoints.py    # API integration tests
└── test_services.py         # Service layer unit tests
```

## Running Tests

### Install Test Dependencies

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_state_machine.py
```

### Run with Coverage Report

```bash
pytest --cov=app --cov-report=html
```

Coverage report will be generated in `htmlcov/index.html`

### Run Specific Test

```bash
pytest tests/test_state_machine.py::TestOrderStateMachine::test_valid_transition_pending_to_in_preparation
```

### Run Tests in Verbose Mode

```bash
pytest -v
```

### Run Tests with Output

```bash
pytest -s
```

## Test Categories

### 1. State Machine Tests (`test_state_machine.py`)

Tests the core business logic of the order state machine:

- ✅ Valid state transitions
- ✅ Invalid transition prevention
- ✅ Business rules ($1000 threshold for review)
- ✅ Cancellation policies (blocked after shipping)
- ✅ Allowed actions per state

**Example:**
```python
def test_valid_transition_pending_to_in_preparation():
    """Test valid transition from PENDING to IN_PREPARATION."""
    is_valid, new_state, error = OrderStateMachine.is_valid_transition(
        current_state="pending",
        action="start_preparation",
        order_amount=500.0
    )
    assert is_valid is True
    assert new_state == "in_preparation"
```

### 2. API Endpoint Tests (`test_api_endpoints.py`)

Integration tests for REST API endpoints:

- ✅ Customer CRUD operations
- ✅ Product CRUD operations
- ✅ Order creation and retrieval
- ✅ State transitions
- ✅ Transition logs
- ✅ Allowed actions endpoint

**Example:**
```python
@pytest.mark.asyncio
async def test_create_customer(client, sample_customer_data):
    """Test creating a customer."""
    response = await client.post("/customers/", json=sample_customer_data)
    assert response.status_code == 201
```

### 3. Service Layer Tests (`test_services.py`)

Unit tests for business logic services with mocked dependencies:

- ✅ Transition service logic
- ✅ Business rule enforcement
- ✅ Error handling
- ✅ Repository interaction

**Example:**
```python
@pytest.mark.asyncio
async def test_transition_order_success(transition_service, mock_order_repo):
    """Test successful order transition."""
    result = await transition_service.transition_order(order_id, "start_preparation")
    assert result["new_state"] == "in_preparation"
```

## Fixtures

### Database Fixtures (`conftest.py`)

- `test_db_engine`: In-memory SQLite database for testing
- `test_db_session`: Database session for tests
- `client`: HTTP test client with DB override

### Data Fixtures

- `sample_customer_data`: Customer test data
- `sample_product_data`: Product test data
- `sample_order_data`: Order test data

## Coverage Goals

- **State Machine**: 100% coverage (critical business logic)
- **Controllers**: 90%+ coverage
- **Services**: 90%+ coverage
- **Overall**: 85%+ coverage

## Best Practices

1. **Isolation**: Each test is independent
2. **Naming**: Descriptive test names explaining what is tested
3. **AAA Pattern**: Arrange, Act, Assert
4. **Mocking**: Mock external dependencies
5. **Async**: Use `@pytest.mark.asyncio` for async tests

## CI/CD Integration

Tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=app --cov-report=xml
```

## Troubleshooting

### Tests failing with database errors

Make sure you're using the test database, not production:
```python
# conftest.py uses in-memory SQLite
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
```

### Import errors

Make sure you're running from the Backend directory:
```bash
cd Backend
pytest
```

### Async warnings

Make sure `pytest-asyncio` is installed:
```bash
pip install pytest-asyncio
```

## Adding New Tests

### 1. Add test file

```bash
touch tests/test_new_feature.py
```

### 2. Import necessary modules

```python
import pytest
from httpx import AsyncClient
```

### 3. Create test class

```python
class TestNewFeature:
    @pytest.mark.asyncio
    async def test_something(self, client):
        response = await client.get("/endpoint")
        assert response.status_code == 200
```

### 4. Run new tests

```bash
pytest tests/test_new_feature.py -v
```

## Continuous Testing

For development, use pytest-watch:

```bash
pip install pytest-watch
ptw -- -v
```

This will automatically rerun tests when files change.
