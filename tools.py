import os, datetime
from langchain.tools import tool

@tool
def save_plan(plan: str, location: str)-> str:
    """
    Save the travel plan to a file with a timestamp.
    Args:
        plan (str): The travel plan to save.
        location (str): The location for which the plan is created.
    Returns:
        str: Confirmation message with the filename.
    """
    os.makedirs("plans", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"plans/{location.replace(' ', '_').lower()}_{timestamp}.txt"
    with open(filename, "w", encoding='utf-8') as file:
        file.write(plan)
    return f'Plan saved as {filename}'

@tool
def suggest_trip(city:str):
    """
    Suggest a trip itinerary for a specific city.
    Args:
        city (str): The city for which to suggest a trip.
    Returns:
        str: A brief itinerary suggestion.
    """
    return f"""
    Top 5 things to do in {city}:
    1. Visit historical sites
    2. Try traditional cuisine
    3. Explore museums or art districts
    4. Go hiking or sightseeing
    5. Experience local nightlife or music
    """

tools = [
    save_plan,
    suggest_trip,
]