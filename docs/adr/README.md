# Architecture Decision Records (ADR)

This directory contains Architecture Decision Records (ADRs) for the wonderland project. Each ADR documents a significant architectural decision made during the project's development.

## What is an ADR?

An Architecture Decision Record (ADR) is a document that captures an important architectural decision made along with its context and consequences.

## ADR Template

See [0000-template.md](0000-template.md) for the template used to create new ADRs.

## List of ADRs

| № | Title | Status |
|---|-------|--------|
| [0000](0000-template.md) | Template | - |
| [0001](0001-context.md) | Передача сущностей в ручку | Частично реализовано |
| [0002](0002-access_handler.md) | Ограничения доступа (Только для админов) | Принято |
| [0003](0003-database-choice.md) | Выбор базы данных и ORM | Принято |
| [0004](0004-deployment-strategy.md) | Стратегия развертывания | Предложено |
| [0005](0005-error-handling.md) | Обработка ошибок и логирование | Принято |
| [0006](0006-api-structure.md) | Структура API | Принято |
| [0007](0007-testing-strategy.md) | Стратегия тестирования | Предложено |
| [0008](0008-ci-cd.md) | Стратегия CI/CD | Предложено |
| [0009](0009-authentication-library-choice.md) | Выбор библиотеки аутентификации | Принято |
| [0010](0010-caching-strategy.md) | Стратегия кэширования | Предложено |
| [0011](0011-message-queue-choice.md) | Выбор очереди сообщений | Принято |

## Status Definitions

- **Предложено** — решение находится на стадии обсуждения
- **Принято** — решение утверждено и применяется
- **Отклонено** — обсуждалось, но не принято
- **Устарело** — всё ещё используется, но больше не рекомендуется
- **Заменено** — это решение было заменено другим ADR
- **Неактуально** — полностью устарело, более не применяется
- **Реализовано** — принято и полностью внедрено
- **Отложено** — обсуждение или внедрение заморожено

## Project Architecture Overview

The wonderland project follows a modular architecture with clear separation of concerns:

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