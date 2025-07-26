from functools import wraps

from app.bot_engine.update_context import Context
from app.medias.models import Media


def fallback_image_file(**file_path: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(ctx: Context, *args, **kwargs):
            path = kwargs.pop("image_file_path", file_path)
            kwargs["image_file"] = await ctx.store.media.get_by_file_path(
                ctx.db_session, path
            )

            answer = await func(ctx, *args, **kwargs)
            if kwargs["image_file"]:
                try:
                    file_id = answer["photo"][0]["file_id"]
                except (KeyError, IndexError):
                    raise RuntimeError("Could not extract file_id from answer")

                media = Media(
                    title="auto_saved",
                    file_id=file_id,
                    file_path=path,
                )
                ctx.db_session.add(media)
            return answer

        return wrapper

    return decorator
