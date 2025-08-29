# sveta_bot

Telegram-бот для управления программами, бронированием и взаимодействием с пользователями.

## Описание

sveta_bot - это Telegram-бот, разработанный на Python с использованием aiohttp и Django. Проект предназначен для автоматизации взаимодействия с пользователями через Telegram, управления программами, обработки бронирований и администрирования контента через веб-интерфейс.

Бот предоставляет пользователям возможность:
- Просматривать доступные программы
- Получать информацию о программах
- Оставлять заявки на участие
- Получать обратную связь
- Работать с FAQ и промо-материалами

## Функциональность

- **Telegram-бот**:
  - Интерактивное меню навигации
  - Просмотр программ и деталей
  - Система бронирования
  - Обратная связь от пользователей
  - FAQ раздел
  - Промо-функциональность
  - Управление администраторами

- **Админ-панель (Django)**:
  - Управление программами
  - Управление медиа-контентом
  - Управление промо-материалами
  - Управление пользователями
  - Управление анкетами

- **База данных**:
  - Хранение информации о пользователях
  - Хранение программ и медиа
  - Управление бронированиями
  - Система FSM (Finite State Machine) для состояний пользователей

- **Интеграции**:
  - PostgreSQL для хранения данных
  - Redis для кэширования

## Структура проекта

```
.
├── app/                    # Основное приложение aiohttp
│   ├── bot_engine/        # Движок Telegram-бота
│   ├── tg_api/            # Работа с Telegram API
│   ├── database/          # Работа с базой данных
│   ├── store/             # Хранилище аксессоров
│   ├── web/               # Веб-приложение aiohttp
│   ├── users/             # Управление пользователями
│   ├── programs/          # Управление программами
│   ├── questionnaire/     # Анкетирование
│   ├── fsm/               # Машина состояний
│   └── wonderland/        # Бизнес-логика бота
├── admin_panel/           # Админ-панель Django
│   ├── programs/          # Управление программами
│   ├── medias/            # Управление медиа
│   ├── promos/            # Промо-материалы
│   └── users/             # Управление пользователями
├── docs/
│   ├── adr/              # Architecture Decision Records
│   └── tdr/              # Technical Debt Records
├── migrations/            # Миграции базы данных
├── etc/                  # Конфигурационные файлы
└── tests/                # Тесты (TODO: Создать структуру тестов)
```

## Установка и запуск

### Требования

- Python 3.12+
- PostgreSQL
- Redis (опционально)

### Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd sveta_bot
```

2. Установите зависимости:
```bash
# С использованием poetry (рекомендуется)
poetry install

# Или с использованием pip
pip install -r requirements.txt
```

3. Настройте базу данных PostgreSQL и обновите конфигурацию в `etc/config.yml`

4. Примените миграции:
```bash
alembic upgrade head
```

### Запуск

1. Запуск Telegram-бота:
```bash
python main.py
```

2. Запуск админ-панели Django:
```bash
cd admin_panel
python manage.py runserver
```

## Примеры использования

### Запуск бота

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

### Работа с Telegram API

```python
# Отправка сообщения через аксессор
async def send_welcome_message(chat_id, text):
    await app.store.tg_api.send_message(chat_id=chat_id, text=text)
```

### Работа с базой данных

```python
# Получение данных через аксессор
async def get_user(user_id):
    async with app.database.session() as session:
        user = await session.get(UserModel, user_id)
        return user
```

## Документация

- [Architecture Decision Records (ADR)](docs/adr/README.md) - Документы архитектурных решений
- [Technical Debt Records (TDR)](docs/tdr/README.md) - Записи технического долга
- [API Documentation] - TODO: Добавить документацию API
- [User Guide] - TODO: Добавить руководство пользователя

## Планы развития / TODO

- [ ] Реализовать полноценную систему тестирования
- [ ] Добавить кэширование с использованием Redis
- [ ] Реализовать полноценный CI/CD pipeline
- [ ] Добавить мониторинг и логирование
- [ ] Улучшить безопасность (устранить технический долг)
- [ ] Добавить документацию API
- [ ] Создать руководство пользователя
- [ ] Реализовать систему уведомлений
- [ ] Добавить поддержку多язычности

## Авторы / Контрибьюторы

- Замесов Олег Константинович
  - email: o.zamesov@yandex.ru
  - telegram: @Zamesov

## Лицензия

TODO: Определить и добавить информацию о лицензии