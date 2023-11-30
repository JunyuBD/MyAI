from assistant import *

if __name__ == '__main__':
    assistant = Assistant()
    while True:


        print("success??")
        assistant.add_user_message_to_thread(" Can you create a doc for me, add some content to it: explain the history of lark and advantages of lark then I can present to my customers?")
        run = assistant.get_run()
        if run is None:
            print("run is None")


        assistant.execute_run(run)


        response = assistant.get_latest_assistant_message()

        print(response)

        # reply_to_user("om_a0c7bcf68f9cc70c06340318c82eb652", response)