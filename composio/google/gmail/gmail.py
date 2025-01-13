from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from composio_crewai import ComposioToolSet, Action, App
import logging
import json
import os
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s')

load_dotenv()

class GmailTestSuite:
    def __init__(self):
        self.composio_toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
        self.all_actions = [
            'GMAIL_SEND_EMAIL',
            'GMAIL_LIST_LABELS',
            'GMAIL_GET_PROFILE',
            'GMAIL_LIST_MESSAGES',
            'GMAIL_GET_MESSAGE',
            'GMAIL_FETCH_EMAILS'
        ]

    def run_test(self, action, description):
        try:
            logging.info(f"\nTesting: {description}")
            tools = self.composio_toolset.get_tools(actions=[action])
            
            agent = Agent(
                role="Gmail Assistant",
                goal=f"Process the following Gmail request: {description}",
                backstory="You are an AI agent that manages Gmail operations efficiently. Handle emails, labels, and attachments with care. When using tools, always pass parameters as a Python dictionary, not as a JSON string.",
                verbose=True,
                tools=tools,
                llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
            )
            
            task = Task(
                description=description,
                agent=agent,
                expected_output="Gmail operation result"
            )
            
            crew = Crew(
                agents=[agent],
                tasks=[task]
            )
            
            result = crew.kickoff()
            logging.info(f"Success: {action}")
            print(f"\nResponse: {result}")
            return result
        except Exception as e:
            logging.error(f"Error in {action}: {str(e)}")
            return f"Error: {str(e)}"

    def test_list_labels(self):
        """Teste específico para listar labels"""
        return self.run_test('GMAIL_LIST_LABELS', 
            "List all Gmail labels")

    def test_get_profile(self):
        """Teste específico para obter perfil"""
        return self.run_test('GMAIL_GET_PROFILE',
            "Get my Gmail profile information")

    def test_send_email(self):
        """Teste específico para enviar email"""
        return self.run_test('GMAIL_SEND_EMAIL',
            "Send an email to test@example.com with subject 'Test Email' and body 'This is a test email'")

    def run_all_tests(self):
        results = {}
        
        # Teste específico para listar labels
        results['list_labels'] = self.test_list_labels()
        
        # Teste específico para obter perfil
        results['get_profile'] = self.test_get_profile()
        
        # Teste específico para enviar email
        results['send_email'] = self.test_send_email()
        
        # Print summary
        print("\n=== Test Summary ===")
        for test_name, result in results.items():
            success = "Error" not in str(result)
            status = " Success" if success else " Failed"
            print(f"{test_name}: {status}")

if __name__ == "__main__":
    test_suite = GmailTestSuite()
    
    # Testar apenas envio de email
    test_suite.test_send_email()
