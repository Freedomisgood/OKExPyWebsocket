from typing import Optional

import pydantic


# ----------------------- ↓↓↓↓↓ 通用的消息类型 ↓↓↓↓↓ ----------------------- #
class Message(pydantic.BaseModel):
    pass


class EventMessage(Message):
    event: str
    # 失败有下面三项， 且登陆无arg
    code: Optional[str]
    msg: Optional[str]
    arg: Optional[dict]


class PushMessage(Message):
    data: list
    action: Optional[str]
    arg: dict


class OrderMessage(pydantic.BaseModel):
    id: str
    op: str
    data: list
    code: str
    msg: str


# ----------------------- ↑↑↑↑↑ 通用的消息类型 ↑↑↑↑↑ ----------------------- #


# ----------------------- ↓↓↓↓↓ 具体的推送消息类型注册装饰器 ↓↓↓↓↓ ----------------------- #
MESSAGE_TYPES = {}


def register_topic_message(msg_type):
    def register(cls):
        MESSAGE_TYPES[msg_type] = cls
        return cls

    return register


# ----------------------- ↑↑↑↑↑ 具体的推送消息类型注册装饰器 ↑↑↑↑↑ ----------------------- #


# ----------------------- ↓↓↓↓↓ 具体的推送消息类型 ↓↓↓↓↓ ----------------------- #
class TopicMessage(Message):
    msg_data: Optional[Message]

    def __init__(self, msg: Message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg_data = msg


@register_topic_message("login")
class LoginTopicMessage(TopicMessage):
    pass


@register_topic_message("balance_and_position")
class BalanceAndPositionTopicMessage(TopicMessage):
    pass


@register_topic_message("order")
class OrderTopicMessage(TopicMessage):
    pass


@register_topic_message("instruments")
class InstrumentsTopicMessage(TopicMessage):
    pass


# ----------------------- ↑↑↑↑↑ 具体的消息类型 ↑↑↑↑↑ ----------------------- #
