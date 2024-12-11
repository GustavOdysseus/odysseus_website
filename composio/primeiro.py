from composio_openai import ComposioToolSet, App
from openai import OpenAI
from dotenv import load_dotenv
import os
from autogen import AssistantAgent, UserProxyAgent
from composio_autogen import ComposioToolSet, App


load_dotenv()
openai_client = OpenAI()
composio_toolset = ComposioToolSet()

openai_client.api_key = os.getenv("OPENAI_API_KEY")
tools = composio_toolset.get_tools(apps=[App.GITHUB])

task = "Give me a list of 5 repositories about quant trading"

response = openai_client.chat.completions.create(
model="gpt-4o-mini",
tools=tools,
messages=
    [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": task},
    ],
)

result = composio_toolset.handle_tool_calls(response)
print(result)
