from telethon import TelegramClient
from config.config import api_id, api_hash

# Create a Telegram client instance
# The 'session_name' parameter is used to save session data, allowing you to reuse it without re-authenticating.
client = TelegramClient('session_name', api_id, api_hash)
