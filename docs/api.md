# API Documentation

## Overview

The sveta_bot project has two main API interfaces:

1. **Telegram Bot API** - Used for communication with Telegram users
2. **Admin Panel API** - Django REST API for administrative functions

## Telegram Bot API

The Telegram Bot API is implemented through the `TgApiAccessor` class which provides methods for interacting with the Telegram Bot API.

### Core Methods

#### send_message
Sends a text message to a chat.

```python
async def send_message(
    self, 
    chat_id: int, 
    text: str, 
    reply_markup: InlineKeyboardMarkup | None = None
)
```

Parameters:
- `chat_id` (int): Unique identifier for the target chat
- `text` (str): Text of the message to be sent
- `reply_markup` (InlineKeyboardMarkup, optional): Inline keyboard attached to the message

Returns:
- `Message`: The sent message object

#### send_photo
Sends a photo to a chat.

```python
async def send_photo(
    self,
    chat_id: int,
    path_image: str,
    caption: str | None = None,
    file_id: str | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
)
```

Parameters:
- `chat_id` (int): Unique identifier for the target chat
- `path_image` (str): Path to the image file
- `caption` (str, optional): Photo caption
- `file_id` (str, optional): Telegram file ID of previously uploaded photo
- `reply_markup` (InlineKeyboardMarkup, optional): Inline keyboard attached to the message

#### send_media_group
Sends a group of photos as an album.

```python
async def send_media_group(
    self,
    chat_id: int,
    media_items: list[dict],
    reply_markup: InlineKeyboardMarkup | None = None,
)
```

Parameters:
- `chat_id` (int): Unique identifier for the target chat
- `media_items` (list[dict]): List of media objects to send
- `reply_markup` (InlineKeyboardMarkup, optional): Inline keyboard attached to the message

#### edit_message_text
Edits text and game messages.

```python
async def edit_message_text(
    self,
    text: str,
    message_id: int,
    chat_id: int,
    reply_markup: InlineKeyboardMarkup | None = None,
)
```

Parameters:
- `text` (str): New text of the message
- `message_id` (int): Required if inline_message_id is not specified
- `chat_id` (int): Required if inline_message_id is not specified
- `reply_markup` (InlineKeyboardMarkup, optional): Inline keyboard attached to the message

#### edit_message_caption
Edits captions of messages.

```python
async def edit_message_caption(
    self,
    caption: str,
    message_id: int,
    chat_id: int,
    reply_markup: InlineKeyboardMarkup | None = None,
)
```

Parameters:
- `caption` (str): New caption of the message
- `message_id` (int): Required if inline_message_id is not specified
- `chat_id` (int): Required if inline_message_id is not specified
- `reply_markup` (InlineKeyboardMarkup, optional): Inline keyboard attached to the message

#### delete_message
Deletes a message.

```python
async def delete_message(self, chat_id: int, message_id: int)
```

Parameters:
- `chat_id` (int): Unique identifier for the target chat
- `message_id` (int): Identifier of the message to delete

#### answer_callback_query
Sends answers to callback queries sent from inline keyboards.

```python
async def answer_callback_query(self, callback_query_id: str)
```

Parameters:
- `callback_query_id` (str): Unique identifier for the query to be answered

## Admin Panel API

The admin panel is built with Django and provides a web interface for content management. It doesn't have a traditional REST API but uses Django's admin interface patterns.

### Authentication

Authentication is handled through Django's built-in authentication system. Admin users can log in at `/admin/login/`.

### Endpoints

The admin panel provides CRUD operations for the following entities:

#### Programs
- List: `/admin/programs/program/`
- Add: `/admin/programs/program/add/`
- Change: `/admin/programs/program/[id]/change/`
- Delete: `/admin/programs/program/[id]/delete/`

#### Media
- List: `/admin/medias/media/`
- Add: `/admin/medias/media/add/`
- Change: `/admin/medias/media/[id]/change/`
- Delete: `/admin/medias/media/[id]/delete/`

#### Promotions
- List: `/admin/promos/promo/`
- Add: `/admin/promos/promo/add/`
- Change: `/admin/promos/promo/[id]/change/`
- Delete: `/admin/promos/promo/[id]/delete/`

#### Users
- List: `/admin/users/user/`
- Add: `/admin/users/user/add/`
- Change: `/admin/users/user/[id]/change/`
- Delete: `/admin/users/user/[id]/delete/`

#### Questionnaires
- List: `/admin/questionare/questionnaire/`
- Add: `/admin/questionare/questionnaire/add/`
- Change: `/admin/questionare/questionnaire/[id]/change/`
- Delete: `/admin/questionare/questionnaire/[id]/delete/`

## Data Models

### User Model
```python
class User(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    user_name: Mapped[str] = mapped_column(VARCHAR(32), nullable=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(64))
    last_name: Mapped[str] = mapped_column(VARCHAR(64), nullable=True)
    langue_code: Mapped[str] = mapped_column(VARCHAR(10), nullable=True)
    
    class UserRole(enum.Enum):
        ADMIN = "admin"
        USER = "user"
        RESTRICTED = "restricted"
    
    role: Mapped[UserRole] = mapped_column(
        String(20),
        nullable=True,
        default=UserRole.USER.value,
        server_default=UserRole.USER.value,
    )
```

### Program Model
```python
class Programs(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    short_description: Mapped[str] = mapped_column(Text, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
```

## Error Handling

The API follows standard error handling patterns:

- HTTP status codes for REST API responses
- Exception handling for Telegram API errors
- Logging of errors for debugging purposes

### Common Error Codes

- **400 Bad Request** - Invalid request parameters
- **401 Unauthorized** - Authentication required
- **403 Forbidden** - Access denied
- **404 Not Found** - Resource not found
- **500 Internal Server Error** - Server-side error

### Telegram API Errors

Telegram API errors are wrapped in `TelegramAPIError` exceptions:

```python
class TelegramAPIError(Exception):
    def __init__(self, message: str, error_code: int = None, response=None):
        super().__init__(f"Telegram API error {error_code}: {message}")
        self.error_code = error_code
```

## Rate Limiting

The Telegram Bot API has rate limits:
- Maximum 30 messages per second globally
- Maximum 20 messages per minute to the same group chat

The application should implement appropriate rate limiting to avoid hitting these limits.