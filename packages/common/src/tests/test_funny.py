import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..miose_toolkit_common import (
        advance_call,
        advance_class_call,
        async_advance_call,
    )
else:
    from miose_toolkit_common import (
        advance_call,
        advance_class_call,
        async_advance_call,
    )


def test_funny():
    @advance_call(show_output=False)
    def test1():
        pass

    test1()

    @advance_call(show_output=True)
    def test2():
        pass

    test2()

    @advance_call(show_output=True, loops=2)
    def test3():
        pass

    test3()

    @advance_call(show_output=True, spin_interval=0.05)
    def test4():
        pass

    test4()

    @advance_class_call(show_output=False)
    class Test1:
        def __init__(self):
            pass

    Test1()

    @advance_class_call(show_output=True)
    class Test2:
        def __init__(self):
            pass

    Test2()

    @advance_class_call(show_output=True, loops=2)
    class Test3:
        def __init__(self):
            pass

    Test3()

    @advance_class_call(show_output=True, spin_interval=0.05)
    class Test4:
        def __init__(self):
            pass

    Test4()

    @async_advance_call(show_output=False)
    async def test5():
        pass

    asyncio.run(test5())

    @async_advance_call(show_output=True)
    async def test6():
        pass

    asyncio.run(test6())

    @async_advance_call(show_output=True, loops=2)
    async def test7():
        pass

    asyncio.run(test7())

    @async_advance_call(show_output=True, spin_interval=0.05)
    async def test8():
        pass

    asyncio.run(test8())
