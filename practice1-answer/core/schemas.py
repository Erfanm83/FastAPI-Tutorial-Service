from pydantic import BaseModel, field_validator, Field, field_serializer

class BaseCostSchema(BaseModel):
    description : str = Field(..., description="Enter a Description")

    @field_validator("description")
    def validate_description(cls, value):
        if len(value) > 50:
            raise ValueError("Description must not exceed 50 characters")
        if not value.isalpha():
            raise ValueError("Description must contain only alphabetic characters")
        return value
    
    @field_serializer("description")
    def serialize_description(self, value: str, _info) -> str:
        return value.title()

class CostCreateSchema(BaseCostSchema):
    amount: int = Field(..., description="An Amount of the Cost", gt=0, lt=1000000000)

    @field_validator("amount")
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount must be positive")
        if value >= 1_000_000_000:
            raise ValueError("Amount exceeds maximum allowed value")
        return value
    
    @field_serializer("amount")
    def serialize_amount(self, value):
        return f"{value / 100:.2f}"

class CostResponseSchema(BaseCostSchema):
    id: int = Field(..., description= "Unique user idebtifier")
    amount: int = Field(..., description="An Amount of the Cost")

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Amount must be positive")
        if value >= 1_000_000_000:
            raise ValueError("Amount exceeds maximum allowed value")
        return value

    @field_serializer("amount")
    def serialize_amount(self, value: int, _info) -> str:
        return f"{value / 100:.2f}"

class CostUpdateSchema(BaseCostSchema):
    amount: int = Field(..., description="An Amount of the Cost")

    @field_validator("amount")
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount must be positive")
        if value >= 1_000_000_000:
            raise ValueError("Amount exceeds maximum allowed value")
        return value
    
    @field_serializer("amount")
    def serialize_amount(self, value: int, _info) -> str:
        return f"{value / 100:.2f}"