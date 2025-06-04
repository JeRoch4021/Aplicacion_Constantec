import functools

from database.connection import AsyncSessionLocal


def with_async_session(func):
    """
    Decorator to provide an AsyncSession to an async function.
    The decorated function must accept the session as its first argument.
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        async with AsyncSessionLocal() as session:
            try:
                # Pass the session as the first argument
                result = await func(session, *args, **kwargs)
                # Assuming successful operations should be committed.
                # You might want to make this configurable or handle it inside 'func'.
                await session.commit()
                return result
            except Exception as e:
                await session.rollback()
                # print(f"Error in {func.__name__} with session: {e}") # Optional: logging
                raise  # Re-raise the exception after rollback

    return wrapper
