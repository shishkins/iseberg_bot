import os
import sys
import time
import json
import random
import requests
from zoneinfo import ZoneInfo
import hmac
import hashlib
from dateutil import parser
from json import dumps as dp, loads as ld
import datetime
from colorama import *
from urllib.parse import unquote

merah = Fore.LIGHTRED_EX
putih = Fore.LIGHTWHITE_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
hitam = Fore.LIGHTBLACK_EX

# # url = 'https://0xiceberg.store/api/v1/web-app'
#
# account_data = 'query_id=AAHhNAAYAAAAAOE0ABjgxCX0&user=%7B%22id%22%3A402666721%2C%22first_name%22%3A%22shishka%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22tretiakov_aal%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1718430826&hash=03f4cf9d73c33eeea14e70d77a6326836dc7611ae5c7c5bf80a2769fabdcbb95'
#
# def data_parsing(data):
#     redata = {}
#     for i in unquote(data).split("&"):
#         key, value = i.split("=")
#         redata[key] = value
#
#     return redata
#
# def get_secret(userid):
#     rawr = "adwawdasfajfklasjglrejnoierjboivrevioreboidwa"
#     secret = hmac.new(
#         rawr.encode("utf-8"), str(userid).encode("utf-8"), hashlib.sha256
#     ).hexdigest()
#     return secret
#
# data_parse = data_parsing(account_data)
# user = json.loads(data_parse['user'])
# base_headers = {
#     "accept": "application/json, text/plain, */*",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
#     "content-type": "application/json",
#     "origin": "https://0xiceberg.store/webapp",
#     "x-requested-with": "org.telegram.messenger",
#     "sec-fetch-site": "same-site",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-dest": "empty",
#     "referer": "https://0xiceberg.store/webapp/",
#     "accept-encoding": "gzip, deflate",
#     "accept-language": "en,en-US;q=0.9",
# }
#
# headers = base_headers.copy()
# headers['X-Telegram-Auth'] = account_data
# # user = json.loads(data_parse['user'])
# # userid = str(user['id'])
# # # headers['secret'] = get_secret(userid)
# # headers['tg-id'] = userid
# # headers['username'] = None
#
# def solve_tasks():
#     url ='https://0xiceberg.store/api/v1/web-app/tasks'
#     res = requests.post(url = url, headers = headers)
#     for task in res.json():
#         task_id = task["id"]
#         task_title = task["description"]
#         task_status = task["status"]
#         if task_status == "new":
#             url_start = (
#                 f"https://0xiceberg.store/api/v1/web-app/tasks/task/{task_id}/"
#             )
#             res = requests.get(url = url_start, headers = headers)
#             res_link = requests.get(url = res.json()['link'], headers = headers)
#             if "message" in res.text:
#                 continue
#
#             url_claim = (
#                 f"https://game-domain.blum.codes/api/v1/tasks/{task_id}/claim"
#             )
#             res = requests.post(url_claim, headers, "")
#             if "message" in res.text:
#                 continue
#
#             status = res.json()["status"]
#             if status == "collected":
#                 print(f"success complete task {task_title} !")
#                 continue
#
# def
#
# def claim_reward():
#     status_api, balance_api = 'farming', 'balance'
#     url = 'https://0xiceberg.store/api/v1/web-app/{task}'
#     balance_res = requests.post(url=url.format(task=balance_api), headers=headers).json()
#     status_res = requests.post(url=url.format(task=status_api), headers=headers).json()
#     stop_time_farming = parser.parse(status_res['stop_time'])
#
#     print(balance_res.json()['amount'])

class IceBergBot:
    def __init__(self):
        self.base_headers = {
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
            "content-type": "application/json",
            "origin": "https://0xiceberg.store/webapp",
            "x-requested-with": "org.telegram.messenger",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://0xiceberg.store/webapp/",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en,en-US;q=0.9",
        }

        import data, proxies
        self.datas = data.dict_data
        self.proxies = proxies.dict_proxies
        self.current_account_proxy = self.proxies[1]
        self.current_account_number = None

        self.all_end_farming = dict.fromkeys(self.datas, datetime.datetime.now())
        self.all_balances = dict.fromkeys(self.datas)
        self.all_claiming_status = dict.fromkeys(self.datas, True)
        self.config = json.loads(open('config.json', 'r').read())

    def http(self, url):
        headers = self.base_headers.copy()
        headers['X-Telegram-Auth'] = self.datas[self.current_account_number]
        proxy_headers = {
            'https': self.proxies[self.current_account_number]
        }
        counter_tries = 0
        while True:
            try:
                res = requests.post(url=url,
                                    headers=headers,
                                    proxies=proxy_headers,
                                    timeout=30)
                open(".http_request.log", "a", encoding="utf-8").write(res.text + "\n")
                if "<html>" in res.text:
                    time.sleep(2)
                    continue

                return res
            except (
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ConnectTimeout,
                    requests.exceptions.ReadTimeout,
            ) as e:
                counter_tries += 1
                self.log(f"{merah}connection error, try:{hijau}{counter_tries}")
                open(".http_request.log", "a", encoding="utf-8").write(repr(e) + "\n")
                if counter_tries > self.config['max_http_retries']:
                    self.log(f"{merah}maximum connection retries, raising error")
                    raise e

    def get_balance(self):
        url_balance = 'https://0xiceberg.store/api/v1/web-app/balance'
        res = self.http(url=url_balance)
        self.all_balances[self.current_account_number] = res.json()['amount']

    def claim_reward(self):
        url_farming = 'https://0xiceberg.store/api/v1/web-app/farming'
        res = self.http(url=url_farming)
        self.all_balances[self.current_account_number] = res.json()['amount']

bot = IceBergBot()
bot.current_account_number = 1
bot.claim_reward()

# solve_tasks()
claim_reward()

# res = requests.post(url, headers, auth = BearerAuth('3pVzwec1Gs1m'))