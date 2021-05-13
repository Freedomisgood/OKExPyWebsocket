import time

from faker import Faker
from ws4py.client.threadedclient import WebSocketClient

import app_utils as u
from app_utils import WS_PRIVATE_URL, WS_PUBLIC_URL, gen_send_msg, gen_send_order_msg
from constant import Channel, Operation
from wsmode import stategies as s, utils as pu
from wsmode.handler import MessageCallbackHandler

fake = Faker("zh-CN")


class BaseAgent:
    """
    提供环境上下文
    """

    URL = ""

    def __init__(
        self,
        strategy: s.IStrategy,
        msg_cb_handler: MessageCallbackHandler,
        ws: WebSocketClient = None,
    ):
        self.ws = ws
        self.msg_cb_handler = msg_cb_handler
        self.strategy = strategy
        self.strategy.set_agent(self)
        self.strategy.register()

    def handle(self, json_msg: dict):
        msg = pu.parse_message(json_msg)
        topic_msg = pu.parse(msg)
        self.msg_cb_handler.dispatch(topic_msg)

    def set_websocket(self, ws: WebSocketClient):
        self.ws = ws

    def after_ws_opened(self):
        raise NotImplementedError

    def subscribe_channel(self, channel: Channel, **kwargs):
        args = {
            "channel": channel,
        }
        args.update(kwargs)
        self.ws.send(gen_send_msg(Operation.SUBSCRIBE, args))


class PrivateWSAgent(BaseAgent):
    URL = WS_PRIVATE_URL

    def send_order(self, op: Operation, **kwargs):
        random_order_id = fake.pystr(min_chars=1, max_chars=32)
        self.ws.send(gen_send_order_msg(random_order_id, op, kwargs))
        return random_order_id

    def after_ws_opened(self):
        # 第一步，登陆
        headers = u.header_util.get_ws_header()
        self.ws.send(u.gen_send_msg(Operation.LOGIN, headers))
        time.sleep(1)
        print("成功登入私有频道～")
        self.strategy.open_subscribe()


class PublicWSAgent(BaseAgent):
    URL = WS_PUBLIC_URL

    def after_ws_opened(self):
        print("成功登入公有频道～")
        self.strategy.open_subscribe()

        # self.ws.send(
        #     '{"op":"subscribe","args":[{"channel": "instruments","instType": "FUTURES"}]}'
        # )
