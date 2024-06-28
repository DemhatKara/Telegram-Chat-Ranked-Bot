import requests
import re

# Add your bot token here
TOKEN = "YOUR_BOT_TOKEN"
URL = f"https://api.telegram.org/bot{TOKEN}/"

# Dictionaries to track message counts and users
chat_message_counts = {}
user_message_counts = {}

def get_updates(offset=None):
    response = requests.get(URL + "getUpdates", params={"offset": offset})
    return response.json()

def send_message(chat_id, text, is_group=True):
    requests.post(URL + "sendMessage", data={"chat_id": chat_id, "text": text})

def process_message(message):
    chat_id = message["chat"]["id"]
    user_id = message["from"]["id"]
    user_name = message["from"]["username"]
    message_text = message.get("text", "")

    # Analyze the message for scoring
    message_score = 1

    # Messages starting with https: or http: get 15 points
    if re.search(r'https?://', message_text):
        message_score += 15

    # Award points based on word count
    word_count = len(message_text.split())
    if word_count < 15:
        message_score += 1
    elif 15 <= word_count < 25:
        message_score += 5
    elif 25 <= word_count < 35:
        message_score += 10
    elif word_count >= 35:
        message_score += 15

    # Update the message count
    if chat_id in chat_message_counts:
        chat_message_counts[chat_id] += message_score
    else:
        chat_message_counts[chat_id] = message_score

    # Update the user's message count
    if user_id in user_message_counts:
        user_message_counts[user_id]['count'] += message_score
    else:
        user_message_counts[user_id] = {'username': user_name, 'count': message_score}

    # Check user's level and send a message
    current_count = user_message_counts[user_id]['count']
    if current_count % 100 == 0:
        level = current_count // 100
        level_message = f"Thank you for contributing to the Dynamo Community Telegram Channel, @{user_name}! You've advanced to the next chat level: {level}."
        send_message(chat_id, level_message, is_group=True)  # updated to is_group=True

def get_rankings():
    sorted_users = sorted(user_message_counts.items(), key=lambda x: x[1]['count'], reverse=True)
    rankings = "Top active users:\n"
    for rank, (user_id, user_info) in enumerate(sorted_users, start=1):
        rankings += f"{rank}. @{user_info['username']}: {user_info['count']} points\n"
    return rankings

def handle_command(command, chat_id):
    if command == "/start":
        send_message(chat_id, "Hello! I'm your bot. I can track message counts in chats and show the most active users with the /rankings command.")
    elif command == "/rankings":
        rankings = get_rankings()
        send_message(chat_id, rankings)
    elif command == "/reset":
        global chat_message_counts, user_message_counts
        chat_message_counts = {}
        user_message_counts = {}
        send_message(chat_id, "The scoring system has been reset.", is_group=True)

def main():
    update_id = None
    while True:
        updates = get_updates(offset=update_id)
        if updates["ok"]:
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
