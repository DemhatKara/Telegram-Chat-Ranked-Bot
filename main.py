import requests
import re

# Bot tokeninizi buraya ekleyin
TOKEN = "7268649705:AAHQMEaNjSZ_cSnsUj0RhcynEblaNupI-l4"
URL = f"https://api.telegram.org/bot{TOKEN}/"

# Mesaj sayısını ve kullanıcıları takip etmek için sözlükler oluşturun
chat_message_counts = {}
user_message_counts = {}

def get_updates(offset=None):
    response = requests.get(URL + "getUpdates", params={"offset": offset})
    return response.json()

def send_message(chat_id, text):
    requests.post(URL + "sendMessage", data={"chat_id": chat_id, "text": text})

def process_message(message):
    chat_id = message["chat"]["id"]
    user_id = message["from"]["id"]
    user_name = message["from"]["username"]
    message_text = message.get("text", "")

    # Puanlama için mesajı analiz et
    message_score = 1

    # Regex ile mesajda https: veya http: var mı kontrol et
    if re.search(r'https?://', message_text):
        message_score = 5

    # Mesaj sayısını güncelle
    if chat_id in chat_message_counts:
        chat_message_counts[chat_id] += message_score
    else:
        chat_message_counts[chat_id] = message_score

    # Kullanıcı mesaj sayısını güncelle
    if user_id in user_message_counts:
        user_message_counts[user_id]['count'] += message_score
    else:
        user_message_counts[user_id] = {'username': user_name, 'count': message_score}

def get_rankings():
    sorted_users = sorted(user_message_counts.items(), key=lambda x: x[1]['count'], reverse=True)
    rankings = "En aktif kullanıcılar:\n"
    for rank, (user_id, user_info) in enumerate(sorted_users, start=1):
        rankings += f"{rank}. @{user_info['username']}: {user_info['count']} puan\n"
    return rankings

def handle_command(command, chat_id):
    if command == "/start":
        send_message(chat_id, "Merhaba! Ben botunuzdayım. Sohbetlerdeki mesaj sayılarını takip edip, /rankings komutu ile en aktif kullanıcıları gösterebilirim.")
    elif command == "/rankings":
        rankings = get_rankings()
        send_message(chat_id, rankings)

def main():
    update_id = None
    while True:
        updates = get_updates(offset=update_id)
        if updates["result"]:
            for update in updates["result"]:
                update_id = update["update_id"] + 1
                if "message" in update:
                    message = update["message"]
                    if "text" in message:
                        text = message["text"]
                        chat_id = message["chat"]["id"]
                        if text.startswith("/"):
                            handle_command(text, chat_id)
                        else:
                            process_message(message)
                    elif "edited_message" in update:
                        process_message(update["edited_message"])

if __name__ == '__main__':
    main()