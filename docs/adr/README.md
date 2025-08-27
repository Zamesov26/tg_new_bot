# Architecture Decision Records (ADR)

This directory contains Architecture Decision Records (ADRs) for the sveta_bot project. Each ADR documents a significant architectural decision made during the project's development.

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

## Statuses

- **Предложено** — решение находится на стадии обсуждения
- **Принято** — решение утверждено и применяется
- **Отклонено** — обсуждалось, но не принято
- **Устарело** — всё ещё используется, но больше не рекомендуется
- **Заменено** — это решение было заменено другим ADR
- **Неактуально** — полностью устарело, более не применяется
- **Реализовано** — принято и полностью внедрено
- **Отложено** — обсуждение или внедрение заморожено