import os, datetime
from langchain.tools import Tool

def save_plan(plan: str, location: str="Unknown")-> str:
    os.makedirs("plans", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"plans/{location.replace(' ', '_').lower()}_{timestamp}.txt"
    with open(filename, "w", encoding='utf-8') as file:
        file.write(plan)
    return f'Plan saved as {filename}'

def suggest_trip(city:str):
    return f"""
    Top 5 things to do in {city}:
    1. Visit historical sites
    2. Try traditional cuisine
    3. Explore museums or art districts
    4. Go hiking or sightseeing
    5. Experience local nightlife or music
    """

tools = [
    Tool(
        name="save_plan",
        func=save_plan,
        description="Save the generated itinerary to a file."
    ),
    Tool(
        name="suggest_trip",
        func=suggest_trip,
        description="Suggest activities and attractions for a city"
    )
]