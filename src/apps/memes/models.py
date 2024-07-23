from tortoise import fields, Model

from apps.base.models import TimeStampMixin


class Meme(Model, TimeStampMixin):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField(null=True)

    class Meta:
        table = "memes"
