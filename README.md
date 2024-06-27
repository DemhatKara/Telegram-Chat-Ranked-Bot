# Telegram Chat Rank Bot

A Telegram bot that counts messages in group chats and ranks users based on their activity.

## Overview

This Telegram bot monitors group chat messages and assigns points based on message activity. It ranks users by the total number of points they accumulate from their messages.

## Features

- Counts messages in group chats.
- Assigns 1 point per regular message.
- Assigns 5 points per message containing a URL (https:// or http://).
- Provides rankings of the most active users in the chat.

## Setup

### Prerequisites

- Python 3.x
- Libraries: aiogram

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DemhatKara/telegram-chat-rank-bot.git
Navigate into the project directory:

bash
Kodu kopyala
cd telegram-chat-rank-bot
Install dependencies:

bash
Kodu kopyala
pip install -r requirements.txt
Configuration
Obtain your Telegram Bot API token from @BotFather.
Replace TOKEN in main.py with your actual bot token.
Usage
Start the bot.
Add it to your Telegram group chat.
Bot will automatically start counting messages and assigning points.
Use /rankings command to see the leaderboard of active users.
Contributing
Contributions are welcome! If you have suggestions, improvements, or bug fixes, feel free to open issues or pull requests.
