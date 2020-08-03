from threading import Thread

import time


# 测试线程1
def thread_test_1():
    for i in range(5):
        print('thread test 1: %d' % i)
        time.sleep(1)


# 测试线程2
def thread_test_2():
    for i in range(5):
        print('thread test 2: %d' % i)
        time.sleep(1)


def handle_data_test():
    t_test_1 = Thread(target=thread_test_1)
    t_test_2 = Thread(target=thread_test_2)

    print('thread 1 start')
    t_test_1.start()

    print('thread 2 start')
    t_test_2.start()


if __name__ == '__main__':
    handle_data_test()











