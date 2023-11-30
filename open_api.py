import json

import lark_oapi as lark
from lark_oapi.api.docx.v1 import *
from lark_oapi.api.drive.v1 import *
from lark_oapi.api.im.v1 import *
document_link = ""

def reply_to_user(message_id, msg):
    client = lark.Client.builder() \
        .app_id("cli_a5ba31b9a4aad00c") \
        .app_secret("PFMpHuja5Z73ObWH4uyhyeLjn4udject") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()
    text_content = json.dumps({"text": msg})
    # 构造请求对象
    request: ReplyMessageRequest = ReplyMessageRequest.builder() \
        .message_id(message_id) \
        .request_body(ReplyMessageRequestBody.builder()
                      .content(text_content)
                      .msg_type("text")
                      .build()) \
        .build()

    # 发起请求
    response: ReplyMessageResponse = client.im.v1.message.reply(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.reply failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

def updateViewPermission(token):
  # 创建client
    client = lark.Client.builder() \
        .app_id("cli_a5ba31b9a4aad00c") \
        .app_secret("PFMpHuja5Z73ObWH4uyhyeLjn4udject") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: PatchPermissionPublicRequest = PatchPermissionPublicRequest.builder() \
        .token(token) \
        .type("docx") \
        .request_body(PermissionPublicRequest.builder()
            .external_access(True)
            .security_entity("anyone_can_view")
            .comment_entity("anyone_can_view")
            .share_entity("anyone")
            .link_share_entity("anyone_readable")
            .invite_external(True)
            .build()) \
        .build()

    # 发起请求
    response: PatchPermissionPublicResponse = client.drive.v1.permission_public.patch(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.drive.v1.permission_public.patch failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    # lark.logger.info(lark.JSON.marshal(response.data, indent=4))

def insertContentIntoDoc(doc_id, c):
  # 创建client
    client = lark.Client.builder() \
        .app_id("cli_a5ba31b9a4aad00c") \
        .app_secret("PFMpHuja5Z73ObWH4uyhyeLjn4udject") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: CreateDocumentBlockChildrenRequest = CreateDocumentBlockChildrenRequest.builder() \
        .document_id(doc_id) \
        .block_id(doc_id) \
        .document_revision_id(-1) \
        .request_body(CreateDocumentBlockChildrenRequestBody.builder()
            .children([Block.builder()
                .block_type(2)
                .text(Text.builder()
                    .style(TextStyle.builder()
                        .build())
                    .elements([TextElement.builder()
                        .text_run(TextRun.builder()
                            .content(c)
                            .build())
                        .build()
                        ])
                    .build())
                .build()
                ])
            .index(0)
            .build()) \
        .build()


    # 发起请求
    response: CreateDocumentBlockChildrenResponse = client.docx.v1.document_block_children.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.docx.v1.document_block_children.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

    return response.data
def createLarkDoc (title):
  # 创建client
    client = lark.Client.builder() \
        .app_id("cli_a5ba31b9a4aad00c") \
        .app_secret("PFMpHuja5Z73ObWH4uyhyeLjn4udject") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: CreateDocumentRequest = CreateDocumentRequest.builder() \
        .request_body(CreateDocumentRequestBody.builder()
            .title(title)
            .build()) \
        .build()

    # 发起请求
    response: CreateDocumentResponse = client.docx.v1.document.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.docx.v1.document.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    # lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    # print(type(lark.JSON.marshal(response.data, indent=4)))

    document_id = response.data.document.document_id
    print("doc link is :" + "https://bytedance.larkoffice.com/docx/"+document_id)
    updateViewPermission(document_id)
    return lark.JSON.marshal(response.data, indent=4), "https://bytedance.larkoffice.com/docx/"+document_id