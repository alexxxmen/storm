# -*- coding:utf-8 -*-

from playhouse.postgres_ext import PostgresqlExtDatabase
from peewee import (Model, CharField, DateTimeField, TextField,
                    datetime as peewee_datetime, DoubleField, SmallIntegerField)

from utils import Struct
from config import DB_CONFIG
from constants import BidStatus

peewee_now = peewee_datetime.datetime.now

db = PostgresqlExtDatabase(**DB_CONFIG)
db.commit_select = True
db.autorollback = True


class _Model(Model):
    class Meta:
        database = db
        only_save_dirty = True
    
    def to_dict(self):
        return dict(self._data.items())
    
    def to_struct(self):
        return Struct(**self.to_dict())

    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.get(cls.id == id) if id else None
        except cls.DoesNotExist:
            return None


class Bid(_Model):
    class Meta:
        db_table = 'bids'

    name = CharField()
    email = CharField()
    account = CharField()  # instagram account
    amount = DoubleField(null=True)
    status = SmallIntegerField(default=BidStatus.New)
    created = DateTimeField(default=peewee_datetime.datetime.now)

    @classmethod
    def new(cls, name, email, account):
        with db.atomic():
            return cls.create(
                name=name,
                email=email,
                account=account
            )


class ClientLog(_Model):
    class Meta:
        db_table = 'client_logs'

    error = TextField(null=True)
    request_ip = CharField()
    request_url = TextField()
    request_data = TextField()
    request_headers = TextField()
    finished = DateTimeField()
    request_method = CharField()
    traceback = TextField(null=True)
    created = DateTimeField(default=peewee_datetime.datetime.now)
