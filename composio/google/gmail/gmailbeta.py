            if action == 'GMAIL_LIST_LABELS':
                  result = self.gmail_api.list_labels()
            elif action == 'GMAIL_SEND_EMAIL':
                result = self.gmail_api.send_email(to='test@example.com', subject='Test Email', body='This is a test email')
            elif action == 'GMAIL_LIST_THREADS':
                result = self.gmail_api.list_threads()
            elif action == 'GMAIL_GET_PROFILE':
                 result = self.gmail_api.get_profile()
            elif action == 'GMAIL_FETCH_MESSAGE_BY_THREAD_ID':
                threads = self.gmail_api.list_threads()
                if threads and threads.get('data') and threads.get('data').get('threads'):
                     thread_id = threads.get('data').get('threads')[0]['id']
                     result = self.gmail_api.fetch_message_by_thread_id(thread_id)
                else:
                    result = "No threads found"
            elif action == 'GMAIL_GET_PEOPLE':
                 result = self.gmail_api.get_people()
            elif action == 'GMAIL_REMOVE_LABEL':
                  threads = self.gmail_api.list_threads()
                  if threads and threads.get('data') and threads.get('data').get('threads'):
                    thread_id = threads.get('data').get('threads')[0]['id']
                    thread = self.gmail_api.fetch_message_by_thread_id(thread_id)
                    if thread and thread.get('data') and thread.get('data').get('messages'):
                      message_id = thread.get('data').get('messages')[0]['id']
                      result = self.gmail_api.remove_label(message_id)
                  else:
                     result = "no threads found"
            elif action == 'GMAIL_ADD_LABEL_TO_EMAIL':
                threads = self.gmail_api.list_threads()
                if threads and threads.get('data') and threads.get('data').get('threads'):
                     thread_id = threads.get('data').get('threads')[0]['id']
                     thread = self.gmail_api.fetch_message_by_thread_id(thread_id)
                     if thread and thread.get('data') and thread.get('data').get('messages'):
                         message_id = thread.get('data').get('messages')[0]['id']
                         result = self.gmail_api.add_label_to_email(message_id)
                else:
                   result = "No threads found"
            elif action == 'GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID':
                 threads = self.gmail_api.list_threads()
                 if threads and threads.get('data') and threads.get('data').get('threads'):
                    thread_id = threads.get('data').get('threads')[0]['id']
                    thread = self.gmail_api.fetch_message_by_thread_id(thread_id)
                    if thread and thread.get('data') and thread.get('data').get('messages'):
                       message_id = thread.get('data').get('messages')[0]['id']
                       result = self.gmail_api.fetch_message_by_message_id(message_id)
                 else:
                     result = "no threads found"

            elif action == 'GMAIL_MODIFY_THREAD_LABELS':
                threads = self.gmail_api.list_threads()
                if threads and threads.get('data') and threads.get('data').get('threads'):
                  thread_id = threads.get('data').get('threads')[0]['id']
                  result = self.gmail_api.modify_thread_labels(thread_id, add_label_ids=['TEST_GMAIL'])
                else:
                   result ="no threads found"
            elif action == 'GMAIL_REPLY_TO_THREAD':
                threads = self.gmail_api.list_threads()
                if threads and threads.get('data') and threads.get('data').get('threads'):
                   thread_id = threads.get('data').get('threads')[0]['id']
                   result = self.gmail_api.reply_to_thread(thread_id, "This is a reply")
                else:
                    result = "no threads found"
            elif action == 'GMAIL_GET_ATTACHMENT':
                threads = self.gmail_api.list_threads()
                if threads and threads.get('data') and threads.get('data').get('threads'):
                    thread_id = threads.get('data').get('threads')[0]['id']
                    thread = self.gmail_api.fetch_message_by_thread_id(thread_id)
                    if thread and thread.get('data') and thread.get('data').get('messages'):
                      message_id = thread.get('data').get('messages')[0]['id']
                      message = self.gmail_api.fetch_message_by_message_id(message_id)
                      if message and message.get('data') and message.get('data').get('payload') and message.get('data').get('payload').get('parts'):
                        for part in message.get('data').get('payload').get('parts'):
                              if part.get('filename') and part.get('body') and part.get('body').get('attachmentId'):
                                   attachment_id = part.get('body').get('attachmentId')
                                   result = self.gmail_api.get_attachment(message_id, attachment_id)
                                   break
                        else:
                            result = {'success':False, "data": "no attachments found"}
                      else:
                        result = {'success':False, "data": "no attachments found"}
                else:
                     result = "no threads found"
            elif action == 'GMAIL_CREATE_LABEL':
                   result = self.gmail_api.create_label('TEST_GMAIL')
            elif action == 'GMAIL_FETCH_EMAILS':
                    result = self.gmail_api.fetch_emails()
            else:
                result = "invalid action"
