import asyncio
from telegram_bot.client import client
from telegram_bot.event_handler import start_monitoring_channels

# Entry point of the script
if __name__ == "__main__":
    # Starts monitoring channels for new messages containing .zip or .txt files
    asyncio.run(start_monitoring_channels(client))
