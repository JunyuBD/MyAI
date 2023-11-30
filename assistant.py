import json
import time

import requests
from openai import OpenAI
from open_api import *


open_api_key =  "VQQrT3BlbkFJ1LnHo2salfTFY0q111CO"
class Assistant:
    def __init__(self):
        self.client = self.get_client()
        self.assistant = self.get_assistant()
        self.thread = self.get_thread()

    def get_client(self):
        openai_key = "sk-F0AWaIVJAxhj7UV6"+open_api_key # <--- Your API KEY
        org_ID = "org-optNPL0mDpKx1zJB0tETlz2t"  # <--- Your Organization ID

        client = OpenAI(
            organization=org_ID,
            api_key=openai_key
        )

        return client

    def get_assistant(self):
        assistant = self.client.beta.assistants.retrieve("asst_OoOI3k7xyrBXkj92E3B1dowx")

        return assistant

    def get_thread(self):
        thread = self.client.beta.threads.create()
        return thread

    def get_run(self):
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id
            # instructions=""
        )
        return run

    def add_user_message_to_thread(self, message):
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )

        return message

    def execute_run(self, run):

        i = 0
        print("execute run id is ======== : " + run.id)

        while run.status not in ["completed", "failed"]:
            if i > 0:
                time.sleep(10)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )

            i += 1
            print("***************            "+run.status)

            if run.status == "requires_action":
                print("Action required")
                tools_to_call = run.required_action.submit_tool_outputs.tool_calls
                print(tools_to_call)

                tool_output_array = []
                for each_tool in tools_to_call:
                    tool_call_id = each_tool.id
                    function_name = each_tool.function.name
                    function_arg = each_tool.function.arguments
                    # print("Tool ID: " + tool_call_id)
                    # print("Function to call: " + function_name)
                    # print("Parameters to use: " + function_arg)
                    # print("=============")
                    output = ""
                    # TO DO call the API matching the functionname and return the output
                    if function_name == "create_lark_doc":
                        print("calling create_lark_doc +++++++++++++++")
                        # To Do:  call fetch_userid API and return the userid as output
                        data = json.loads(function_arg)
                        # Use get method to avoid KeyError
                        title_value = data.get('title', 'Default Value')  # You can set a default value

                        # print(title_value)
                        doc_result, doc_link = createLarkDoc(title_value)
                        # print("doc result is " + doc_result)
                        print("doc link:   " + doc_link)
                        output = doc_result + " The sharable doc link is: " + doc_link
                    if function_name == "add_content_to_doc":
                        print("calling add_content_to_doc +++++++++++++++")
                        # To Do:  call fetch_userid API and return the userid as output
                        data = json.loads(function_arg)
                        # Use get method to avoid KeyError
                        document_id = data.get('document_id', 'Default Value')  # You can set a default value
                        content = data.get('content', 'Default')
                        # print(document_id)
                        # print(content)
                        output = insertContentIntoDoc(document_id, content)
                        # print(output)

                    tool_output_array.append({"tool_call_id": tool_call_id, "output": output})

                self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=self.thread.id,
                    run_id=run.id,
                    tool_outputs=tool_output_array
                )
                time.sleep(1)
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=run.id
                )
        return


    def get_latest_assistant_message(self):
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        )

        for each in messages:
            # print(each)
            print(each.role + ": " + each.content[0].text.value)
            print("=========")
            return each.content[0].text.value