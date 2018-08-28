# 生产者消费者模式

# 生产者的线程专门用来生产数据，然后将数据存放在一个中间变量中，消费者再从这个中间变量中取出数据进行消费。
# 因为要使用中间变量，中间变量常是一些全局变量，因此需要使用锁来保证数据的完整性。

# Lock版本的模式
import threading
import random
import time

GMONEY = 1000  # 金钱初始值1000
GLOCK = threading.Lock()  # 创建一个共享锁
TOTALTIME = 10  # 生产者只生产10次
TIMES = 0  # 生产次数的初始值


# 生产者
class Producer(threading.Thread):
    def run(self):
        global GMONEY
        global TIMES
        while True:
            money = random.randint(100, 1000)
            GLOCK.acquire()  # 开启锁
            if TIMES >= TOTALTIME:  # 生产10次后不再生产，需要释放锁
                GLOCK.release()
                break
            GMONEY += money
            print('{}生产了{}元，总共{}元'.format(threading.current_thread(), money, GMONEY))
            TIMES += 1  # 生产次数加1
            GLOCK.release()  # 释放锁
            time.sleep(0.5)


# 消费者
class Consumer(threading.Thread):
    def run(self):
        global GMONEY
        while True:
            money = random.randint(100, 1000)
            GLOCK.acquire()  # 加锁
            if GMONEY >= money:  # 总共的钱大于消费的钱
                GMONEY -= money
                print('{}消费了{}元，剩余{}元'.format(threading.current_thread(), money, GMONEY))
            else:
                if TIMES >= TOTALTIME:  # 生产10次以后，消费者也花费完了，释放锁，不再进行消费
                    print('需花费{}元，剩余{}元，生产者不再生产，{}不再消费'.format(money, GMONEY, threading.current_thread()))
                    GLOCK.release()
                    break
                print('{}准备消费{}元，金库剩余{}元，剩余不足!'.format(threading.current_thread(), money, GMONEY))

            GLOCK.release()  # 释放锁
            time.sleep(0.5)

def main():
    # 3个消费者
    for x in range(3):
        t = Consumer(name='消费者{}'.format(x))
        t.start()

    # 5个生产者
    for x in range(5):
        t = Producer(name='生产者{}'.format(x))
        t.start()


if __name__ == '__main__':
    main()