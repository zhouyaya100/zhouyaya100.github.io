from peewee import *
import os

# 使用SQLite（MVP推荐，生产环境替换为PostgreSQL）
db = SqliteDatabase(os.path.join(os.path.dirname(__file__), 'monitor.db'))

class BaseModel(Model):
    class Meta:
        database = db

class Group(BaseModel):
    name = CharField(unique=True)

class Device(BaseModel):
    ip = CharField(unique=True)
    protocol = CharField()  # ipmi/snmp
    username = CharField()
    password = CharField()
    group = CharField(default="Default")

def init_db():
    db.connect()
    db.create_tables([Group, Device])
    # 初始化默认分组
    if not Group.select().exists():
        Group.create(name="Default")
