# from flask import current_app

from enum import IntEnum
from os import getcwd, path

from modules.msg_parser import get_messages
from modules.state_machine import State, Machine
from .api import Message, EMessageType

EState = IntEnum('EState', 'initial base meta team')

MESSAGES = get_messages(open(path.join(getcwd(), 'messages.msg')).read())


class InitialState(State):
    def next_state(self, msg):
        return BaseState()

    def leaving(self, msg: Message):
        msg.reply(MESSAGES.get('greet'))


class BaseState(State):
    def next_state(self, msg: Message):
        if msg.kind is EMessageType.command:
            if msg.text.strip() == '/end':
                return MetaState()
            elif msg.text.strip() == '/cancel':
                return BaseState()

        return None

    def entered(self, msg: Message):
        msg.session.text = ''
        msg.session.set_state(EState.base)
        msg.session.save()

        msg.reply(MESSAGES.get('start_typing'))

    def stay(self, msg: Message):
        msg.session.text += msg.text
        msg.session.save()


class MetaState(State):
    def entered(self, msg):
        msg.session.set_state(EState.meta)
        msg.session.save()

    def next_state(self, msg):
        return None


class BotStateMachine(Machine):
    map_states = {
        EState.initial: InitialState(),
        EState.base: BaseState(),
        EState.meta: MetaState(),
    }

    def get_initial_state(self, msg):
        state = EState(msg.user.state)

        if state in self.map_states:
            return self.map_states.get(state)

        return BaseState()


machine = BotStateMachine()


def process_nmessage(message: Message):
    machine.run(message)
