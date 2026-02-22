from app.core.response.base_schema import CustomModel


class JWTPayloadSchema(CustomModel):
    """JWT Payload Schema."""


    sub: int

    