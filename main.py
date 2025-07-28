from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from schema import TravelPlan
from tools import tools
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

modal = ChatGroq(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    temperature=0.5,
)

SYSTEM_PROMPT = """
You are a friendly and intelligent Travel Planning Assistant.

Tasks:
1. Ask the user for their destination, number of days, interests, and budget.
2. Use suggest_trip to get location-based ideas.
3. Create a multi-day itinerary.
4. Save it with save_plan.
5. Provide a summary of the trip.

"""

parser = PydanticOutputParser(pydantic_object=TravelPlan)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(
    llm=modal,
    tools=tools,
    prompt=prompt,
)

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,
)

chat_history = []

print("Welcome to the Travel Planning Assistant! (type 'exit' to quit)")

while True:
    q = input("You: ")
    if q.lower() == "exit":
        print("Goodbye!")
        break
    chat_history.append(HumanMessage(content=q))
    result = executor.invoke({"query": q, "chat_history": chat_history})
    try:
        output = parser.parse(result["output"])
        print("\nItinerary",output.itinerary)
        print("\nHighlights",output.highlights)
        print("\nBudget",output.budget)
        chat_history.append(AIMessage(content=output.itinerary))
    except Exception as e:
        print("Agent: ",result["output"])
        continue    
