import os
import sys
import time
import json
import random
import requests
import hmac
import hashlib
from json import dumps as dp, loads as ld
from datetime import datetime
from colorama import *
from urllib.parse import unquote

# url = 'https://0xiceberg.store/api/v1/web-app'

account_data = 'query_id=AAHhNAAYAAAAAOE0ABjgxCX0&user=%7B%22id%22%3A402666721%2C%22first_name%22%3A%22shishka%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22tretiakov_aal%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1718430826&hash=03f4cf9d73c33eeea14e70d77a6326836dc7611ae5c7c5bf80a2769fabdcbb95'

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def data_parsing(data):
    redata = {}
    for i in unquote(data).split("&"):
        key, value = i.split("=")
        redata[key] = value

    return redata

def get_secret(userid):
    rawr = "adwawdasfajfklasjglrejnoierjboivrevioreboidwa"
    secret = hmac.new(
        rawr.encode("utf-8"), str(userid).encode("utf-8"), hashlib.sha256
    ).hexdigest()
    return secret

data_parse = data_parsing(account_data)
user = json.loads(data_parse['user'])
base_headers = {
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

headers = base_headers.copy()
headers['X-Telegram-Auth'] = account_data
# user = json.loads(data_parse['user'])
# userid = str(user['id'])
# # headers['secret'] = get_secret(userid)
# headers['tg-id'] = userid
# headers['username'] = None

def solve_tasks():
    url ='https://0xiceberg.store/api/v1/web-app/tasks'
    res = requests.post(url = url, headers = headers)
    for task in res.json():
        task_id = task["id"]
        task_title = task["description"]
        task_status = task["status"]
        if task_status == "new":
            url_start = (
                f"https://0xiceberg.store/api/v1/web-app/tasks/task/{task_id}/"
            )
            res = requests.get(url = url_start, headers = headers)
            res_link = requests.get(url = res.json()['link'], headers = headers)
            if "message" in res.text:
                continue

            url_claim = (
                f"https://game-domain.blum.codes/api/v1/tasks/{task_id}/claim"
            )
            res = requests.post(url_claim, headers, "")
            if "message" in res.text:
                continue

            status = res.json()["status"]
            if status == "collected":
                print(f"success complete task {task_title} !")
                continue

solve_tasks()

# res = requests.post(url, headers, auth = BearerAuth('3pVzwec1Gs1m'))