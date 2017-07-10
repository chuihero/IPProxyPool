# coding:utf-8
import sys
from config import DB_CONFIG
from util.exception import Con_DB_Fail
import queue


try:
    if DB_CONFIG['DB_CONNECT_TYPE'] == 'pymongo':
        from db.MongoHelper import MongoHelper as SqlHelper
    elif DB_CONFIG['DB_CONNECT_TYPE'] == 'redis':
        from db.RedisHelper import RedisHelper as SqlHelper
    else:
        from db.SqlHelper import SqlHelper as SqlHelper
    sqlhelper = SqlHelper()
    sqlhelper.init_db()
except Exception as e:
    raise Con_DB_Fail


def store_data(queue2, db_proxy_num,q2_close_flag):
    '''
    读取队列中的数据，写入数据库中
    :param queue2:
    :return:
    '''
    successNum = 0
    failNum = 0
    while not q2_close_flag.is_set():
        try:
            proxy = queue2.get(timeout=60)
            if proxy:

                sqlhelper.insert(proxy)
                successNum += 1
            else:
                failNum += 1
            str = 'IPProxyPool----->>>>>>>>Success ip num :%d,Fail ip num:%d' % (successNum, failNum)
            print(str)
            sys.stdout.write(str + "\r")
            sys.stdout.flush()
        except queue.Empty:
            # print('empty')
            # 队列为空，继续
            continue

        except BaseException as e:
            print(e)
            if db_proxy_num.value != 0:
                successNum += db_proxy_num.value
                db_proxy_num.value = 0
                str = 'IPProxyPool----->>>>>>>>Success ip num :%d,Fail ip num:%d' % (successNum, failNum)
                print(str)
                sys.stdout.write(str + "\r")
                sys.stdout.flush()
                successNum = 0
                failNum = 0
    print('DataStore end')



