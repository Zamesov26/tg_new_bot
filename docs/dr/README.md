# Document Records (DR)

This directory contains unified Document Records (DRs) for the sveta_bot project. Each DR combines Problem Description Records (PDR) and Technical Debt Records (TDR) into a single comprehensive document.

## What is a DR?

A Document Record (DR) is a unified document that captures either:
1. A significant problem affecting maintainability, performance, security, or clarity of the system
2. A technical debt item that needs to be addressed
3. A combination of both when they refer to the same issue

## List of DRs

| № | Заголовок | Категория | Статус |
|---|-----------|-----------|--------|
| [DR-0001](DR-0001.md) | Отключение проверки SSL-сертификатов | Безопасность | Open |
| [DR-0002](DR-0002.md) | Хардкодинг секретов в коде | Безопасность | Open |
| [DR-0003](DR-0003.md) | Незакрытые файловые дескрипторы | Ресурсы | Open |
| [DR-0004](DR-0004.md) | Большой монолитный класс TgApiAccessor | Архитектура | Open |
| [DR-0005](DR-0005.md) | Отсутствие автоматизированных тестов | Качество | Open |
| [DR-0006](DR-0006.md) | Недостаточная обработка исключений | Стабильность | Open |
| [DR-0007](DR-0007.md) | Потенциальные проблемы с производительностью при работе с БД | Производительность | Open |
| [DR-0008](DR-0008.md) | Дублирование кода для построения URL запросов | Поддержка | Open |
| [DR-0009](DR-0009.md) | Недостаточная документация и комментарии в коде | Поддержка | Open |
| [DR-0010](DR-0010.md) | Недостаточная типизация | Качество | Open |
| [DR-0011](DR-0011.md) | Неиспользуемые зависимости и потенциально ненужные компоненты | Поддержка | Open |
| [DR-0012](DR-0012.md) | Несоответствия в коде и потенциальные баги | Качество | Open |
| [DR-0013](DR-0013.md) | Множество незавершенных задач (TODO-комментариев) | Технический долг | Open |

## Problem Categories

- **Безопасность** - Проблемы, связанные с уязвимостями и защитой данных
- **Ресурсы** - Проблемы с управлением системными ресурсами
- **Архитектура** - Проблемы с архитектурой и структурой кода
- **Качество** - Проблемы с качеством кода и тестированием
- **Технический долг** - Накопленные проблемы, требующие решения
- **Стабильность** - Проблемы со стабильностью работы приложения
- **Поддержка** - Проблемы, затрудняющие поддержку кода
- **Производительность** - Проблемы, влияющие на быстродействие приложения

## Status Definitions

- **Open** - Проблема идентифицирована и задокументирована
- **Closed** - Проблема решена (файлы перемещаются в /closed/)

## Project Context

The sveta_bot project is a Telegram bot application built with Python, aiohttp, and Django. It provides functionality for:
- Managing programs and events
- Handling user bookings and registrations
- Providing interactive FAQ and promotional materials
- Administering content through a Django admin panel

The project currently faces several technical challenges that are documented in these DRs. Addressing these issues will improve the overall quality, security, and maintainability of the application.

## Prioritization Guidelines

When addressing DRs, consider the following prioritization:

1. **Security issues** (DR-0001, DR-0002) - Highest priority
2. **Stability issues** (DR-0006) - High priority
3. **Architecture issues** (DR-0004) - High priority
4. **Performance issues** (DR-0007) - Medium priority
5. **Quality issues** (DR-0005, DR-0010, DR-0012) - Medium priority
6. **Documentation issues** (DR-0009) - Medium priority
7. **Maintenance issues** (DR-0003, DR-0008, DR-0011, DR-0013) - Lower priority