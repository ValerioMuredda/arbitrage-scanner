
from telegram import Bot

# Replace with your actual token and chat_id
BOT_TOKEN = '8012047938:AAFWZuiE9OPSpp-V2O0XNtBbdxrMy3alidzQ'
CHAT_ID = '5197787052'

def send_alert(message):
    try:
        Bot(token=BOT_TOKEN).send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"Telegram error: {e}")
