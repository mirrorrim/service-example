from pydantic import BaseModel, ConfigDict


def to_camel(string: str) -> str:
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


default_config = ConfigDict(
    from_attributes=True, alias_generator=to_camel, populate_by_name=True
)


class BaseSchema(BaseModel):
    model_config = ConfigDict(**default_config)


class ObjectCreatedResponse(BaseSchema):
    id: int
