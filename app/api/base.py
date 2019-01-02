from enum import IntEnum

from app.db import Session


class Api:
    def get_message(self, message: dict):
        raise NotImplementedError()

    def message(self, to: str, message: str):
        raise NotImplementedError()


EMessageType = IntEnum('EMessageType', 'unknown text command joined leaved')


class Message:
    text = ''  # type: str
    kind = EMessageType.unknown
    session = None  # type: Session
    chat = None

    def __init__(self, text, session, kind, chat):
        self.text = text
        self.session = session
        self.kind = kind
        self.chat = chat

    def reply(self, message: str):
        raise NotImplementedError()

    def __repr__(self):
        return '<Message {} from {}: {}>'.format(self.kind.name, self.session.__repr__(), self.text)
