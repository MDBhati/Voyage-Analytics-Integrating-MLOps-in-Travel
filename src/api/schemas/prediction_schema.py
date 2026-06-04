from pydantic import BaseModel, Field


class FlightPredictionRequest(BaseModel):
    from_location: str = Field(
        ...,
        description="Origin city (e.g. 'Recife (PE)')",
        examples=["Recife (PE)"],
    )
    to_location: str = Field(
        ...,
        description="Destination city (e.g. 'Florianopolis (SC)')",
        examples=["Florianopolis (SC)"],
    )
    flightType: str = Field(
        ...,
        description="Cabin class: economic, premium, or firstClass",
        examples=["firstClass"],
    )
    agency: str = Field(
        ...,
        description="Booking agency name",
        examples=["FlyingDrops"],
    )
    time: float = Field(
        ...,
        gt=0,
        description="Flight duration in hours",
        examples=[1.76],
    )
    distance: float = Field(
        ...,
        gt=0,
        description="Route distance in kilometers",
        examples=[676.53],
    )
