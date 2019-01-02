# from flask import current_app

from enum import IntEnum

from modules.state_machine import State, Machine
from .api import Message

EState = IntEnum('EState', 'initial base text meta command tags')


class InitialState(State):
    def next_state(self, msg):
        return BaseState()


class BaseState(State):
    def next_state(self, msg):
        return None


class BotStateMachine(Machine):
    map_states = {
        EState.initial: InitialState(),
    }

    def get_initial_state(self, msg):
        state = EState(msg.user.state)

        if state in self.map_states:
            return self.map_states.get(state)

        return BaseState()


machine = BotStateMachine()


def process_nmessage(message: Message):
    machine.run(message)
