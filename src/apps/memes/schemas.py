from typing import IO

from apps.base.schemas import BaseSchema


class MemeCreateSchema(BaseSchema):
    title: str
    description: str | None = None


class MemeSchema(MemeCreateSchema):
    id: int


class MemeResponceSchema(BaseSchema):
    meme: MemeSchema
    image: bytes


class MemeUpdateSchema(BaseSchema):
    title: str | None = None
    description: str | None = None
