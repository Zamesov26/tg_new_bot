from functools import wraps

from sqlalchemy import select

from app.bot_engine.update_context import UpdateContext
from app.medias.models import Media


def with_image_file(file_path: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(ctx: UpdateContext, *args, **kwargs):
            image_file = (
                await ctx.db_session.execute(
                    select(Media).where(Media.file_path == file_path)
                )
            ).scalar_one_or_none()

            answer = await func(ctx, *args, image_file=image_file, **kwargs)

            if image_file is None:
                try:
                    file_id = answer["result"]["photo"][0]["file_id"]
                except (KeyError, IndexError):
                    raise RuntimeError("Could not extract file_id from answer")

                media = Media(
                    title="auto_saved",
                    file_id=file_id,
                    file_path=file_path,
                )
                ctx.db_session.add(media)
            return answer

        return wrapper

    return decorator
