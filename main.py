import requests
import re


TOKEN = "7268649705:AAHQMEaNjSZ_cSnsUj0RhcynEblaNupI-l4"
URL = f"https://api.telegram.org/bot{TOKEN}/"
#source_channel_id = -1002243664086  # Privet kanalının ID'si
#destination_channel_id = -1002237875985  # dynamotest kanalının ID'si
chat_message_counts = {}
user_message_counts = {}
ranks = [
    (1000, "👑 Legend"),
    (700, "🔥 Supreme"),
    (600, "💎 Elite"),
    (500, "🌟 Pro"),
    (400, "🚀 Achiever"),
    (300, "🎖️ Master"),
    (200, "🏆 Expert"),
    (100, "🥇 Advanced"),
    (50, "🥈 Intermediate"),
]

def get_updates(offset=None):
    response = requests.get(URL + "getUpdates", params={"offset": offset})
    return response.json()

def send_message(chat_id, text, is_group=True):
    requests.post(URL + "sendMessage", data={"chat_id": chat_id, "text": text})

def forward_message(chat_id, from_chat_id, message_id):
    requests.post(URL + "forwardMessage", data={"chat_id": chat_id, "from_chat_id": from_chat_id, "message_id": message_id})

def process_message(message):
    chat_id = message["chat"]["id"]
    user_id = message["from"]["id"]
    user_name = message["from"]["username"]
    message_text = message.get("text", "")


    #if chat_id == source_channel_id:
    # forward_message(destination_channel_id, chat_id, message["message_id"])


    message_score = 1


    if re.search(r'https?://', message_text):
        message_score = 10


    word_count = len(message_text.split())
    if word_count < 15:
        message_score += 1
    elif 15 <= word_count < 25:
        message_score += 5
    elif 25 <= word_count < 35:
        message_score += 10
    elif word_count >= 35:
        message_score += 15


    if chat_id in chat_message_counts:
        chat_message_counts[chat_id] += message_score
    else:
        chat_message_counts[chat_id] = message_score


    if user_id in user_message_counts:
        user_message_counts[user_id]['count'] += message_score
    else:
        user_message_counts[user_id] = {'username': user_name, 'count': message_score}


    current_count = user_message_counts[user_id]['count']
    for points, rank_name in ranks:
        if current_count >= points and current_count - message_score < points:
            level_message = f"Dynamo Community Telegram Kanalına Katkınız için teşekkürler @{user_name}! Sohbet Seviyesi sıralamasında yeni bir rank elde ettiniz: {rank_name}."
            send_message(chat_id, level_message, is_group=True)

def get_rankings():
    sorted_users = sorted(user_message_counts.items(), key=lambda x: x[1]['count'], reverse=True)
    rankings = "En aktif kullanıcılar:\n"
    for rank, (user_id, user_info) in enumerate(sorted_users, start=1):
        current_count = user_info['count']
        current_rank = next((rank_name for points, rank_name in ranks if current_count >= points), "🌱 Başlangıç Seviyesi")
        rankings += f"{rank}. @{user_info['username']}: {current_count} puan - {current_rank}\n"
    return rankings

def get_teamlist():
    teamlist = "Grup Katılımcıları:\n"
    for user_id, user_info in user_message_counts.items():
        teamlist += f"@{user_info['username']}\n"
    return teamlist

def handle_command(command, chat_id):
    global chat_message_counts, user_message_counts
    if command == "/start":
        send_message(chat_id, "Merhaba! Ben botunuzdayım. Sohbetlerdeki mesaj sayılarını takip edip, /rankings komutu ile en aktif kullanıcıları gösterebilirim.")
    elif command == "/rankings":
        rankings = get_rankings()
        send_message(chat_id, rankings)
    elif command == "/dynamoreset":
        chat_message_counts = {}
        user_message_counts = {}
        send_message(chat_id, "Puanlama sistemi sıfırlandı.", is_group=True)
    elif command == "/comlist":  # Değiştirilen komut
        teamlist = get_teamlist()
        send_message(chat_id, teamlist, is_group=True)
    elif command == "/kanalıd":  # Yeni komut
        send_message(chat_id, f"Bu grubun/kanalın ID'si: {chat_id}")

def main():
    update_id = None
    while True:
        updates = get_updates(offset=update_id)
        if updates["ok"] and updates["result"]:
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
