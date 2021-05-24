#coding=UTF-8
from telethon import TelegramClient
from collections import defaultdict
import os
import re
import time

# 修改jcode所在目录，如果为空则使用py脚本所在目录的jdcode.txt文件
log_dir="/home/xxx/app/jd/log/jcode/"

# 填入my.telegram.org中得到的api_id和api_hash
api_id = 1234 
api_hash = 'abcd'

class TuringLabBotCMD:
    get_all_activities = "/get_activities_status"
    submit_activity_codes = "/submit_activity_codes"

class CommitBotCMD:
    get_all_activities = "/count"
    submit_activity_codes = "/"

'''
目前支持的活动(每2分钟更新一次)
长期活动：
种豆得豆 - bean
东东农场 - farm
东东萌宠 - pet
东东工厂 - ddfactory
京喜工厂 - jxfactory
短期活动(只显示英文活动名)：
sgmh
jxcfd
health
'''
TuringLabBot_JDC = {"bean":"Bean",              # 种豆得豆
                    "farm":"Fruit",             # 东东农场
                    "pet":"Pet",                # 东东萌宠
                    "ddfactory":"JdFactory",    # 东东工厂
                    "jxfactory":"DreamFactory", # 京喜工厂
                    "sgmh":"Sgmh",              #闪购盲盒
                    "jxcfd":"Cfd",              # 京喜财富岛
                    "health":"Health",          # 东东健康社区
                    "carnivalcity":"Carni",
                    "city":"City"
                    }

'''
/jdcash  ???     # 签到领现金
/jdcrazyjoy      # 疯狂的JOY
/jdzz            # 京东赚赚
'''
CommitBot_JDC = {"jdzz":"Jdzz",              # 京东赚赚
                 "jdcrazyjoy":"Joy",         # 东东农场
                 "jdcash":"",                # 签到领现金
                }

g_log_JDcodeName = ["Bean","DreamFactory","JdFactory","Jdzz",
                    "Cfd","Health","Joy","BookShop",
                    "Sgmh","Pet","Fruit","Carni","City"]


client = TelegramClient('tg_signin', api_id, api_hash)

def get_last_JDcode_file_name(log_dir = ""):
    file_name = ""
    if log_dir == "":
        file_name = "jdcode.txt"
    else:
        list = os.listdir(log_dir)
        list.sort(key = lambda fn: os.path.getmtime(log_dir + fn) if not os.path.isdir(log_dir + fn) else 0)
        file_name = log_dir + list[-1]
    return file_name

def make_bot_JDcode(dict_in):
    code_list = []
    with open(get_last_JDcode_file_name(log_dir), 'r') as f:
        f_byts = f.readlines()
        for line in f_byts:
            for key, value in dict_in.items():
                if  not value :
                    continue
                match_rule = r'My{}(\d+)=\'(.*)\''.format(value)
                match_obj = re.match(match_rule, line)
                if match_obj:
                    code_dict = {key : match_obj.group(2)}
                    code_list.append(code_dict)

    return code_list

def merge_dict(dic_list):
    dic = {}
    for _ in dic_list:
        for k, v in _.items():
            dic.setdefault(k, []).append(v)
    # print([{k:v} for k, v in dic.items()])
    return dic
    

async def main(sen_to_chat_tlb, sen_to_chat_cb):

    # await client.send_message('xxx', 'Testing Telethon!')
    time.sleep(31)

    for msg in sen_to_chat_tlb:
        username = 'TuringLabbot'
        await client.send_message(username, msg)
        # time.sleep(0.7)
    for msg in sen_to_chat_cb:
        username = 'LvanLamCommitCodeBot'
        await client.send_message(username, msg)
        # time.sleep(0.3)
    await client.send_message('TuringLabbot',TuringLabBotCMD.get_all_activities)
    await client.send_message('LvanLamCommitCodeBot',CommitBotCMD.get_all_activities)



if __name__ == "__main__":
    dict_tlb = merge_dict(make_bot_JDcode(TuringLabBot_JDC))
    dict_cb = merge_dict(make_bot_JDcode(CommitBot_JDC))


    sen_to_chat_tlb = []
    for key, value_list in dict_tlb.items():
        chat_prefix = "{} {} ".format(TuringLabBotCMD.submit_activity_codes, key)
        for code in value_list:
            chat_prefix += code
            chat_prefix += "&"

        sen_to_chat_tlb.append(chat_prefix.rstrip('&'))

    sen_to_chat_cb = []
    for key, value_list in dict_cb.items():
        chat_prefix = "{}{} ".format(CommitBotCMD.submit_activity_codes, key)
        for code in value_list:
            chat_prefix += code
            chat_prefix += "&"

        sen_to_chat_cb.append(chat_prefix.rstrip('&'))

    print(sen_to_chat_cb)
    print(sen_to_chat_tlb)
    with client:
        client.loop.run_until_complete(main(sen_to_chat_tlb, sen_to_chat_cb))
