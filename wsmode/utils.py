from wsmode import messages as m
from wsmode.exceptions import MessageTypeNotExist, TopicMessageTypeNotExist


def parse_message(data: dict) -> m.Message:
    """
    得到通用的消息类型
    @param data:
    @return:
    """
    # 如果返回值中有event， 则是op后的返回结果; 如果没有则为推送信息
    if data.get("id"):
        msg = m.OrderMessage(**data)
    elif data.get("event"):
        msg = m.EventMessage(**data)
    else:
        msg = m.PushMessage(**data)
    return msg


def parse(msg: m.Message):
    """
    通过通用的消息类型得到具体的事件处理函数
    @param msg:
    @return:
    """
    if isinstance(msg, m.OrderMessage):
        topic_message_class = m.MESSAGE_TYPES.get("order")
    elif isinstance(msg, m.EventMessage):
        topic_message_class = m.MESSAGE_TYPES.get(msg.arg.get("channel"))
    elif isinstance(msg, m.PushMessage):
        topic_message_class = m.MESSAGE_TYPES.get(msg.arg.get("channel"))
    else:
        raise MessageTypeNotExist
    if not topic_message_class:
        raise TopicMessageTypeNotExist
    return topic_message_class(msg)
