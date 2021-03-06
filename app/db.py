from enum import IntEnum

from peewee import Model, IntegerField, PostgresqlDatabase, TextField, CompositeKey, CharField
from urllib3.util import parse_url

from config import *
from modules.utils import choices_from_enum


def get_database():
    parsed_url = parse_url(db_url)

    # Берём из auth имя пользователя и пароль от БД
    username, password = parsed_url.auth.split(':')

    return PostgresqlDatabase(
        parsed_url.path[1:],  # Пропускаем первый "/", так как он не является названием БД
        host=parsed_url.host,
        user=username,
        password=password
    )


database = get_database()

EPlatform = IntEnum('EPlatform', 'tg vk')


class Session(Model):
    platform = IntegerField(default=1, choices=choices_from_enum(EPlatform), help_text='Platform ID')
    id = CharField(help_text='Platform ID')
    state = IntegerField(default=1, help_text='Current bot state for user')
    state_param = TextField(default='', help_text='Param for state')
    text = TextField(default='')

    def set_state(self, state: IntEnum, param=''):
        self.state = state.value
        self.state_param = param

    def __repr__(self):
        return '<Session {}{} s{}|{} >'.format(EPlatform(self.platform).name, self.id, self.state, self.state_param)

    class Meta:
        database = database
        table_name = 'bot_session'
        primary_key = CompositeKey('id', 'platform')


def create_tables():
    with database:
        database.create_tables([Session])
    # закрываем подключение, чтобы не могли слушать ничего страшного.
    database.close()
