from pydantic import BaseModel, Field

class TravelPlan(BaseModel):
    itinerary: str = Field(..., description="Multi-day travel schedule with details")
    highlights: str = Field(..., description="Summary of key experiences")
    saved_path: str = Field(default="", description="Where the itinerary was saved") 