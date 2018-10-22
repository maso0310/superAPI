#LINE的各種訊息介面



#文字訊息介面TextSendMessage 
def text_message(text1):
    message = TextSendMessage(text=text1)
    return message

#圖片訊息介面ImageSendMessage
def imgmessage(url1,url2):
    message = ImageSendMessage(
        original_content_url='https://example.com/original.jpg',
        preview_image_url='https://example.com/preview.jpg'
    )
    return message

#影片訊息VideoSendMessage
def vedio_message(video_url,picture_url):
    message = VideoSendMessage(
        original_content_url='https://example.com/original.mp4',
        preview_image_url='https://example.com/preview.jpg'
    )
    return message

#確認訊息介面

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


#旋轉木馬按鈕訊息介面

def CarouselTemplate(
    pic1,pic2,
    title1,title2,
    text1,text2,
    postlabel1,postlabel2,
    posttext1,posttext2,
    postdata1,postdata2,
    messagelabel1,messagelabel2,
    messagetext1,messagetext2,
    URIlabel1,URIlabel2,
    URIuri1,URIuri2):
    message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://example.com/item1.jpg',
                    title='this is menu1',
                    text='description1',
                    actions=[
                        PostbackTemplateAction(
                            label='postback1',
                            text='postback text1',
                            data='action=buy&itemid=1'
                        ),
                        MessageTemplateAction(
                            label='message1',
                            text='message text1'
                        ),
                        URITemplateAction(
                            label='uri1',
                            uri='http://example.com/1'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://example.com/item2.jpg',
                    title='this is menu2',
                    text='description2',
                    actions=[
                        PostbackTemplateAction(
                            label='postback2',
                            text='postback text2',
                            data='action=buy&itemid=2'
                        ),
                        MessageTemplateAction(
                            label='message2',
                            text='message text2'
                        ),
                        URITemplateAction(
                            label='uri2',
                            uri='http://example.com/2'
                        )
                    ]
                )
            ]
        )
    )
    return message


