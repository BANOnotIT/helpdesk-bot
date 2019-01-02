# from flask import current_app

from enum import IntEnum
from os import getcwd, path

from modules.msg_parser import get_messages
from modules.state_machine import State, Machine
from modules.text_utils import is_yes
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
        msg.session.text += '\n' + msg.text
        msg.session.save()


class MetaState(State):
    def entered(self, msg: Message):
        msg.session.set_state(EState.meta)
        msg.session.save()

        msg.reply(MESSAGES.get('meta_send'))

    def next_state(self, msg: Message):
        try:
            confirmed = is_yes(msg.text)
            if confirmed:
                return BaseState()
        except ValueError:
            pass

        return None

    def leaving(self, msg: Message):
        msg.reply(MESSAGES.get('meta_sending'))
        msg.reply(msg.session.text.strip())

    def stay(self, msg: Message):
        msg.reply(MESSAGES.get('confirm'))


class BotStateMachine(Machine):
    map_states = {
        EState.initial: InitialState(),
        EState.base: BaseState(),
        EState.meta: MetaState(),
    }

    def get_initial_state(self, msg):
        state = EState(msg.session.state)

        if state in self.map_states:
            return self.map_states.get(state)

        return BaseState()


machine = BotStateMachine()


def process_nmessage(message: Message):
    machine.run(message)
