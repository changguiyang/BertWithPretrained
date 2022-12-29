# -*- coding: utf-8 -*-#

# -------------------------------------------------------------------------------
# Name:         chatapi.py
# Description:
# Author:       hsw
# Date:         2022/12/28
# -------------------------------------------------------------------------------
import threading
import time
import gevent
from util import mongo_manager
import os
import openai
### 第一步插入key
# openai_key = ['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'
#              ,'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'
#               ,'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']
#
# seed_mongo = mongo_manager('gptapi', db="chatapi_seed")
# for key in openai_key:
#     result={'_id':key,
#             'name':"何森伟",
#             'apikey':key,
#             "status":None
#             }
#     seed_mongo.insertOne(result)

class chat_api():
    def __init__(self, name):
        self.name = name
        self.seed_mongo = mongo_manager('gptapi', db="chatapi_seed")
        self.chatapidata = mongo_manager('gptdata', db="chatapi_seed")

    def get_seeds(self, name):
        # 先获取当前的 任务别名 如果有
        seed = self.seed_mongo.find_one_and_update({"status": None}, {"status": name}, sort=None)
        if seed:
            return seed
        else:
            print("请稍等---所有api 正在使用，程序等待2s后再请求")
            time.sleep(2)
            return self.get_seeds(self, name)

    def get_data(self, seed, promte):
        openai.api_key = seed['apikey']
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=promte,
                temperature=0.31,
                max_tokens=4000,
                top_p=0.3,
                frequency_penalty=0,
                presence_penalty=0
            )
            seed["status"] = None
            self.seed_mongo.updateOne({"_id": seed["_id"]}, seed)
            text = response.get("choices")[0]["text"]
            return text
        except Exception as e:
            print(e)
            seed["status"] = "失效"
            self.seed_mongo.updateOne({"_id": seed["_id"]}, seed)

    def save_data(self, promote,data):
        data = data.encode("utf8").decode("utf-8")
        result = {'promte':promote ,
                  'name': self.name,
                  'respones': data
                  }
        print(result)
        self.chatapidata.insertOne(result)

    def craw(self,promte):
        seed = self.get_seeds(self.name)
        while seed:
            text = self.get_data(seed,promte)
            self.save_data(promote=promte,data=text)
        else:
            print("无seed")
            time.sleep(5)

def run(name,text):
    chat = chat_api(name)
    chat.craw(text)


def run_crawler(name,lists):
    threadNum = 3
    seeds = []
    for i, text in enumerate(lists):
        print(i,text)
        t = i%threadNum
        alisname =name +'_' + str(t)
        seeds.append(gevent.spawn(run,name=alisname,text=text))
    start_time = time.time()
    gevent.joinall(seeds)
    stop_time = time.time()
    print(stop_time)




if __name__ == '__main__':
    lists = ["帮我生成1轮中文对话",
             "帮我生成2轮中文对话",
             "你好",
             "你好渣哦！",
             "你怎么那么差"]
    name ="何森伟"
    run_crawler(name,lists)
    # for i, text in enumerate(lists):
    #     t = i%2
    #     print(t)
    #     print(i,text)
    # chatapidata = mongo_manager('gptdata', db="chatapi_seed")
    # seeds =chatapidata.findAll()
    # for seed in seeds:
    #     print(seed)






