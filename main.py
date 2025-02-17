from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# Webhook endpoint
@app.post("/callback")
async def callback(request: Request):
    # Get signature
    signature = request.headers.get("X-Line-Signature", "")
    
    # Get request body
    body = await request.body()
    body_text = body.decode("utf-8")

    try:
        # Handle webhook
        handler.handle(body_text, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    return "OK"

# Handle text messages
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()

    if user_message == "send img":
        img_url = 'https://i.ibb.co/xcKgTxY/cheems.png'
        line_bot_api.reply_message(
            event.reply_token, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url)
        )
    else:
        reply = f"You said: {user_message}"
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text=reply)
        )