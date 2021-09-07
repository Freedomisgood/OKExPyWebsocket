import json
import threading
import time

from ws4py.client.threadedclient import WebSocketClient

from wsmode.agent import BaseAgent, PrivateWSAgent, PublicWSAgent
from wsmode.handler import MessageCallbackHandler
from wsmode.stategies import GreenerStrategy


class OKExRunner(WebSocketClient):
    """
    提供websocket环境
    """

    def __init__(
        self,
        agent: BaseAgent,
        protocols=None,
        extensions=None,
        heartbeat_freq=None,
        ssl_options=None,
        headers=None,
        exclude_headers=None,
    ):
        super().__init__(
            agent.URL,
            protocols,
            extensions,
            heartbeat_freq,
            ssl_options,
            headers,
            exclude_headers,
        )
        self.agent = agent
        self.agent.set_websocket(self)

    def opened(self):
        """
        # 果需要订阅多条数据，可以在下面使用ws.send方法来订阅
        # 其中 op 的取值为 1--subscribe 订阅； 2-- unsubscribe 取消订阅 ；3--login 登录
        # args: 取值为频道名，可以定义一个或者多个频道
        @return:
        """
        print("连接成功～")
        self.agent.after_ws_opened()

    def closed(self, code, reason=None):
        print("连接中断～")

    def received_message(self, resp):
        print("接收到ws服务器信息：", resp)
        if str(resp) == "pong":
            return
        json_msg = json.loads(str(resp))
        if json_msg.get("event"):
            pass
        else:
            print("分析resp消息:", type(resp), type(json_msg))
            # 如果返回值中有event， 则是op后的返回结果
            self.agent.handle(json_msg)

    def send_heart_beat(self):
        """
        TODO: 发送心跳数据
        @return:
        """
        ping = 'ping' or '{"event":"ping"}'
        while True:
            time.sleep(30)  # 每隔30秒交易所服务器发送心跳信息
            sent = False
            while sent is False:  # 如果发送心跳包时出现错误，则再次发送直到发送成功为止
                try:
                    self.send(ping)
                    sent = True
                    print("Ping sent.")
                except Exception as e:
                    print(e)


if __name__ == "__main__":
    pv_ws = None
    try:
        agent = PrivateWSAgent(GreenerStrategy(), MessageCallbackHandler())
        pv_ws = OKExRunner(agent)
        pv_ws.connect()
        threading.Thread(
            target=pv_ws.send_heart_beat, args=(), daemon=True, name="private_beat"
        ).start()  # 新建一个线程来发送心跳包
    except KeyboardInterrupt:
        pv_ws.close()

    pc_ws = None
    try:
        agent = PublicWSAgent(GreenerStrategy(), MessageCallbackHandler())
        pc_ws = OKExRunner(agent)
        pc_ws.connect()
        threading.Thread(
            target=pc_ws.send_heart_beat, args=(), daemon=True, name="public_beat"
        ).start()  # 新建一个线程来发送心跳包
        pc_ws.run_forever()
    except KeyboardInterrupt:
        pc_ws.close()
