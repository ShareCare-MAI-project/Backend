import logging

import starlette.exceptions
from fastapi import HTTPException
from starlette import status
import asyncio
from functools import wraps


def handle_errors(error_message: str = "Внутренняя ошибка сервера",
                  status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except (HTTPException, starlette.exceptions.HTTPException):
                raise
            except Exception as e:
                logging.error(f"Error in {func.__name__}: {e}")
                raise HTTPException(
                    status_code=status_code,
                    detail=error_message
                )

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except HTTPException:
                raise
            except Exception as e:
                logging.error(f"Error in {func.__name__}: {e}")
                raise HTTPException(
                    status_code=status_code,
                    detail=error_message
                )

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
