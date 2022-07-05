from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel, validator, Field, root_validator


class UUIDValidationMixin:
    UUID_VERSION = 4

    @classmethod
    def create_uuid_validator(cls, *fields, **kwargs) -> classmethod:
        return validator(*fields, allow_reuse=True, **kwargs)(cls._validate_uuid)

    @classmethod
    def _validate_uuid(cls, uuid_str: str) -> str:
        try:
            uuid_obj = UUID(uuid_str, version=cls.UUID_VERSION)
            assert str(uuid_obj) == uuid_str
        except (ValueError, AssertionError):
            raise ValueError(f'{uuid_str} is not a valid UUID')
        return uuid_str


class Book(BaseModel):
    _MIN_PRICE = 0

    id: str = Field(default_factory=uuid4)
    title: str
    description: Optional[str]
    price: float
    author_id: str

    _is_valid_id = UUIDValidationMixin.create_uuid_validator('id')
    _is_valid_author_id = UUIDValidationMixin.create_uuid_validator('author_id')

    @validator('price')
    @classmethod
    def validate_price(cls, price: float) -> float:
        if not cls._MIN_PRICE <= price:
            raise ValueError(f'Price must be less then {cls._MIN_PRICE} inclusive')
        return price


class Author(BaseModel):
    _MIN_AGE = 18
    _MAX_AGE = 120

    id: str = Field(default_factory=uuid4)
    first_name: Optional[str]
    last_name: Optional[str]
    pseudonym: Optional[str]
    age: int
    country: str

    _is_valid_id = UUIDValidationMixin.create_uuid_validator('id')

    @validator('age')
    @classmethod
    def validate_age(cls, age: int) -> int:
        if not cls._MIN_AGE <= age <= cls._MAX_AGE:
            raise ValueError(f'Age must be between {cls._MIN_AGE} and {cls._MAX_AGE} inclusive')
        return age

    @root_validator
    @classmethod
    def validate_author_name(cls, values: dict) -> dict:
        if not (values.get('first_name') and values.get('last_name') or values.get('pseudonym')):
            raise ValueError('The author must have a pseudonym or first name last name or both')
        return values


class User(BaseModel):
    id: str = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    library_card_number: str = Field(default_factory=uuid4)

    _is_valid_id = UUIDValidationMixin.create_uuid_validator('id')
    _is_valid_library_card_number = UUIDValidationMixin.create_uuid_validator('library_card_number')
