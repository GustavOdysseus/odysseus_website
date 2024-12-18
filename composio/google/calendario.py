from dotenv import load_dotenv
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain import hub
from langchain.agents.loading import load_agent_from_config
from langchain_openai import ChatOpenAI
from composio_langchain import ComposioToolSet
from composio import Action, App



load_dotenv()

llm = ChatOpenAI()
prompt = hub.pull("hwchase17/openai-functions-agent")

composio_toolset = ComposioToolSet(api_key="2nfz9k9ke2hir9bvto33jr")
tools = composio_toolset.get_tools(actions=['GOOGLECALENDAR_GET_CALENDAR'])

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
task = "your task description here"
result = agent_executor.invoke({"input": task})
print(result)