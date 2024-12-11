from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain import hub
from langchain_openai import ChatOpenAI
from composio_langchain import ComposioToolSet, Action, App
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_client = OpenAI()
llm = ChatOpenAI()
prompt = hub.pull("hwchase17/openai-functions-agent")
openai_client.api_key = os.getenv("OPENAI_API_KEY")

composio_toolset = ComposioToolSet(api_key="2nfz9k9ke2hir9bvto33jr")
tools = composio_toolset.get_tools(actions=['GITHUB_SEARCH_TOPICS'])

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
task = "Find for me the 5 githubs repo with the most commits about quant trading"
result = agent_executor.invoke({"input": task})
print(result)