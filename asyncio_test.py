import threading
import asyncio


# @asyncio.coroutine
# def a(x=3):
#     for i in range(x):
#         out = 'a.x {}'.format(i)
#         print(out)
#         # threading.Event().wait(0.001)
#         yield
#
#
# @asyncio.coroutine
# def b(x=3):
#     for i in range(x):
#         out = 'b.x {}'.format(i)
#         print(out)
#         # threading.Event().wait(0.001)
#         yield

async def a(x=3):
    for i in range(x):
        out = 'a.x {}'.format(i)
        print(out)
        # threading.Event().wait(0.001)
        await asyncio.sleep(0.0001)


async def b(x=3):
    for i in range(x):
        out = 'b.x {}'.format(i)
        print(out)
        # threading.Event().wait(0.001)
        await asyncio.sleep(0.0001)


# threading.Thread(target=a).start()
# threading.Thread(target=b).start()


# a = a()
# b = b()
#
# for i in range(3):  # 必须有循环
#     print(next(a))
#     print(next(b))

loop = asyncio.get_event_loop()
tasks = [a(), b()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()





























