import json
s = {
    "type": "bubble",
    "header": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "text",
          "text": "幫你大大節省荷包好幫手",
          "weight": "bold",
          "color": "#aaaaaa",
          "size": "sm"
        }
      ]
    },
    "hero": {
      "type": "image",
      "url": "https://i.imgur.com/7cCG7dd.jpg?1",
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "fit",
      "action": {
        "type": "uri",
        "uri": "line://app/1610156977-pYOvGD5v"
      }
    },
    "body": {
      "type": "box",
      "layout": "horizontal",
      "spacing": "md",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "flex": 1,
          "contents": [
            {
              "type": "image",
              "url": "https://i.imgur.com/i51rNfd.jpg",
              "aspectMode": "cover",
              "aspectRatio": "4:3",
              "size": "sm",
              "gravity": "bottom"
            },
            {
              "type": "image",
              "url": "https://i.imgur.com/daZMJPn.jpg",
              "aspectMode": "cover",
              "aspectRatio": "4:3",
              "margin": "md",
              "size": "sm"
            }
          ]
        },
        {
          "type": "box",
          "layout": "vertical",
          "flex": 2,
          "contents": [
            {
              "type": "text",
              "text": "操作步驟教學(電腦介面)",
              "gravity": "top",
              "size": "xs",
              "flex": 1
            },
            {
              "type": "separator"
            },
            {
              "type": "text",
              "text": "1.註冊為Shop.com免費顧客",
              "gravity": "center",
              "size": "xs",
              "flex": 2
            },
            {
              "type": "separator"
            },
            {
              "type": "text",
              "text": "2.用瀏覽器下載ShopBuddy",
              "gravity": "center",
              "size": "xs",
              "flex": 2
            },
            {
              "type": "separator"
            },
            {
              "type": "text",
              "text": "3.若有回饋金將會即刻提醒",
              "gravity": "bottom",
              "size": "xs",
              "flex": 1
            }
          ]
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "立即註冊成為顧客累積回饋金",
            "uri": "line://app/1610156977-YDl9J6O9"
          }
        }
      ]
    }
  }
print(type(s))
j = json.dumps(s)
print(type(j))
print(j)
