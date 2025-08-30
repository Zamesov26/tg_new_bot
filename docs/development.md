# Development Guide

## Overview

This guide provides information for developers working on the wonderland project. It covers the project structure, development environment setup, coding standards, and contribution guidelines.

## Project Structure

```
.
├── app/                    # Main aiohttp application
│   ├── bot_engine/        # Telegram bot engine
│   ├── tg_api/            # Telegram API accessor
│   ├── database/          # Database configuration
│   ├── store/             # Component store and accessors
│   ├── web/               # Web application components
│   ├── users/             # User management
│   ├── programs/          # Program management
│   ├── questionnaire/     # Questionnaire system
│   ├── fsm/               # Finite State Machine
│   ├── admin/             # Admin functionality
│   ├── medias/            # Media management
│   ├── promo/             # Promotion management
│   ├── wonderland/        # Business logic
│   ├── base/              # Base classes
│   ├── actions/           # Action handlers
│   ├── pagination/        # Pagination utilities
│   ├── templates/         # Templates
│   ├── utils/             # Utility functions
│   ├── config.py          # Configuration loader
│   └── __init__.py        # Package initialization
├── admin_panel/           # Django admin panel
│   ├── admin_panel/       # Django settings
│   ├── programs/          # Program management
│   ├── medias/            # Media management
│   ├── promos/            # Promotion management
│   ├── questionare/       # Questionnaire management
│   ├── users/             # User management
│   ├── shared/            # Shared components
│   └── manage.py          # Django management script
├── docs/                  # Documentation
│   ├── adr/               # Architecture Decision Records
│   ├── dr/                # Document Records (Technical Debt)
│   ├── analysis/          # Analysis and research
│   ├── api.md             # API documentation
│   ├── deployment.md      # Deployment guide
│   ├── user_guide.md      # User guide
│   ├── development.md     # Development guide
│   ├── testing.md         # Testing guide
│   └── CHANGELOG.md       # Change log
├── migrations/            # Database migrations
├── etc/                   # Configuration files
├── tests/                 # Test files (TODO)
├── main.py                # Main application entry point
├── pyproject.toml         # Poetry configuration
├── requirements.txt       # Dependencies
├── README.md              # Project README
└── Makefile              # Build automation
```

## Development Environment Setup

### Prerequisites

- Python 3.12+
- PostgreSQL 13+
- Redis (optional)
- Poetry (for dependency management)

### Setting Up the Environment

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd wonderland
   ```

2. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**:
   ```bash
   poetry install
   ```

4. **Activate the virtual environment**:
   ```bash
   poetry shell
   ```

5. **Set up the database**:
   - Install PostgreSQL
   - Create a database and user
   - Update `etc/config.yml` with database credentials

6. **Run migrations**:
   ```bash
   alembic upgrade head
   ```

### Configuration

Create a development configuration file at `etc/config.yml`:

```yaml
debug: true
database:
  host: localhost
  port: 5432
  user: postgres
  password: postgres
  database: sveta_dev
web:
  host: 127.0.0.1
  port: 8000
bot:
  token: YOUR_DEV_BOT_TOKEN
session:
  key: YOUR_SESSION_KEY
admin:
  email: admin@admin.com
  password: admin
sentry:
  dsn:
  env: dev
```

## Coding Standards

### Python Standards

The project follows PEP 8 coding standards with some additional conventions:

1. **Line Length**: Maximum 80 characters
2. **Naming Conventions**:
   - Variables and functions: `snake_case`
   - Classes: `PascalCase`
   - Constants: `UPPER_SNAKE_CASE`
3. **Type Hints**: Required for all function signatures
4. **Docstrings**: Google style docstrings for all public functions and classes

### Code Structure

1. **Modular Design**: Each feature should be in its own module
2. **Separation of Concerns**: Business logic separated from data access
3. **Dependency Injection**: Components should receive dependencies rather than creating them
4. **Error Handling**: Proper exception handling with meaningful error messages

### SQLAlchemy Models

1. **Model Structure**: Use SQLAlchemy 2.0 style with mapped_column
2. **Relationships**: Define relationships explicitly
3. **Constraints**: Add appropriate database constraints
4. **Indexes**: Add indexes for frequently queried fields

### Testing

1. **Test Organization**: Tests should mirror the source code structure
2. **Test Types**: Unit tests, integration tests, and end-to-end tests
3. **Test Coverage**: Aim for >80% code coverage
4. **Test Data**: Use factories or fixtures for test data

## Development Workflow

### Feature Development

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Implement the feature** following coding standards

3. **Write tests** for new functionality

4. **Run tests**:
   ```bash
   pytest
   ```

5. **Check code quality**:
   ```bash
   ruff check .
   ```

6. **Commit changes** with descriptive messages:
   ```bash
   git commit -m "Add feature: description of what was added"
   ```

7. **Push and create a pull request**

### Database Migrations

When making changes to database models:

1. **Create a migration**:
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   ```

2. **Review the generated migration** file in `migrations/versions/`

3. **Apply the migration**:
   ```bash
   alembic upgrade head
   ```

4. **Test the migration** in a development environment

### Code Review Process

1. **Pull Request Requirements**:
   - All tests must pass
   - Code must follow coding standards
   - Adequate test coverage
   - Clear commit messages
   - Updated documentation if needed

2. **Review Checklist**:
   - Code correctness
   - Performance considerations
   - Security implications
   - Maintainability
   - Documentation updates

## Component Architecture

### Store Pattern

The application uses a "store" pattern for component management:

```python
class Store:
    def __init__(self, app: "Application"):
        self.tg_api = TgApiAccessor(app)
        self.bot_manager = BotManager(app)
        self.user = UserAccessor(app)
        # ... other accessors
```

Each accessor is responsible for a specific domain or functionality.

### Accessor Pattern

Accessors provide a clean interface to domain-specific functionality:

```python
class UserAccessor(BaseAccessor):
    async def get_user(self, user_id: int) -> User:
        # Implementation
        pass
    
    async def create_user(self, data: dict) -> User:
        # Implementation
        pass
```

### Event Handling

The bot uses an event-driven architecture:

```python
class BotManager:
    async def handle_updates(self, update: "Update"):
        # Process update through handlers
        pass
```

Handlers are registered and checked in order to process updates.

## Testing Strategy

### Test Structure

```
tests/
├── unit/
│   ├── test_accessors/
│   ├── test_handlers/
│   └── test_models/
├── integration/
│   ├── test_database/
│   ├── test_telegram_api/
│   └── test_bot_flows/
└── conftest.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test module
pytest tests/unit/test_accessors/

# Run with coverage
pytest --cov=app

# Run tests in parallel
pytest -n auto
```

### Writing Tests

Use pytest with async support:

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_user_accessor_get_user():
    # Test implementation
    pass
```

## Debugging

### Logging

The application uses Python's logging module:

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message")
```

### Debugging Tools

1. **pdb**: Python debugger for stepping through code
2. **logging**: Detailed logging for tracing execution
3. **print statements**: Temporary debugging output (remove before commit)

### Common Debugging Scenarios

1. **Telegram API Issues**:
   - Check bot token
   - Verify webhook/polling configuration
   - Examine API response logs

2. **Database Issues**:
   - Check connection parameters
   - Verify migrations are applied
   - Examine query performance

3. **Performance Issues**:
   - Profile slow functions
   - Check database query performance
   - Monitor memory usage

## Contributing

### How to Contribute

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Write tests
5. Update documentation
6. Submit a pull request

### Pull Request Guidelines

1. **Description**: Clear description of changes
2. **Tests**: Include tests for new functionality
3. **Documentation**: Update relevant documentation
4. **Code Review**: Address all review comments
5. **CI**: Ensure all CI checks pass

### Reporting Issues

1. **Check existing issues** before creating a new one
2. **Provide detailed information**:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details
3. **Include logs** if relevant
4. **Use labels** to categorize issues

## Release Process

### Versioning

The project follows Semantic Versioning (SemVer):
- MAJOR version for incompatible API changes
- MINOR version for backward-compatible functionality
- PATCH version for backward-compatible bug fixes

### Release Steps

1. **Update version** in `VERSION` file
2. **Update CHANGELOG.md**
3. **Create git tag**:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```
4. **Build and deploy** to production

## Tools and Utilities

### Development Tools

1. **Ruff**: Code linting and formatting
2. **Black**: Code formatting
3. **Pytest**: Testing framework
4. **Alembic**: Database migrations
5. **Poetry**: Dependency management

### Useful Commands

```bash
# Format code
ruff format .

# Check code quality
ruff check .

# Run tests
pytest

# Run tests with coverage
pytest --cov=app

# Generate migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Downgrade migrations
alembic downgrade -1
```