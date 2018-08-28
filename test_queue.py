# queue队列的使用

from queue import Queue
import threading
import time


# q = Queue(4)  # 获取一个queue对象，可以设置这个对象的大小

# for x in range(4):
#     q.put(x)  # put() 添加数据
#
# print(q.qsize())  # qsize返回queue队列的大小
#
# print(q.empty())  # 判断queue队列是否为空
#
# print(q.full())   # 判断queue队列是否满了
#
# for x in range(4):
#     print(q.get())  # 取出队列中先进去的第一个数据

# 往队列中添加值
def set_value(q):
    index = 0
    while True:
        q.put(index)
        index += 1
        time.sleep(3)


# get会阻塞等待queue队列中有值就打印
def get_value(q):
    while True:
        print(q.get())


def main():
    q = Queue(4)
    t1 = threading.Thread(target=set_value, args=(q,))
    t2 = threading.Thread(target=get_value, args=(q,))

    t1.start()
    t2.start()


if __name__ == '__main__':
    main()




