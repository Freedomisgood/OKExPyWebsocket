# 提供根据行情反映的策略
# from wsmode.agent import BaseAgent
from wsmode.messages import (
    BalanceAndPositionTopicMessage,
    LoginTopicMessage,
    TopicMessage,
)


class IStrategy:
    """
    根据行情反应的策略, 买卖策略定义者
    """

    def __init__(self):
        self.agent = None

    def set_agent(self, agent):
        self.agent = agent

    def register(self):
        """
        根据主题消息类型绑定处理函数
        @return:
        """
        raise NotImplementedError

    def open_subscribe(self):
        raise NotImplementedError


class GreenerStrategy(IStrategy):
    def register(self):
        self.agent.msg_cb_handler.register_event(LoginTopicMessage)(self.login_handle)
        self.agent.msg_cb_handler.register_event(BalanceAndPositionTopicMessage)(
            self.balance_and_position_topic_message_handle
        )

    def open_subscribe(self):
        # 订阅通知, 频道
        self.agent.ws.send(
            '{"op":"subscribe","args":[{"channel": "balance_and_position"}]}'
        )

    @staticmethod
    def login_handle(data: TopicMessage):
        print("处理登陆信息", data)

    @staticmethod
    def balance_and_position_topic_message_handle(data: TopicMessage):
        print("处理余额信息", data)
