from wsmode import messages as m


class MessageCallbackHandler:
    def __init__(
        self,
    ):
        self.handlers = {}

    def dispatch(self, topic_message: m.TopicMessage):
        topic_message_type = topic_message.__class__
        handler_func = self.handlers.get(topic_message_type)
        return handler_func(topic_message)

    def register_event(self, msg_type: m.TopicMessage):
        def decorator(fn):
            self.handlers[msg_type] = fn
            return fn

        return decorator
