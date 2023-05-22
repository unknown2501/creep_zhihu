import peewee

db = peewee.SqliteDatabase("main.db")
db.connect()


class Pins(peewee.Model):
    class Meta:
        database = db

    content = peewee.TextField()
    user_id = peewee.TextField()
    pin_id = peewee.TextField()
    time_update = peewee.IntegerField()


class Following(peewee.Model):
    class Meta:
        database = db

    follower_id = peewee.TextField()
    followee_id = peewee.TextField()


db.create_tables([
    Pins,
    Following
])