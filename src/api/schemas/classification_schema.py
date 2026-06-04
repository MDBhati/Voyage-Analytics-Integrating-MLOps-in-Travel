from pydantic import BaseModel, Field


class GenderClassificationRequest(BaseModel):
    name: str = Field(
        ...,
        description="Traveler full name",
        examples=["Roy Braun"],
    )
    company: str = Field(
        ...,
        description="Company or booking provider",
        examples=["4You"],
    )
    age: int = Field(
        ...,
        ge=1,
        le=120,
        description="Traveler age in years",
        examples=[21],
    )
