from assistant import *

if __name__ == '__main__':
    assistant = Assistant()

    print("success")
    assistant.add_user_message_to_thread("help me to create a lark doc about the content of lark platform, help me to record: 后续如果研发有一些不需要查数据库的非紧急数据，也可以申请一下上面的数据表权限进行查询～目前海外数据库需要每天申请临时权限真的太")
    run = assistant.get_run()
    if run is None:
        print("run is None")


    assistant.execute_run(run)

    response = assistant.get_latest_assistant_message()

    print(response)

    reply_to_user(response)