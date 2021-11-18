from src.database.database import BaseModel
from datetime import datetime
import peewee


class UserVPN(BaseModel):
    name = peewee.CharField()
    username = peewee.CharField(unique=True)
    password = peewee.CharField()
    admin = peewee.BooleanField(default=False)

    creatdAt = peewee.DateTimeField(default=datetime.utcnow())
    updatedAt = peewee.DateTimeField(default=datetime.utcnow())

    class Meta:
        table_name = '_user'

    @property
    def exclude(self):
        return None

    @exclude.getter
    def exclude(self):
        return [
            UserVPN.password,
            UserVPN.admin
        ]


