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
import numpy as np
from json import dumps as dp, loads as ld
from datetime import datetime, timezone, timedelta
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

        self.all_end_farming = dict.fromkeys(self.datas, datetime.now(timezone.utc))
        self.all_balances = dict.fromkeys(self.datas)
        self.all_claiming_status = dict.fromkeys(self.datas, True)
        self.config = json.loads(open('config.json', 'r').read())
        self.garis = putih + "~" * 50

    def http(self, url, method = 'post'):
        headers = self.base_headers.copy()
        headers['X-Telegram-Auth'] = self.datas[self.current_account_number]
        proxy_headers = {
            'https': self.proxies[self.current_account_number]
        }
        matching_methods = {
            'post': requests.post,
            'delete': requests.delete,
            'get': requests.get,
            'patch': requests.patch
        }

        http_func = matching_methods[method]
        counter_tries = 0
        while True:
            try:
                res = http_func(url=url,
                                headers=headers,
                                proxies=proxy_headers,
                                timeout=30)
                # res = requests.post(url=url,
                #                     headers=headers,
                #                     proxies=proxy_headers,
                #                     timeout=30)
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

    def log(self, message):
        now = datetime.now(timezone.utc).isoformat(" ").split(".")[0]
        print(f"{hitam}[{now}]{reset} {message}")

    def data_parsing(self, data):
        redata = {}
        for i in unquote(data).split("&"):
            key, value = i.split("=")
            redata[key] = value

        return redata

    def get_balance(self):
        url_balance = 'https://0xiceberg.store/api/v1/web-app/balance'
        res = self.http(url=url_balance)
        self.all_balances[self.current_account_number] = res.json()['amount']
        self.log(f"{hijau}current balance: {putih}{res.json()['amount']}")

    def claim_reward(self):

        url_collect = 'https://0xiceberg.store/api/v1/web-app/farming/collect'
        url_get_next_time = 'https://0xiceberg.store/api/v1/web-app/farming/'
        time_to_claim = self.all_end_farming[self.current_account_number]
        if datetime.now(timezone.utc) < time_to_claim:
            self.log(f"{hijau}not time to claim, it will be after {putih}{time_to_claim.strftime('%d.%m.%y %H:%M')}")
        else:
            res = self.http(url=url_collect, method = 'delete')
            if res.status_code == 200:
                balance_after_claim = res.json()['amount']
                self.log(f"{hijau}success to claim reward, balance after claim: {putih}{balance_after_claim}")
            else:
                self.log(f"{merah}cannot get reward, maybe it was rewarded ago{merah}")
            res = self.http(url=url_get_next_time)
            time_to_claim = parser.parse(res.json()['stop_time'])
            self.log(f"{hijau} next time to claim will be in {putih}{time_to_claim.strftime('%d.%m.%y %H:%M')}")
            self.all_end_farming[self.current_account_number] = time_to_claim

    def countdown(self, t):
        while t:
            menit, detik = divmod(t, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"{putih}waiting until {jam}:{menit}:{detik} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def main(self):
        banner = f"""
    {hijau}AUTO CLAIM FOR {putih}ICEBERG {hijau}/ {biru}@shishkins

    {hijau}By : {putih}t.me/tretiakov_aal
    {putih}Github : {hijau}@shiskins

    {hijau}Message : {putih}Dont forget to 'git pull' maybe i update the bot !
        """
        arg = sys.argv
        if "noclear" not in arg:
            os.system("cls" if os.name == "nt" else "clear")
        print(banner)
        self.log(f"{hijau}total account : {putih}{len(self.datas)}")
        if len(self.datas) <= 0:
            self.log(f"{merah}add data account in data.py")
            sys.exit()

        self.log(self.garis)
        while True:
            list_accounts = list(self.datas.keys())
            np.random.shuffle(list_accounts)
            for no in list_accounts:
                self.current_account_number = no
                self.current_account_proxy = self.proxies[no]
                data_parse = self.data_parsing(self.datas[no])
                user = json.loads(data_parse['user'])
                self.log(f"{hijau}account number - {putih}{no + 1}")
                self.log(f"{hijau}login as : {putih}{user['first_name']}")
                self.get_balance()
                self.claim_reward()

            list_accounts.sort(key=lambda x: self.all_end_farming[x])

            min_countdown = self.all_end_farming[list_accounts[0]]
            result = min_countdown - datetime.now(timezone.utc)
            if result <= timedelta(0):
                continue

            self.countdown(int(result.total_seconds()))



if __name__ == "__main__":
    try:
        app = IceBergBot()
        app.main()
    except KeyboardInterrupt:
        sys.exit()

# res = requests.post(url, headers, auth = BearerAuth('3pVzwec1Gs1m'))

# IMPORTANT!!
# это для того, чтобы получить награду
# requests.delete(url='https://0xiceberg.store/api/v1/web-app/farming/collect/', headers = headers, proxies = proxy_headers).json()
#
# это для того, чтобы взять таск
# requests.patch(url='https://0xiceberg.store/api/v1/web-app/tasks/task/7/', data = headers).text