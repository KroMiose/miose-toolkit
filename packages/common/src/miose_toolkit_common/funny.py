import asyncio
import time

SPINNER = ["|", "/", "-", "\\"]


def advance_call(
    show_output=True,
    spin_interval=0.1,
    loops=1,
    output_format=None,
    failed_callback=None,
):
    """\"高级\"调用装饰器

    Args:
        show_output (bool, optional): 是否显示输出. Defaults to True.
        spin_interval (float, optional): 旋转间隔. Defaults to 0.1.
        loops (int, optional): 旋转次数. Defaults to 1.
        output_format (str, optional): 输出格式. Defaults to None. 要自定义输出格式, 请使用{char}作为旋转字符占位符.
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            if show_output:
                for _ in range(loops):
                    for char in SPINNER:
                        if output_format:
                            print(output_format.format(char), end="\r")
                        else:
                            print(f"[{char}] Calling {func.__name__}...", end="\r")
                        time.sleep(spin_interval)

            try:
                func(*args, **kwargs)
            except Exception as e:
                if failed_callback:
                    failed_callback(e)
                else:
                    raise

        return inner

    return wrapper


def async_advance_call(
    show_output=True,
    spin_interval=0.1,
    loops=1,
    output_format=None,
):
    """\"高级\"异步调用装饰器

    Args:
        show_output (bool, optional): 是否显示输出. Defaults to True.
        spin_interval (float, optional): 旋转间隔. Defaults to 0.1.
        loops (int, optional): 旋转次数. Defaults to 1.
    """

    def wrapper(func):
        async def inner(*args, **kwargs):
            if show_output:
                for _ in range(loops):
                    for char in SPINNER:
                        if output_format:
                            print(output_format.format(char), end="\r")
                        else:
                            print(f"[{char}] Calling {func.__name__}...", end="\r")
                        await asyncio.sleep(spin_interval)

            await func(*args, **kwargs)

        return inner

    return wrapper


def advance_class_call(
    show_output=True,
    spin_interval=0.1,
    loops=1,
    output_format=None,
):
    """\"高级\"类调用装饰器

    Args:
        show_output (bool, optional): 是否显示输出. Defaults to True.
        spin_interval (float, optional): 旋转间隔. Defaults to 0.1.
        loops (int, optional): 旋转次数. Defaults to 1.
    """

    def wrapper(cls):
        class Inner(cls):
            def __init__(self, *args, **kwargs):
                if show_output:
                    for _ in range(loops):
                        for char in SPINNER:
                            if output_format:
                                print(output_format.format(char), end="\r")
                            else:
                                print(
                                    f"[{char}] Initializing {cls.__name__}...",
                                    end="\r",
                                )
                            time.sleep(spin_interval)

                super().__init__(*args, **kwargs)

        return Inner

    return wrapper


def with_pray(show_output=True, spin_interval=0.3, loops=3):
    def on_failed(_):
        print("The Coding God is very angry with you.")

    return advance_call(
        show_output=show_output,
        spin_interval=spin_interval,
        loops=loops,
        output_format="[{}] Praying to the Coding God for no error...",
        failed_callback=on_failed,
    )
