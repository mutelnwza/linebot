from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, FollowEvent

import os
import db

from dotenv import load_dotenv


load_dotenv()
app = FastAPI()


ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

print(f"LINE_CHANNEL_ACCESS_TOKEN: {ACCESS_TOKEN}")
print(f"LINE_CHANNEL_SECRET: {CHANNEL_SECRET}")

if not ACCESS_TOKEN or not CHANNEL_SECRET:
    raise ValueError("LINE_CHANNEL_ACCESS_TOKEN or LINE_CHANNEL_SECRET is not set in the environment")

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)



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

# Handle text messages
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id, name = getInfo(event)
    user_message = event.message.text.lower()

    # send image to user
    if user_message == "history":
        return
    
    elif user_message == "send img":
        reply = 'https://i.ibb.co/xcKgTxY/cheems.png'
        line_bot_api.reply_message(
            event.reply_token, ImageSendMessage(original_content_url=reply, preview_image_url=reply)
        )
    # text
    else:
        reply = f"You said: {user_message}"
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text=reply)
        )
    
    db.store_message("user", user_id, name, user_message)
    db.store_message("bot",user_id, name, reply)


# When user adds the bot
@handler.add(FollowEvent)
def follow(event):
    user_id, name = getInfo(event)
    db.store_user_data(user_id, name) #store data of the user


def getInfo(event):
    return event.source.user_id, line_bot_api.get_profile(event.source.user_id).display_name