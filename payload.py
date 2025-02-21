from linebot.models import *

def show_menu():
    text = TextSendMessage(text = "เมนูแนะนำของเรา! 🍽️ \n🥩 สเต็กเนื้อวากิว ซอสพริกไทยดำ\n🍜 ก๋วยเตี๋ยวต้มยำกุ้งแม่น้ำ \n🍰 ชีสเค้กมะม่วง เมนูของหวานสุดฮิต! \n\nสนใจลองเมนูไหนเป็นพิเศษไหมคะ? 😊")

    carousel_template = TemplateSendMessage(
        alt_text="Menu Options",
        template=CarouselTemplate(columns=[
            CarouselColumn(
                thumbnail_image_url="https://i.ibb.co/QjrCHHBx/photo.jpg",
                title="Steak Wagyu Black Pepper",
                text="Juicy steak with black pepper sauce 🥩",
                actions=[MessageAction(label="Order", text="สเต็กเนื้อวากิวซอสพริกไทยดำ")]
            ),
            CarouselColumn(
                thumbnail_image_url="https://i.ibb.co/hJFgT8Fd/Konjam-Shrimp-Tom-Yum-Noodles-scaled.jpg",
                title="Tom Yum Noodles",
                text="Spicy and flavorful Tom Yum with shrimp 🍜",
                actions=[MessageAction(label="Order", text="ก๋วยเตี๋ยวต้มยำกุ้งแม่น้ำ")]
            ),
            CarouselColumn(
                thumbnail_image_url="https://i.ibb.co/tpsjPWf8/souffle-cheesecake-00-1024x576.jpg",
                title="Mango Cheesecake",
                text="Sweet & creamy mango cheesecake 🍰",
                actions=[MessageAction(label="Order", text="ชีสเค้กมะม่วง")]
            )
        ])
    )
    return text, carousel_template


def order_confirm(user_sessions, user_id):

    order_sum = TextSendMessage(text="ออเดอร์ของคุณคือ \n" + "\n".join([f"{item['order']} จำนวน {item['amount']}" for item in user_sessions[user_id]["orders"]]))

    
    confirm_template = TemplateSendMessage(
        alt_text="Order Confirmation",
        template= ConfirmTemplate
        (
            text = "คลิกเพื่อยืนยันหรือยกเลิกคำสั่งซื้อ",
            actions=[MessageAction(label="ยืนยัน", text="ยืนยันออเดอร์"), MessageAction(label="ยกเลิก", text="ยกเลิก")]
        )
    )

    return order_sum, confirm_template


def confirm_or_cancel(text, user_sessions, user_id):
    template = TemplateSendMessage(
        alt_text= "Confirm",
        template = ButtonsTemplate(
            title=text,
            text= "กรุณายืนยันความถูกต้อง",
            actions=[
                MessageAction(label = "ข้อมูลถูกต้อง", text =f"ยืนยัน"),
                MessageAction(label = "แก้ไขข้อมูล", text = f"แก้ไข"),
                MessageAction(label = "ยกเลิกการสั่งอาหาร", text = "ยกเลิกออเดอร์ทั้งหมด")
            ]
        )
    )
    return template