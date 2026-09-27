from datetime import datetime
from html import escape
from typing import Annotated

from pydantic import BaseModel, Field, SecretStr, StringConstraints, field_serializer


PostDescription = Annotated[str, StringConstraints(min_length=1, max_length=500)]
PostName = Annotated[
    str, StringConstraints(min_length=1, max_length=50, strip_whitespace=True)
]

Username = Annotated[
    str, StringConstraints(min_length=1, max_length=20, strip_whitespace=True)
]


class PostRequest(BaseModel):
    name: PostName
    description: PostDescription


class PostResponse(BaseModel):
    name: PostName
    description: PostDescription
    created_at: datetime
    author: str

    @field_serializer("name", "description", "author")
    def escape_text(self, value: str) -> str:
        return escape(value, quote=True)


class LoginRequest(BaseModel):
    username: Username
    password: SecretStr = Field(min_length=12, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
