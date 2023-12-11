import asyncio
import time


def retry(retry_times=3, delay=1, ignore_exception: bool = True):
    """重试装饰器"""

    def wrapper(func):
        def inner(*args, **kwargs):
            for i in range(retry_times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if i == retry_times - 1:
                        if ignore_exception:
                            pass
                        else:
                            raise
                    else:
                        time.sleep(delay)
            return None

        return inner

    return wrapper


def async_retry(retry_times=3, delay=1, ignore_exception: bool = True):
    """异步重试装饰器"""

    def wrapper(func):
        async def inner(*args, **kwargs):
            for i in range(retry_times):
                try:
                    return await func(*args, **kwargs)
                except Exception:
                    if i == retry_times - 1:
                        if ignore_exception:
                            pass
                        else:
                            raise
                    else:
                        await asyncio.sleep(delay)
            return None

        return inner

    return wrapper
