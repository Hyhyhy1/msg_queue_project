from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

class EmailNotification(BaseModel):
    type: str = Field("email")
    recipient: EmailStr
    message: str

    @field_validator('type')
    def check_type(cls, v):
        if v != "email":
            raise ValueError('type must be "email"')
        return v


class SMSNotification(BaseModel):
    type: str = Field("sms")
    recipient: PhoneNumber
    message: str

    @field_validator('type')
    def check_type(cls, v):
        if v != "sms":
            raise ValueError('type must be "sms"')
        return v


class PushNotification(BaseModel):
    type: str = Field("push")
    recipient: str
    message: str

    @field_validator('type')
    def check_type(cls, v):
        if v != "push":
            raise ValueError('type must be "push"')
        return v