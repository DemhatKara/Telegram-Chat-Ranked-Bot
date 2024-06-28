# Telegram Chat Rank Bot
Telegram bot that tracks message activity in a chat and rewards users with points based on the content and length of their messages. The bot can display the most active users and reset the scoring system on command.

## Features

- Track and score messages in a Telegram chat.
- Award points based on message length and content.
- Display rankings of the most active users.
- Reset the scoring system with a command.

## Scoring System

- Every message gets 1 point.
- Messages starting with `https:` or `http:` get an additional 15 points.
- Messages with less than 15 words get an additional 1 point.
- Messages with 15-24 words get an additional 5 points.
- Messages with 25-34 words get an additional 10 points.
- Messages with 35 or more words get an additional 15 points.

## Commands

- `/start`: Display a welcome message and information about the bot.
- `/rankings`: Display the most active users.
- `/reset`: Reset the scoring system and notify the chat.

## Setup

1. Clone the repository.
2. Install the required dependencies:
    ```bash
    pip install requests
    ```
3. Replace `YOUR_BOT_TOKEN` in the `main.py` file with your Telegram bot token.
4. Run the bot:
    ```bash
    ```

## Usage

Invite telegrambot to your Telegram group and start interacting. Use the provided commands to see the most active users and manage the scoring system.



