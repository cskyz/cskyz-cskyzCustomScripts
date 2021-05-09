#coding=UTF-8
from telethon import TelegramClient
from collections import defaultdict
import os
import re
import time

# 修改jcode所在目录，如果为空则使用py脚本所在目录的jdcode.txt文件
log_dir="/home/xxx/app/jd/log/jddj_fruit/"

# 填入my.telegram.org中得到的api_id和api_hash
api_id = 1234 
api_hash = 'abcd'

class PasserbyBotCMD:
    start = "/start"

'''
'''
Passerbybot_JDC = {"jddj_fruit":"好友互助码:"              # 种豆得豆
                    }

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
                match_rule = r'(JD|WX)_(.*)\,'
                match_obj = re.match(match_rule, line)
                if match_obj:
                    code_dict = {key : line}
                    code_list.append(code_dict)

    return code_list

def merge_dict(dic_list):
    dic = {}
    for _ in dic_list:
        for k, v in _.items():
            dic.setdefault(k, []).append(v)
    return dic
    

async def main(sen_to_chat_pb):

    # await client.send_message('xxx', 'Testing Telethon!')
    for msg in sen_to_chat_pb:
        if not msg:
            continue

        username = '@passerbybbot'
        await client.send_message(username, PasserbyBotCMD.start)
        time.sleep(15)
        await client.send_message(username, msg)


if __name__ == "__main__":
    dict_pb = merge_dict(make_bot_JDcode(Passerbybot_JDC))
    sen_to_chat_pb = []
    for key, value_list in dict_pb.items():
        chat_prefix = ""
        for code in value_list:
            if not code:
                continue
            chat_prefix += code.rstrip('\n')

        sen_to_chat_pb.append(chat_prefix)

    print(sen_to_chat_pb)
    with client:
        client.loop.run_until_complete(main(sen_to_chat_pb))
