# Project Documentation

## Project Overview

**sveta_bot** is a Telegram bot application built with Python, aiohttp, and Django. The project provides a comprehensive solution for managing programs, handling user bookings, and interacting with users through Telegram. It features both a Telegram bot interface for end users and a Django admin panel for content management.

### Key Features
- Telegram bot with interactive navigation menu
- Program management and information display
- Booking system for user participation
- FAQ and promotional materials
- User management with role-based access control
- Django admin panel for content management
- PostgreSQL database with SQLAlchemy ORM
- Alembic for database migrations

## Architecture

The project follows a modular architecture with clear separation of concerns:

### Core Components

1. **Telegram Bot Engine** (`app/bot_engine/`)
   - Handles incoming updates from Telegram
   - Manages the update processing queue
   - Routes updates to appropriate handlers

2. **Telegram API Accessor** (`app/tg_api/`)
   - Provides interface to Telegram Bot API
   - Handles message sending, media operations, and callback queries
   - Implements polling mechanism for receiving updates

3. **Web Application** (`app/web/`)
   - Built with aiohttp for asynchronous web handling
   - Contains custom Application, Request, and View classes
   - Integrates all components together

4. **Database Layer** (`app/database/`)
   - Uses SQLAlchemy 2.0 with asyncpg for PostgreSQL
   - Implements async session management
   - Provides base model class for all entities

5. **Store Layer** (`app/store/`)
   - Centralized access point for all application components
   - Contains accessors for each domain entity
   - Manages component lifecycle (start/stop)

6. **Domain Modules**
   - **Users** (`app/users/`): User management and authentication
   - **Programs** (`app/programs/`): Program catalog and management
   - **Media** (`app/medias/`): Media content handling
   - **Promotions** (`app/promo/`): Promotional materials
   - **Questionnaire** (`app/questionnaire/`): User questionnaire system
   - **FSM** (`app/fsm/`): Finite State Machine for user states
   - **Admin** (`app/admin/`): Administrative user management

7. **Admin Panel** (`admin_panel/`)
   - Django-based web interface for content management
   - Separate apps for users, programs, media, promotions, and questionnaires
   - Uses the same database as the main application

### Data Flow

1. Telegram sends updates to the bot via webhooks or polling
2. TgApiAccessor receives and validates updates
3. BotManager queues updates and processes them asynchronously
4. Handlers process updates based on business logic
5. Database accessors handle data persistence/retrieval
6. Responses are sent back through the Telegram API

## Setup & Installation

### Prerequisites
- Python 3.12+
- PostgreSQL database
- Redis (optional, for caching)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd sveta_bot
   ```

2. **Install dependencies:**
   ```bash
   # Using poetry (recommended)
   poetry install
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Configure the application:**
   ```bash
   # Copy the example config and update with your settings
   cp etc/exapmple.config.yml etc/config.yml
   # Edit etc/config.yml with your database credentials, bot token, etc.
   ```

4. **Set up the database:**
   ```bash
   # Create the database in PostgreSQL
   # Update etc/config.yml with your database settings
   
   # Apply migrations
   alembic upgrade head
   ```

### Running the Application

1. **Start the Telegram bot:**
   ```bash
   python main.py
   ```

2. **Start the admin panel:**
   ```bash
   cd admin_panel
   python manage.py runserver
   ```

## Configuration

### Configuration File

The application uses a YAML configuration file located at `etc/config.yml`. An example configuration is provided in `etc/exapmple.config.yml`.

#### Example Configuration:
```yaml
debug: true
database:
  host: localhost
  port: 5432
  user: postgres 
  password: postgres
  database: sveta
web:
  host: 127.0.0.1
  port: 8000
bot:
  token: YOUR_TELEGRAM_BOT_TOKEN
session:
  key: SESSION_SECRET_KEY
admin:
  email: admin@admin.com
  password: admin
sentry:
  dsn:
  env: dev

store: {}
```

### Environment Variables
The application currently does not use environment variables for configuration but relies on the YAML config file.

## Usage

### Starting the Bot
```python
import os
from aiohttp.web import run_app
from app.web.app import setup_app

if __name__ == "__main__":
    run_app(
        setup_app(
            config_path=os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "etc/config.yml"
            )
        )
    )
```

### Working with Telegram API
```python
# Send a message through the accessor
async def send_welcome_message(chat_id, text):
    await app.store.tg_api.send_message(chat_id=chat_id, text=text)
```

### Database Operations
```python
# Get user data through the accessor
async def get_user(user_id):
    async with app.database.session() as session:
        user = await session.get(UserModel, user_id)
        return user
```

### Admin Panel
The Django admin panel provides a web interface for managing:
- Programs
- Media content
- Promotional materials
- Users
- Questionnaires

Access it at `http://localhost:8000/admin/` after starting the server.

## Testing

### Current State
The project currently lacks a comprehensive test suite. The README mentions tests as a TODO item.

### Recommended Testing Approach

1. **Unit Tests** for individual components:
   - Test accessors in isolation
   - Test business logic in handlers
   - Test data models

2. **Integration Tests** for component interactions:
   - Test database operations
   - Test Telegram API interactions
   - Test end-to-end bot flows

3. **Test Structure**:
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
Once tests are implemented:
```bash
# Run all tests
pytest

# Run specific test module
pytest tests/unit/test_accessors/

# Run with coverage
pytest --cov=app
```

## Best Practices & Recommendations

### Code Quality
1. **Follow PEP 8** coding standards
2. **Use type hints** for all function signatures and variable declarations
3. **Implement proper error handling** with try/except blocks
4. **Use logging** instead of print statements
5. **Write docstrings** for all public functions and classes

### Architecture Improvements
1. **Separate concerns** more clearly between components
2. **Implement dependency injection** for better testability
3. **Use interfaces/abstract classes** for component contracts
4. **Implement proper validation** for all inputs
5. **Add caching layer** with Redis for frequently accessed data

### Security
1. **Validate all user inputs** to prevent injection attacks
2. **Use environment variables** for sensitive configuration
3. **Implement rate limiting** for API endpoints
4. **Use HTTPS** in production
5. **Regularly update dependencies** to patch vulnerabilities

### Performance
1. **Use database connection pooling**
2. **Implement caching** for expensive operations
3. **Use asynchronous operations** wherever possible
4. **Optimize database queries** with proper indexing
5. **Monitor resource usage** in production

### Development Workflow
1. **Use feature branches** for new functionality
2. **Write tests** before implementing features
3. **Follow semantic versioning** for releases
4. **Document API changes** in changelog
5. **Use code reviews** for all pull requests

## TODOs / Known Issues

### Critical Missing Features
- [ ] Implement comprehensive test suite
- [ ] Add proper caching with Redis
- [ ] Implement CI/CD pipeline
- [ ] Add monitoring and logging infrastructure
- [ ] Address technical debt (see docs/tdr/)
- [ ] Add API documentation
- [ ] Create user guide
- [ ] Implement notification system
- [ ] Add multilingual support

### Code Quality Issues
- [ ] Fix TODO comments in store/store.py regarding unnecessary accessors
- [ ] Refactor TgApiAccessor to use facade pattern as noted in TODO
- [ ] Remove unused `_build_query` method in TgApiAccessor
- [ ] Improve error handling in Telegram API interactions
- [ ] Add proper validation for configuration loading

### Technical Debt
- [ ] Address issues documented in docs/tdr/
- [ ] Refactor session management (currently commented out in config.py)
- [ ] Improve database model relationships and constraints
- [ ] Optimize database queries for better performance
- [ ] Add proper input sanitization for user-generated content

### Documentation Gaps
- [ ] Complete API documentation
- [ ] Create comprehensive user guide
- [ ] Add deployment instructions for production
- [ ] Document admin panel usage
- [ ] Create architecture diagrams
- [ ] Add troubleshooting guide

### Future Enhancements
- [ ] Implement webhook support for Telegram updates (more efficient than polling)
- [ ] Add user analytics and reporting
- [ ] Implement backup and recovery procedures
- [ ] Add support for multiple bots
- [ ] Create mobile-friendly admin interface
- [ ] Implement user feedback system
- [ ] Add integration with payment systems