

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, ImageSendMessage, FollowEvent, MessageEvent, TextMessage

import os
import db, payload

import just_checking

from dotenv import load_dotenv


load_dotenv()
app = FastAPI()


ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

user_sessions = {}

class WebhookRequest(BaseModel):
    responseId: str
    queryResult: dict
    originalDetectIntentRequest: dict

print(f"LINE_CHANNEL_ACCESS_TOKEN: {ACCESS_TOKEN}")
print(f"LINE_CHANNEL_SECRET: {CHANNEL_SECRET}")

if not ACCESS_TOKEN or not CHANNEL_SECRET:
    raise ValueError("LINE_CHANNEL_ACCESS_TOKEN or LINE_CHANNEL_SECRET is not set in the environment")

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
menu_text, menu_carousel = payload.show_menu()
parser = WebhookParser(CHANNEL_SECRET)


# Webhook endpoint
@app.post("/callback")
async def callback(request: Request):
    signature = request.headers.get("X-Line-Signature", "")
    body = await request.body()
    body_text = body.decode("utf-8")

    try:
        handler.handle(body_text, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
    return "OK"


@app.post("/webhook")
async def webhook(request: Request):
    global user_sessions
    req = await request.json()

    just_checking.formatjson(req, "userinput") # view json

    intent_name = req["queryResult"]["intent"]["displayName"]
    user_id = req["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    reply_token = req["originalDetectIntentRequest"]["payload"]["data"]["replyToken"]


    # Menu recommendation
    if intent_name == "Menu Recommendation":
        line_bot_api.reply_message(reply_token, [menu_text, menu_carousel]) #send the menu
        return {"fulfillmentText": "Showing menu"}

    # Food Order
    elif intent_name == "Order":
        if user_id not in user_sessions:
            user_sessions[user_id] = {"name": None, "phone": None, "orders": []}

        for i in range(len(req["queryResult"]["parameters"]["food"])):
            order = req["queryResult"]["parameters"]["food"][i]
            amount = int(req["queryResult"]["parameters"]["amount"][i])

            user_sessions[user_id]["orders"].append({"order": order, "amount": amount})

        order_sum, reply = payload.order_confirm(user_sessions, user_id)
        line_bot_api.reply_message(reply_token, [order_sum,reply])

        return {"fulfillmentText": "Order added"}
    
    # Cancel all orders
    elif intent_name == "Order - no" or intent_name == "GetName - cancel":
        user_sessions.pop(user_id,None)
        line_bot_api.reply_message(reply_token, TextSendMessage(text = "ยกเลิกออเดอร์ของคุณแล้ว หากต้องการสั่งเมนูเพิ่มเติมสามารถแจ้งได้เลยนะคะ"))

    # Get name and phone
    elif intent_name == "GetName":
        user_name=req["queryResult"]["parameters"]["name"]
        phone=req["queryResult"]["parameters"]["phone"]

        user_sessions[user_id]["name"] = user_name
        user_sessions[user_id]["phone"] = phone

        text = f"ชื่อของคุณคือ {user_name} โทร {phone}"

        line_bot_api.reply_message(reply_token, payload.confirm_or_cancel(text, user_sessions, user_id))

        return {"fulfillmentText": f"บันทึกชื่อ: {user_name} เบอร์โทร : {phone}"}


    # After user confirms name and phone
    elif intent_name == "GetName - yes":
        name = user_sessions[user_id]["name"]
        phone = user_sessions[user_id]["phone"]

        user_sessions.pop(user_id,None) # pop out the data

        line_bot_api.reply_message(reply_token, TextSendMessage(text= f"บันทึกชื่อ: {name} เบอร์โทร : {phone} ขอบคุณสำหรับการสั่งจอง"))


# Handle text messages
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     user_id, name = getInfo(event)
#     user_message = event.message.text.lower()

#     if user_message == "send img":
#         reply = 'https://i.ibb.co/xcKgTxY/cheems.png'
#         line_bot_api.reply_message(
#             event.reply_token, ImageSendMessage(original_content_url=reply, preview_image_url=reply)
#         )
#     # text
#     else:
#         reply = f"You said: {user_message}"
#         line_bot_api.reply_message(
#             event.reply_token,TextSendMessage(text=reply))
    
#     # db.store_message("user", user_id, name, user_message)
#     # db.store_message("bot",user_id, name, reply)


def getInfo(event):
    return event.source.user_id, line_bot_api.get_profile(event.source.user_id).display_name