#LINE API確認介面訊息

def ConfirmTemplate(label1,label2,text0,text1,text2,data1):

    message = TemplateSendMessage(
        alt_text='Confirm template',
        template=ConfirmTemplate(
            text=text0,
            actions=[
                PostbackTemplateAction(
                    label=label1,
                    text=text1,
                    data=data1
                ),
                MessageTemplateAction(
                    label=label2,
                    text=text2
                )
            ]
        )
    )
    return message