from linebot.models import TextSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, MessageAction

def show_menu():
    text = TextSendMessage(text = "วันนี้มีเมนูพิเศษค่ะ! 🍽️ \n🥩 สเต็กเนื้อวากิว ซอสพริกไทยดำ\n🍜 ก๋วยเตี๋ยวต้มยำกุ้งแม่น้ำ \n🍰 ชีสเค้กมะม่วง เมนูของหวานสุดฮิต! \n\nสนใจลองเมนูไหนเป็นพิเศษไหมคะ? 😊")

    carousel_template = TemplateSendMessage(
        alt_text="Menu Options",
        template=CarouselTemplate(columns=[
            CarouselColumn(
                thumbnail_image_url="https://i.imgur.com/hLzCRGO.jpg",
                title="Steak Wagyu Black Pepper",
                text="Juicy steak with black pepper sauce 🥩",
                actions=[MessageAction(label="Order", text="สเต็กเนื้อวากิวซอสพริกไทยดำ")]
            ),
            CarouselColumn(
                thumbnail_image_url="https://i.imgur.com/Z9pLVWU.jpg",
                title="Tom Yum Noodles",
                text="Spicy and flavorful Tom Yum with shrimp 🍜",
                actions=[MessageAction(label="Order", text="ก๋วยเตี๋ยวต้มยำกุ้งแม่น้ำ")]
            ),
            CarouselColumn(
                thumbnail_image_url="https://i.imgur.com/someDessert.jpg",
                title="Mango Cheesecake",
                text="Sweet & creamy mango cheesecake 🍰",
                actions=[MessageAction(label="Order", text="ชีสเค้กมะม่วง")]
            )
        ])
    )
    return text, carousel_template