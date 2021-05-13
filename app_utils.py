import base64
import datetime
import hmac
import json
import time

from config import *


class HeaderUtils:
    method = "GET"
    body = ""

    def __init__(self, api_key, passphrase, secret_key):
        self.api_key = api_key
        self.passphrase = passphrase
        self.secret_key = secret_key

    @staticmethod
    def get_timestamp():
        now = datetime.datetime.utcnow()
        t = now.isoformat("T", "milliseconds")
        return t + "Z"

    @staticmethod
    def get_unix_timestamp():
        return str(round(time.time()))

    @staticmethod
    def pre_hash(timestamp, method, request_path, body):
        return str(timestamp) + str.upper(method) + request_path + body

    @staticmethod
    def sign_encode(message, secretKey):
        mac = hmac.new(
            bytes(secretKey, encoding="utf8"),
            bytes(message, encoding="utf-8"),
            digestmod="sha256",
        )
        d = mac.digest()
        return base64.b64encode(d)

    def get_ws_sign(self, request_path="/users/self/verify"):
        timestamp = self.get_unix_timestamp()
        sign = self.sign_encode(
            self.pre_hash(timestamp, self.method, request_path, str(self.body)),
            self.secret_key,
        )  # 签名
        return str(sign, encoding="utf8")

    def get_rest_sign(self, request_path):
        timestamp = self.get_timestamp()
        sign = self.sign_encode(
            self.pre_hash(timestamp, self.method, request_path, str(self.body)),
            self.secret_key,
        )  # 签名
        header = dict()
        header[CONTENT_TYPE] = APPLICATION_JSON
        header[OK_ACCESS_KEY] = self.api_key
        header[OK_ACCESS_SIGN] = str(sign, encoding="utf-8")
        header[OK_ACCESS_TIMESTAMP] = str(timestamp)
        header[OK_ACCESS_PASSPHRASE] = self.passphrase
        return header

    def get_ws_header(self, request_path="/users/self/verify"):
        timestamp = self.get_unix_timestamp()
        sign = self.sign_encode(
            self.pre_hash(timestamp, self.method, request_path, str(self.body)),
            self.secret_key,
        )  # 签名
        header = dict()
        header["apiKey"] = self.api_key
        header["sign"] = str(sign, encoding="utf-8")
        header["timestamp"] = timestamp
        header["passphrase"] = self.passphrase
        return header


header_util = HeaderUtils(api_key=API_KEY, passphrase=PASSPHRASE, secret_key=SECRET_KEY)


def gen_send_msg(op: str, args: dict) -> str:
    return f'{{"op": "{op}", "args": [{json.dumps(args)}]}}'


def gen_send_order_msg(order_id, op: str, args: dict) -> str:
    if isinstance(order_id, int):
        order_id = str(order_id)
    return f'{{"id": {order_id}, "op": "{op}", "args": [{json.dumps(args)}]}}'


# 处理推送信息
def get_resp_data(resp: dict):
    return resp.get("data")


def get_resp_channel(resp: dict):
    return resp.get("arg").get("channel")


class Proccessor:
    @staticmethod
    def get():
        import os

        import psutil as psutil

        pid = os.getpid()
        p = psutil.Process(pid)
        # 打开进程socket的namedutples列表
        print(p.connections())
        # 此进程的线程数
        print("Process number of threads : %s" % p.num_threads())
        # 打开进程socket的namedutples列表
        print(p.connections())
        # 此进程的线程数
        print("Process number of threads : %s" % p.num_threads())
        return pid
