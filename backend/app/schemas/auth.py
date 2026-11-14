from pydantic import BaseModel, ConfigDict, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="student@example.com")
    password: str = Field(..., min_length=1, example="secret123")


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    )