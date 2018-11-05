#10層旋轉木馬訊息
#lineAPI
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

def Ten_Carousel_Template(
    img_url1_1,title1_1,text1_1,label1_4,url1_4,
    img_url2_1,title2_1,text2_1,label2_4,url2_4,
    img_url3_1,title3_1,text3_1,label3_4,url3_4,
    img_url4_1,title4_1,text4_1,label4_4,url4_4,
    img_url5_1,title5_1,text5_1,label5_4,url5_4,
    img_url6_1,title6_1,text6_1,label6_4,url6_4,
#    img_url7_1,title7_1,text7_1,label7_4,url7_4
#    img_url8_1,title8_1,text8_1,label8_3,text8_3,label8_4,url8_4,
#    img_url9_1,title9_1,text9_1,label9_3,text9_3,label9_4,url9_4,
#    img_url10_1,title10_1,text10_1,label10_3,text10_3,label10_4,url10_4
):
    message = TemplateSendMessage(
        alt_text='請查看手機的訊息',
        template=CarouselTemplate(
            imageAspectRatio='square',
            imageSize='cover',
            imageBackgroundColor= "#a8e8fb",
            columns=[
                CarouselColumn(
                    thumbnail_image_url=img_url1_1,
                    title=title1_1,
                    text=text1_1,
                    actions=[
                        URITemplateAction(
                            label=label1_4,
                            uri=url1_4
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=img_url2_1,
                    title=title2_1,
                    text=text2_1,
                    actions=[
                        URITemplateAction(
                            label=label2_4,
                            uri=url2_4
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=img_url3_1,
                    title=title3_1,
                    text=text3_1,
                    actions=[
                        URITemplateAction(
                            label=label3_4,
                            uri=url3_4
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=img_url4_1,
                    title=title4_1,
                    text=text4_1,
                    actions=[
                        URITemplateAction(
                            label=label4_4,
                            uri=url4_4
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=img_url5_1,
                    title=title5_1,
                    text=text5_1,
                    actions=[
                        URITemplateAction(
                            label=label5_4,
                            uri=url5_4
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=img_url6_1,
                    title=title6_1,
                    text=text6_1,
                    actions=[
                        URITemplateAction(
                            label=label6_4,
                            uri=url6_4
                        )
                    ]
                )
            ]
        )
    )
    return message