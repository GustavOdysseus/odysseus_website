import os
import dotenv
from composio_langchain import Action, ComposioToolSet
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain import hub


dotenv.load_dotenv()
composio_toolset = ComposioToolSet()
gmail_tools = composio_toolset.get_actions(actions=[Action.GMAIL_SEND_EMAIL])
llm = ChatOpenAI(model="gpt-4omini", openai_api_key=os.getenv("OPENAI_API_KEY"))
gmail_send_email = "YOUR_EMAIL_KEY"

prompt = hub.pull("hwchase17/openai-functions-agent")
agent = create_openai_functions_agent(llm, gmail_tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=gmail_tools, verbose=True)

email_task = """
Send an email to liminaught@gmail.com with the subject 'Test Email' and the body 'Hello.'
"""
result = agent_executor.invoke({"input": email_task})
print(result)
