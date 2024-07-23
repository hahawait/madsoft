from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    # from_attributes=True позволяет создавать экземпляры модели из атрибутов объекта.
    # extra="forbid" запрещает дополнительные поля, не определенные в модели.
    model_config = ConfigDict(from_attributes=True, extra="forbid")


class ResponseSchema(BaseSchema):
    message: str
