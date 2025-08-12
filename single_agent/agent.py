import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    tz = ZoneInfo(city)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


root_agent = Agent(
    name="time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the time in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time in a city."
        "When the user provides a city name, do not pass it directly to the tool. "
        "First, determine the correct IANA time zone identifier for that city "
        "(for example, 'America/New_York', 'Europe/London', 'Asia/Tokyo'). "
        "Use reliable geographic knowledge to identify the zone, even for less common cities. "
        "Then pass that IANA zone string to the tool. "
        "If the IANA time zone cannot be determined with high confidence, ask the user for clarification."
    ),
    tools=[get_current_time],
)