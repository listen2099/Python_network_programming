import threading


def a(x=3):
    for i in range(x):
        out = 'a.x {}'.format(i)
        # print(out)
        # threading.Event().wait(0.001)
        yield out


def b(x=3):
    for i in range(x):
        out = 'b.x {}'.format(i)
        # print(out)
        # threading.Event().wait(0.001)
        yield out


# threading.Thread(target=a).start()
# threading.Thread(target=b).start()


a = a()
b = b()

for i in range(3):  # 必须有循环
    print(next(a))
    print(next(b))
