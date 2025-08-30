# Testing Guide

## Overview

This document describes the testing strategy, tools, and practices for the wonderland project. The project currently lacks a comprehensive test suite, which is documented as a technical debt item (DR-0005).

## Current State

The project has no formal test suite implemented. Tests are listed as a TODO item in the project documentation.

## Testing Strategy

### Test Types

1. **Unit Tests**: Test individual functions and classes in isolation
2. **Integration Tests**: Test interactions between components
3. **End-to-End Tests**: Test complete user workflows
4. **Regression Tests**: Ensure bugs don't reappear

### Test Organization

```
tests/
├── unit/
│   ├── test_accessors/
│   │   ├── test_user_accessor.py
│   │   ├── test_program_accessor.py
│   │   └── test_tg_api_accessor.py
│   ├── test_handlers/
│   │   ├── test_message_handlers.py
│   │   └── test_callback_handlers.py
│   ├── test_models/
│   │   ├── test_user_model.py
│   │   └── test_program_model.py
│   └── test_utils/
│       └── test_helpers.py
├── integration/
│   ├── test_database/
│   │   ├── test_user_operations.py
│   │   └── test_program_operations.py
│   ├── test_telegram_api/
│   │   └── test_api_interactions.py
│   └── test_bot_flows/
│       └── test_user_journeys.py
├── e2e/
│   └── test_scenarios/
│       ├── test_program_browsing.py
│       └── test_booking_flow.py
└── conftest.py
```

## Testing Tools

### Primary Tools

1. **pytest**: Testing framework
2. **pytest-asyncio**: Async support for pytest
3. **pytest-aiohttp**: aiohttp testing utilities
4. **unittest.mock**: Mocking library
5. **coverage.py**: Code coverage measurement

### Installation

Testing dependencies are included in `pyproject.toml`:

```toml
[tool.poetry.group.dev.dependencies]
pytest = "8.0.2"
pytest-aiohttp = "1.0.5"
pytest-asyncio = "0.23.5"
```

## Writing Tests

### Unit Tests

Unit tests should focus on testing individual functions and methods in isolation.

#### Example Unit Test

```python
import pytest
from unittest.mock import AsyncMock, Mock
from app.users.accessor import UserAccessor
from app.users.models import User

@pytest.mark.asyncio
async def test_user_accessor_get_user():
    # Arrange
    app = Mock()
    accessor = UserAccessor(app)
    accessor.app.database.session = AsyncMock()
    
    # Mock database response
    mock_user = User(
        id=1,
        tg_id=123456789,
        first_name="Test",
        last_name="User"
    )
    accessor.app.database.session.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_user)
    
    # Act
    result = await accessor.get_user(1)
    
    # Assert
    assert result.id == 1
    assert result.tg_id == 123456789
    assert result.first_name == "Test"
    assert result.last_name == "User"
```

### Integration Tests

Integration tests should test how components work together.

#### Example Integration Test

```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.models import User
from app.users.accessor import UserAccessor

@pytest.mark.asyncio
async def test_user_creation_integration(db_session: AsyncSession):
    # Arrange
    app = Mock()
    app.database.session = lambda: db_session
    accessor = UserAccessor(app)
    
    user_data = {
        "tg_id": 987654321,
        "first_name": "Integration",
        "last_name": "Test"
    }
    
    # Act
    user = await accessor.create_user(user_data)
    
    # Assert
    assert user.tg_id == 987654321
    assert user.first_name == "Integration"
    
    # Verify in database
    db_user = await db_session.get(User, user.id)
    assert db_user is not None
    assert db_user.tg_id == 987654321
```

### End-to-End Tests

E2E tests should simulate real user interactions.

#### Example E2E Test

```python
import pytest
from unittest.mock import AsyncMock
from app.bot_engine.manager import BotManager
from app.tg_api.models import Update, Message, Chat, User as TgUser

@pytest.mark.asyncio
async def test_start_command_flow():
    # Arrange
    app = Mock()
    app.store = Mock()
    app.store.tg_api = AsyncMock()
    app.store.user = AsyncMock()
    
    bot_manager = BotManager(app)
    
    # Mock update
    update = Update(
        update_id=1,
        message=Message(
            message_id=1,
            from_user=TgUser(id=123456789, is_bot=False, first_name="Test"),
            chat=Chat(id=123456789, type="private"),
            date=1234567890,
            text="/start"
        )
    )
    
    # Act
    await bot_manager.handle_updates(update)
    
    # Assert
    # Verify that welcome message was sent
    app.store.tg_api.send_message.assert_called_once()
```

## Test Fixtures

### Database Fixtures

```python
# conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database.sqlalchemy_base import BaseModel

@pytest.fixture
async def db_engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def db_session(db_engine):
    async_session = sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
```

### Application Fixtures

```python
@pytest.fixture
def mock_app():
    app = Mock()
    app.config = Mock()
    app.database = Mock()
    app.store = Mock()
    return app
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run tests in a specific directory
pytest tests/unit/

# Run a specific test file
pytest tests/unit/test_accessors/test_user_accessor.py

# Run a specific test function
pytest tests/unit/test_accessors/test_user_accessor.py::test_user_accessor_get_user
```

### Test with Coverage

```bash
# Run tests with coverage report
pytest --cov=app

# Generate HTML coverage report
pytest --cov=app --cov-report=html

# Run tests with coverage and show missing lines
pytest --cov=app --cov-report=term-missing
```

### Parallel Test Execution

```bash
# Run tests in parallel (requires pytest-xdist)
pytest -n auto
```

### Test Selection

```bash
# Run only failed tests
pytest --lf

# Run tests matching a pattern
pytest -k "user"

# Run tests with specific markers
pytest -m "asyncio"
```

## Test Configuration

### pytest.ini

```ini
[tool.pytest.ini_options]
asyncio_mode = "auto"
filterwarnings = [
    "ignore::DeprecationWarning:asyncpg.*:",
    "ignore::DeprecationWarning:pytest_asyncio.plugin.*:",
    "ignore::DeprecationWarning",
]
markers = [
    "asyncio: marks tests as asyncio",
    "integration: marks tests as integration tests",
    "e2e: marks tests as end-to-end tests",
]
```

### pyproject.toml

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
filterwarnings = [
  "ignore::DeprecationWarning:asyncpg.*:",
  "ignore::DeprecationWarning:pytest_asyncio.plugin.*:",
  "ignore::DeprecationWarning",
]

[tool.coverage.run]
source = ["app"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/venv/*",
    "*/.venv/*",
]
```

## Mocking Strategies

### Mocking External APIs

```python
from unittest.mock import AsyncMock, patch

@patch('app.tg_api.accessor.ClientSession')
@pytest.mark.asyncio
async def test_send_message(mock_session_class):
    # Arrange
    mock_session = AsyncMock()
    mock_session_class.return_value = mock_session
    mock_session.get.return_value.__aenter__.return_value.json = AsyncMock(
        return_value={"ok": True, "result": {"message_id": 1}}
    )
    
    # Act & Assert
    # Test implementation
```

### Mocking Database Operations

```python
from unittest.mock import AsyncMock

def test_user_accessor_with_mocked_db():
    app = Mock()
    app.database.session = AsyncMock()
    
    # Mock the async context manager
    mock_session = AsyncMock()
    app.database.session.return_value.__aenter__.return_value = mock_session
    
    # Mock database operations
    mock_session.get.return_value = AsyncMock()
```

## Continuous Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.12]
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install poetry
        poetry install
    
    - name: Run tests
      run: |
        poetry run pytest --cov=app
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## Test Data Management

### Factory Pattern

```python
# tests/factories.py
from app.users.models import User
from app.programs.models import Programs

class UserFactory:
    @staticmethod
    def create(**kwargs):
        defaults = {
            "tg_id": 123456789,
            "first_name": "Test",
            "last_name": "User",
        }
        defaults.update(kwargs)
        return User(**defaults)

class ProgramFactory:
    @staticmethod
    def create(**kwargs):
        defaults = {
            "title": "Test Program",
            "price": 100.00,
            "description": "Test program description",
        }
        defaults.update(kwargs)
        return Programs(**defaults)
```

### Test Data Fixtures

```python
@pytest.fixture
def sample_user():
    return UserFactory.create()

@pytest.fixture
def sample_program():
    return ProgramFactory.create()
```

## Performance Testing

### Load Testing

For testing the bot under load, consider using tools like:

1. **Locust**: Python-based load testing tool
2. **Artillery**: Node.js based load testing toolkit

### Example Load Test

```python
# load_test.py
from locust import HttpUser, task, between

class TelegramBotUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def send_message(self):
        self.client.post("/webhook", json={
            "update_id": 1,
            "message": {
                "message_id": 1,
                "from": {"id": 123456789, "is_bot": False, "first_name": "Test"},
                "chat": {"id": 123456789, "type": "private"},
                "date": 1234567890,
                "text": "/start"
            }
        })
```

## Best Practices

### Test Design

1. **Arrange-Act-Assert**: Follow the AAA pattern
2. **Descriptive Names**: Use clear, descriptive test names
3. **Isolation**: Each test should be independent
4. **Speed**: Tests should run quickly
5. **Reliability**: Tests should produce consistent results

### Code Coverage

1. **Target**: Aim for >80% code coverage
2. **Quality over Quantity**: Focus on meaningful test coverage
3. **Edge Cases**: Test boundary conditions and error cases
4. **Happy Path**: Test the main success scenario

### Maintenance

1. **Regular Cleanup**: Remove obsolete tests
2. **Refactoring**: Keep tests updated with code changes
3. **Documentation**: Comment complex test setups
4. **Review**: Include tests in code reviews

## Common Testing Patterns

### Parameterized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("valid_data", True),
    ("invalid_data", False),
    ("edge_case", True),
])
def test_data_validation(input, expected):
    result = validate_data(input)
    assert result == expected
```

### Test Suites

```python
@pytest.mark.parametrize("user_role", ["admin", "user", "restricted"])
class TestUserPermissions:
    def test_can_view_programs(self, user_role):
        # Test implementation
        pass
    
    def test_can_book_programs(self, user_role):
        # Test implementation
        pass
```

## Troubleshooting

### Common Issues

1. **Async Test Failures**: Ensure proper async/await usage
2. **Database Isolation**: Use transactions or fresh databases per test
3. **Mock Issues**: Verify mock configurations match actual implementations
4. **Test Order Dependencies**: Ensure tests are truly independent

### Debugging Tests

```bash
# Run tests with verbose output
pytest -v

# Run tests with print statements
pytest -s

# Run tests and stop on first failure
pytest -x

# Run tests with traceback
pytest --tb=long
```

## Future Improvements

### Test Automation

1. **CI/CD Integration**: Automate test execution on every commit
2. **Scheduled Tests**: Run full test suite periodically
3. **Performance Monitoring**: Track test execution times
4. **Flaky Test Detection**: Identify and fix unreliable tests

### Advanced Testing

1. **Contract Testing**: Verify API contracts
2. **Security Testing**: Include security-focused tests
3. **Chaos Engineering**: Test system resilience
4. **A/B Testing**: Test different implementations