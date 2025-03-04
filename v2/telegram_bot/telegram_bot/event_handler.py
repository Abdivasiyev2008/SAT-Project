from telethon import events
from downloader.file_downloader import download_file_with_retries
from database.db_utils import get_channel_data_from_db
from telegram_bot.utils import resolve_channel_ids

async def start_monitoring_channels(client):
    """
    Monitors specified channels for new .zip or .txt files.
    """
    # Kanal ma'lumotlarini olish
    channel_data_list = get_channel_data_from_db()

    if not channel_data_list:
        print("No channel data found in the database. Please check your MongoDB collection.")
        return

    async with client:
        # Kanal usernamesini entity ID ga aylantirish
        resolved_channels = await resolve_channel_ids(client, channel_data_list)

        if not resolved_channels:
            print("No channels resolved. Please check your channel IDs and bot permissions.")
            return

        # Yangi xabarlar uchun eshitish
        @client.on(events.NewMessage(chats=[entity for entity, _ in resolved_channels]))
        async def new_message_handler(event):
            """
            Handles new messages received in monitored channels.
            """
            # Yangilangan kanal ma'lumotlarini olish
            updated_channel_data_list = get_channel_data_from_db()
            channel_data = next((data for data in updated_channel_data_list if 
                                 data['url'].lstrip('@') == event.chat.username or 
                                 data['url'] == event.chat.title), None)

            if channel_data:
                print(f"New message received: {event.message}")
                # Faylni qayta urinish bilan yuklash
                await download_file_with_retries(client, event.message, channel_data)
            else:
                print(f"Channel data for {event.chat.username} not found or updated in the database.")

        print("Monitoring started. Waiting for new files...")
        await client.run_until_disconnected()

