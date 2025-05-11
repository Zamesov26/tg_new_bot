import json
import typing

from aiohttp.web_exceptions import (HTTPConflict, HTTPException, HTTPNotFound,
                                    HTTPUnprocessableEntity)
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware
from aiohttp_session import get_session
from sqlalchemy.exc import IntegrityError

from app.admin.models import admin_from_session
from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application, Request


HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def auth_middleware(request: "Request", handler: typing.Callable):
    session = await get_session(request)
    if session:
        request.admin = admin_from_session(session)
    return await handler(request)


PGCODE_DUPLICATE = "23505"
PGCODE_NOTFOUND = "23503"


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message=e.reason,
            data=json.loads(e.text),
        )

    except IntegrityError as e:
        if e.orig.pgcode == PGCODE_DUPLICATE:
            raise HTTPConflict
        elif e.orig.pgcode == PGCODE_NOTFOUND:
            raise HTTPNotFound
        raise

    except HTTPException as e:
        return error_json_response(
            http_status=e.status,
            status=HTTP_ERROR_CODES[e.status],
            message=str(e),
        )
    except Exception as e:
        request.app.logger.error("Exception", exc_info=e)
        return error_json_response(
            http_status=500, status="internal server error", message=str(e)
        )

    return response


def setup_middlewares(app: "Application"):
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
    app.middlewares.append(auth_middleware)
