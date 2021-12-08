from peewee import *
from collections import deque
from threading import Thread
import time
import datetime
import traceback as tr

# thread_safe=True
database = SqliteDatabase('test1.db', check_same_thread=False)


class Test(Model):
    ts = IntegerField()

    class Meta:
        database = database


Test.create_table()


class ThreadTest(object):
    def __init__(self):
        pass

    def f1(self):
        while True:
            try:
                time.sleep(0.1)
                p = Test(ts=int(time.time() * 1000))
                q.append(p)
            except Exception:
                print(f'{time.ctime()}, {tr.format_exc()}')

    def f2(self):
        while True:
            try:
                time.sleep(0.1)
                p = Test(ts=int(time.time() * 1000))
                q.append(p)
            except Exception:
                print(f'{time.ctime()}, {tr.format_exc()}')

    def engine(self):
        global q
        q = deque(maxlen=10000000)
        t1 = Thread(target=self.f1)
        t2 = Thread(target=self.f2)
        t1.start()
        t2.start()

        while True:
            try:
                if q:
                    print(q)
                    process = q.pop()
                    process.save()
                else:
                    time.sleep(0.08)
            except Exception:
                print(f'{time.ctime()}, {tr.format_exc()}')


if __name__ == '__main__':
    __test_case = ThreadTest()
    __test_case.engine()
