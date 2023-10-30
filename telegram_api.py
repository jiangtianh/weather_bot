import requests
TELEGRAM_BOT_TOKEN = #Your Telegram Bot Token


def send_message(message):
    message_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    params = {
        "chat_id": #Your chat id,
        "text": message
    }
    response = requests.get(message_url, params=params)
    return response.json()


def send_photo(image_path):
    chat_id = "5854619087"
    files = {
        'photo': open(image_path, 'rb')
    }
    message = ('https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendPhoto?chat_id=' + chat_id)
    response = requests.post(message, files=files)
    return response.json()


