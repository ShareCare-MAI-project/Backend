import re
from typing import Any, Callable

from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

PHONE_REGEX = r"^\+79[0-9]{9}$"


#  Пример кастомного типа, работающего с Pydantic+Swagger
class PhoneNumber(str):
    """Класс для валидации номера телефона."""

    @classmethod
    def __get_pydantic_core_schema__(
            cls,
            _source_type: Any,
            handler: Callable[[Any], core_schema.CoreSchema]
    ) -> core_schema.CoreSchema:
        str_schema = handler(core_schema.str_schema())

        return core_schema.no_info_after_validator_function(
            cls.validate,
            str_schema,
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
            cls,
            schema: core_schema.CoreSchema,
            handler: Callable[[core_schema.CoreSchema], JsonSchemaValue]
    ) -> JsonSchemaValue:
        json_schema = handler(schema)
        json_schema.update({
            "type": "string",
            "format": "phone",
            "pattern": PHONE_REGEX,
            "example": "+1234567890",
            "minLength": 10,
            "maxLength": 15
        })
        return json_schema

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')

        if not re.match(PHONE_REGEX, v):
            raise ValueError('Неверный формат номера телефона')

        return v
