# Condition版本生产者消费者

import threading
import time
import random

CONDTITION = threading.Condition()  # 创建一个共享Condition
GMONEY = 1000  # 金库初始值
TIMES = 0  # 生产次数初始值
TOTALTIMES = 10  # 生产者只生产10次


# 生产者
class Producer(threading.Thread):
    def run(self):
        global GMONEY
        global TIMES
        while True:
            money = random.randint(100, 1000)
            CONDTITION.acquire()  # 获取锁
            if TIMES >= TOTALTIMES:
                CONDTITION.release()
                print('{}生产完毕'.format(threading.current_thread()))
                break
            GMONEY += money
            print('{}生产了{}元，总共{}元'.format(threading.current_thread(), money, GMONEY))
            TIMES += 1
            CONDTITION.notify_all()
            CONDTITION.release()  # 释放锁
            time.sleep(0.5)


# 消费着
class Consumer(threading.Thread):
    def run(self):
        global GMONEY
        while True:
            money = random.randint(100, 1000)
            CONDTITION.acquire()
            while GMONEY < money:
                if TIMES >= TOTALTIMES:
                    CONDTITION.release()
                    return
                print('{}准备消费{}元，剩余{}元，不足!'.format(threading.current_thread(), money, GMONEY))
                CONDTITION.wait()  # 等待生产完毕通知
            GMONEY -= money
            print('{}消费了{}元，剩余{}元'.format(threading.current_thread(), money, GMONEY))
            CONDTITION.release()
            time.sleep(0.5)


def main():
    # 3个消费者
    for x in range(3):
        t = Consumer(name='消费者')
        t.start()

    # 5个生产者
    for x in range(5):
        t = Producer(name='生产者')
        t.start()


if __name__ == '__main__':
    main()
