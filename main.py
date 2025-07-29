from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from schema import TravelPlan
from tools import tools
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import gradio as gr
import re
import os

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

Note: 
2. Don't show user your internal reasoning or tool calls, just the final response.
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

def respond(message, history):
    global chat_history
    
    chat_history.append(HumanMessage(content=message))
    
    result = executor.invoke({"query": message, "chat_history": chat_history})
    response = result["output"]
    
    chat_history.append(AIMessage(content=response))

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response})
    
    return "", history

def clear_chat():
    global chat_history
    chat_history = []
    return [], "", None

with gr.Blocks(title="Travel Planning Agent") as demo:
    gr.Markdown("# 🤖 Travel Planning Assistant 🌍")

    chatbot = gr.Chatbot(
        chat_history,
        height=400,
        type="messages"
    )

    msg = gr.Textbox(
        show_label=False,
        placeholder="Type your travel question here..."
    )

    with gr.Row():
        submit = gr.Button("Send")
        clear = gr.Button("Clear")

    gr.Markdown("Plan your perfect trip with personalized travel recommendations and assistance.")

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    submit.click(respond, [msg, chatbot], [msg, chatbot])
    clear.click(clear_chat, None, [chatbot, msg])

if __name__ == "__main__":
    demo.launch()
