# coding:utf-8

from multiprocessing import Value, Queue, Process, Event
from api.apiServer import start_api_server
from db.DataStore import store_data

from validator.Validator import validator, getMyIP
from spider.ProxyCrawl import startProxyCrawl

from config import TASK_QUEUE_SIZE

if __name__ == "__main__":
    myip = getMyIP()
    DB_PROXY_NUM = Value('i', 0)
    q1 = Queue(maxsize=TASK_QUEUE_SIZE)
    q2 = Queue()
    q1_close_flag = Event()
    q2_close_flag = Event()
    q1_close_flag.clear()
    q2_close_flag.clear()
    # p0 = Process(target=start_api_server)
    p1 = Process(target=startProxyCrawl, args=(q1, DB_PROXY_NUM,myip,q1_close_flag))
    p2 = Process(target=validator, args=(q1, q2, myip,q1_close_flag,q2_close_flag))
    p3 = Process(target=store_data, args=(q2, DB_PROXY_NUM,q2_close_flag))
    # p0.start()
    p1.start()
    p2.start()
    p3.start()
    # p0.join()
    p1.join()
    p2.join()
    print('thread2 joined')
    p3.join()
    print('thread3 join3d')
