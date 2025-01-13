from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from composio_crewai import ComposioToolSet, Action, App
import logging
import json
import os
import time
import threading
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s')

load_dotenv()

def format_action_input(input_data):
    """Ensure the input is a proper dictionary."""
    if isinstance(input_data, str):
        try:
            return json.loads(input_data)
        except json.JSONDecodeError:
            logging.error("Failed to parse input string as JSON")
            return None
    return input_data

class GmailTestSuite:
    def __init__(self):
        self.composio_toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
        self.all_actions = [
            'GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID',
            'GMAIL_FETCH_MESSAGE_BY_THREAD_ID',
            'GMAIL_LIST_LABELS',
            'GMAIL_GET_PEOPLE',
            'GMAIL_REMOVE_LABEL',
            'GMAIL_ADD_LABEL_TO_EMAIL',
            'GMAIL_LIST_THREADS',
            'GMAIL_MODIFY_THREAD_LABELS',
            'GMAIL_SEND_EMAIL',
            'GMAIL_REPLY_TO_THREAD',
            'GMAIL_GET_PROFILE',
            'GMAIL_GET_ATTACHMENT',
            'GMAIL_CREATE_LABEL',
            'GMAIL_FETCH_EMAILS'
        ]
        self.trigger = None

    def run_test(self, action, description):
        try:
            logging.info(f"\nTesting: {description}")
            tools = self.composio_toolset.get_tools(actions=[action])
            
            # Wrap the tool functions to handle string inputs
            for tool in tools:
                original_func = tool['func']
                tool['func'] = lambda x, f=original_func: f(format_action_input(x))
            
            agent = Agent(
                role="Gmail Assistant",
                goal=f"Process the following Gmail request: {description}",
                backstory="You are an AI agent that manages Gmail operations efficiently. Handle emails, labels, and attachments with care. Always verify recipient addresses and content before sending. IMPORTANT: When providing input to tools, use Python dictionaries instead of JSON strings.",
                verbose=True,
                tools=tools,
                llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
            )
            
            task = Task(
                description=description,
                agent=agent,
                expected_output="Gmail operation result",
                context={"format_instructions": "Return the action input as a Python dictionary, not a JSON string."}
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
            return {"success": False, "error": str(e)}

    def run_all_tests(self):
        results = {}
        
        # Test 1: List Labels
        results['list_labels'] = self.run_test('GMAIL_LIST_LABELS', 
                     "List all labels in my Gmail account")
        
        # Test 2: Send Email
        results['send_email'] = self.run_test('GMAIL_SEND_EMAIL',
                     "Send an email with subject 'Test Email' and body 'This is a test email' to test@example.com")
        
        # Test 3: List Threads
        results['list_threads'] = self.run_test('GMAIL_LIST_THREADS',
                     "List the latest 5 email threads from my inbox")
        
        # Test 4: Get Profile
        results['get_profile'] = self.run_test('GMAIL_GET_PROFILE',
                     "Get my Gmail profile information")
        
        # Test 5: Get message by thread id
        threads = self.run_test('GMAIL_LIST_THREADS', "List threads")
        if isinstance(threads, dict) and 'data' in threads and 'threads' in threads['data'] and threads['data']['threads']:
            thread_id = threads['data']['threads'][0]['id']
            results['fetch_message_by_thread_id'] = self.run_test('GMAIL_FETCH_MESSAGE_BY_THREAD_ID',
                         f"Fetch message by thread id {thread_id}")
        else:
            results['fetch_message_by_thread_id'] = {"success": False, "error": "No threads found"}
        
        # Test 6: Get People
        results['get_people'] = self.run_test('GMAIL_GET_PEOPLE',
                     "Get my people information")
        
        # Test 7: Create label
        results['create_label'] = self.run_test('GMAIL_CREATE_LABEL',
                     "Create a new label named 'TEST_LABEL'")
        
        # Test 8: Add label to email
        if isinstance(threads, dict) and 'data' in threads and 'threads' in threads['data'] and threads['data']['threads']:
            thread = threads['data']['threads'][0]
            results['add_label_to_email'] = self.run_test('GMAIL_ADD_LABEL_TO_EMAIL',
                         f"Add label TEST_LABEL to message {thread['id']}")
        else:
            results['add_label_to_email'] = {"success": False, "error": "No threads found"}
        
        # Test 9: Remove label
        if isinstance(threads, dict) and 'data' in threads and 'threads' in threads['data'] and threads['data']['threads']:
            thread = threads['data']['threads'][0]
            results['remove_label'] = self.run_test('GMAIL_REMOVE_LABEL',
                         f"Remove label TEST_LABEL from message {thread['id']}")
        else:
            results['remove_label'] = {"success": False, "error": "No threads found"}
        
        # Test 10: Modify thread labels
        if isinstance(threads, dict) and 'data' in threads and 'threads' in threads['data'] and threads['data']['threads']:
            thread = threads['data']['threads'][0]
            results['modify_thread_labels'] = self.run_test('GMAIL_MODIFY_THREAD_LABELS',
                         f"Add label IMPORTANT and remove label UNREAD from thread {thread['id']}")
        else:
            results['modify_thread_labels'] = {"success": False, "error": "No threads found"}
        
        # Test 11: Reply to thread
        if isinstance(threads, dict) and 'data' in threads and 'threads' in threads['data'] and threads['data']['threads']:
            thread = threads['data']['threads'][0]
            results['reply_to_thread'] = self.run_test('GMAIL_REPLY_TO_THREAD',
                         f"Reply to thread {thread['id']} with message 'This is a test reply'")
        else:
            results['reply_to_thread'] = {"success": False, "error": "No threads found"}
        
        # Test 12: Get attachment
        if isinstance(threads, dict) and 'data' in threads and 'threads' in threads['data'] and threads['data']['threads']:
            thread = threads['data']['threads'][0]
            results['get_attachment'] = self.run_test('GMAIL_GET_ATTACHMENT',
                         f"Get attachments from message {thread['id']}")
        else:
            results['get_attachment'] = {"success": False, "error": "No threads found"}
        
        # Test 13: Fetch emails
        results['fetch_emails'] = self.run_test('GMAIL_FETCH_EMAILS',
                     "Fetch emails with label INBOX")
        
        # Print summary
        print("\n=== Test Summary ===")
        for test_name, result in results.items():
            success = result.get('success') if isinstance(result, dict) else False
            status = "✅ Success" if success else "❌ Failed"
            print(f"{test_name}: {status}")
        
        return results

    def setup_trigger(self, interval=1, userid='me', labelids=['INBOX']):
        """Configure and start the Gmail trigger"""
        self.trigger = GmailTrigger(
            interval=interval,
            userid=userid,
            labelids=labelids,
            composio_toolset=self.composio_toolset
        )
        self.trigger.start()

    def stop_trigger(self):
        """Stop the Gmail trigger if it's running"""
        if self.trigger:
            self.trigger.stop()


class GmailTrigger:
    def __init__(self, interval=1, userid='me', labelids=['INBOX'], composio_toolset=None):
        self.interval = interval
        self.userid = userid
        self.labelids = labelids
        self.composio_toolset = composio_toolset
        self.running = False
        self.thread = None
        self.last_check_time = datetime.now()

    def start(self):
        """Start the trigger monitoring"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._monitor)
            self.thread.start()
            logging.info("Gmail trigger started")

    def stop(self):
        """Stop the trigger monitoring"""
        self.running = False
        if self.thread:
            self.thread.join()
            logging.info("Gmail trigger stopped")

    def _monitor(self):
        """Monitor Gmail for new messages"""
        while self.running:
            try:
                self._check_new_emails()
                time.sleep(self.interval * 60)  # Convert minutes to seconds
            except Exception as e:
                logging.error(f"Error in Gmail trigger: {str(e)}")

    def _check_new_emails(self):
        """Check for new emails using GMAIL_FETCH_EMAILS action"""
        try:
            tools = self.composio_toolset.get_tools(actions=['GMAIL_FETCH_EMAILS'])
            
            # Wrap the tool functions to handle string inputs
            for tool in tools:
                original_func = tool['func']
                tool['func'] = lambda x, f=original_func: f(format_action_input(x))
            
            agent = Agent(
                role="Gmail Monitor",
                goal="Monitor Gmail inbox for new messages",
                backstory="You are an AI agent that monitors Gmail for new messages and processes them according to specified labels. IMPORTANT: When providing input to tools, use Python dictionaries instead of JSON strings.",
                verbose=True,
                tools=tools,
                llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
            )
            
            task = Task(
                description=f"Check for new emails in labels: {', '.join(self.labelids)}",
                agent=agent,
                context={"format_instructions": "Return the action input as a Python dictionary, not a JSON string."}
            )
            
            crew = Crew(
                agents=[agent],
                tasks=[task]
            )
            
            result = crew.kickoff()
            self._process_new_emails(result)
            self.last_check_time = datetime.now()
        except Exception as e:
            logging.error(f"Error checking new emails: {str(e)}")

    def _process_new_emails(self, result):
        """Process any new emails found"""
        try:
            logging.info("Starting to process new emails")
            
            if not result:
                logging.warning("No result received from email fetch")
                return
                
            if isinstance(result, str):
                logging.info(f"Received string result: {result[:200]}...")  # Log only first 200 chars
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    logging.error("Failed to parse string result as JSON")
                    return
            
            if not isinstance(result, dict):
                logging.error(f"Unexpected result type: {type(result)}")
                return
                
            # Log the structure of the result
            logging.info(f"Result structure: {list(result.keys()) if isinstance(result, dict) else 'not a dict'}")
            
            if 'data' in result and 'messages' in result['data']:
                messages = result['data']['messages']
                logging.info(f"Found {len(messages)} new messages")
                
                for message in messages:
                    try:
                        message_id = message.get('id')
                        if not message_id:
                            continue
                            
                        logging.info(f"Processing message ID: {message_id}")
                        # Adicione aqui a lógica de processamento específica para cada mensagem
                        
                    except Exception as e:
                        logging.error(f"Error processing individual message: {str(e)}")
                        continue
            else:
                logging.warning("No messages found in the result structure")
                
        except Exception as e:
            logging.error(f"Error in _process_new_emails: {str(e)}")
            # Log the full error traceback for debugging
            import traceback
            logging.error(traceback.format_exc())


if __name__ == "__main__":
    test_suite = GmailTestSuite()
    
    # Executar todos os testes
    results = test_suite.run_all_tests()
    
    # Configurar e iniciar o trigger (opcional)
    # test_suite.setup_trigger(interval=1, labelids=['INBOX'])
    
    # Para parar o trigger mais tarde:
    # test_suite.stop_trigger()
