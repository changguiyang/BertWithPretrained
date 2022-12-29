# !/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/17
# @Author  : szw
# @Email   : 1259577135@qq.com
# @File    : util
# @Software: 食物主义
# @desc :超级工具类

import calendar
from datetime import datetime
from datetime import  timedelta
from pymongo.collection import ReturnDocument
import pymongo
from bson import ObjectId
from random import choice
from concurrent.futures import ThreadPoolExecutor
import  hashlib
from prettytable import PrettyTable
import  re
import time
from prettytable import PrettyTable

import json
import  random



def get_proxy():
    port = random.randint(24000, 24400)
    proxies = {'http': f'http://zheng123:zheng123@haproxy.iinti.cn:{port}',
               'https': f'http://zheng123:zheng123@haproxy.iinti.cn:{port}'}
    return proxies

def subStr(s:str,startStr:str,endStr:str)->str :
    resultStr=s[s.index(startStr)+1:-1]

    resultStr=resultStr[0:resultStr.rindex(endStr)]
    return  resultStr


class mongo_manager():
    def __init__(self, collect_name, client="mongodb://127.0.0.1:27017", db="chatapi"):
        self.client=pymongo.MongoClient(client)
        self.db=self.client[db]
        self.collect=self.db[collect_name]

    def find_one_and_update(self,query,update,sort,projection=None,):
        """
        mongodb事务操作  查询并更新   类似于乐观锁  只不过是基于数据库的  性能只能说 差强人意 能用就行
        :param query:
        :param update:
        :param sort:
        :param projection:
        :return:
        """
        return  self.collect.find_one_and_update(query,{'$set': update},return_document=ReturnDocument.AFTER,sort=sort,projection=projection)

    def getCollect(self,collect_name:str)->pymongo.collection.Collection :
        """
        创建集合
        :return:
        """
        if bool(collect_name):
            return self.db[collect_name]
        return  self.collect


    def findById(self,id:str):
        myquery = {"_id": ObjectId(id)}
        return self.collect.find_one(myquery)


    def findAll(self,data=None):
        if bool(data):
            return self.collect.find(data)
        return  self.collect.find()

    def findOne(self,data=None):
        if bool(data):
            return self.collect.find_one(data)
        return  self.collect.find_one()

    def insertOne(self,data:dict):
        return self.collect.insert_one(data)

    def insertMany(self,datas:list):
        return  self.collect.insert_many(datas)

    def updateOne(self,query,new_value):
        newvalues = {"$set": new_value}
        return self.collect.update_one(query, newvalues)

    def updateMany(self, query, new_value):
        newvalues = {"$set": new_value}
        return self.collect.update_many(query, newvalues)

    # def deleteById(self,id):
    #     return self.collect.remove({"_id", ObjectId(id)})

    def  deleteOne(self,myquery):
        return  self.collect.delete_one(myquery)

    def deleteMany(self,myquery):
        return  self.collect.delete_many(myquery)

    def close(self):
        self.client.close()

def thread_util(func,seedList,threadNum=7):
    executor = ThreadPoolExecutor(max_workers=threadNum)
    executor.map(func, seedList)
    result = [data for data in executor.map(func, seedList)]
    executor.shutdown()


def camel_to_snake(string):
    string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    string = re.sub('(.)([0-9]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()

#驼峰转蟒蛇命名
def hump_to_snake(dict):
    result={}
    for k,v in dict.items():
        result[camel_to_snake(k)] = v

    return result

def md5(s):
    print(s)
    return hashlib.md5(str(s).encode()).hexdigest()[8:-8].lower()


def now():
    now_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return now_date
def today():
    today_date = time.strftime("%Y-%m-%d", time.localtime())
    return today_date



def calculate_time(delta,format="%Y-%m-%d",cur_time=(datetime.now())):
    """
    计算时间， 输入时间 进行加减
    :param delta:
    :param format:
    :param cur_time:
    :return:
    """
    day = (cur_time + timedelta(days=delta)).strftime(format)

    return day



def print_table(print_dict:dict):
    table = PrettyTable(print_dict.keys())
    datas=list()
    for k,v in print_dict.items():
        datas.append(v)
    table.add_row(datas)
    print(table)

