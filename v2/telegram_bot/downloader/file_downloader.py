import os
import asyncio
import re
from unzipper.file_processor import process_txt_file
from unzipper.unziper import extract_and_process

async def download_file_with_retries(client, message, channel_data, retries=5):
    """
    File is downloaded from the telegram and that file is changed.
    """
    if message.media and hasattr(message.media, 'document'):
        file_name = message.media.document.attributes[0].file_name
        file_path = f"./downloads/{file_name}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # File is downloaded
        for attempt in range(retries):
            try:
                await client.download_media(message.media.document, file=file_path)
                print(f"File downloaded: {file_name}")
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == retries - 1:
                    raise
                delay = 2 ** attempt  # Eksponentiyal kechikish
                print(f"Waiting for {delay} seconds before next attempt...")
                await asyncio.sleep(delay)

        # All spaces are changed what are located in the text
        sanitized_file_path = file_path.replace(" ", "_")
        if sanitized_file_path != file_path:
            if not os.path.exists(sanitized_file_path):  # Agar nomi mavjud bo'lmasa
                os.rename(file_path, sanitized_file_path)
                file_path = sanitized_file_path

        # Faylga ishlov berish
        if file_name.endswith('.txt'):
            print("Processing .txt file for URLs...")
            process_txt_file(file_path)
            print(f"Processed and deleted .txt file: {file_name}")
            os.remove(file_path)

        elif file_name.endswith('.zip'):
            # 1-step. Unzip without password
            extraction_success = extract_and_process(file_path, password=None)
            if extraction_success:
                print("File extracted successfully without a password.")
            else:
                print("Failed to extract without password. Attempting to find password...")

                # 2-qadam: Agar parolsiz ochilish muvaffaqiyatsiz bo'lsa, parolni olish
                password = channel_data.get('password')  # channel_data'dan parolni olish

                # Agar channel_data'da parol mavjud bo'lmasa, message.text ichidan parolni izlash
                if not password and message.text:
                    # message.text ichidan parolni qidiramiz
                    match = re.search(r'(https?://\S+|@\S+)\b[^\s`]*', message.text, re.IGNORECASE)
                    if match:
                        password = match.group(1)  # Agar matndan parol topilsa, uni oling
                        print(f"Found password in message text: {password}")
                    else:
                        print("No password found in message text.")

                # 3-qadam: Parol bilan yana ochishga urinish
                extraction_success = extract_and_process(file_path, password)
                if extraction_success:
                    print(f"File extracted successfully with password: {password}")
                else:
                    print(f"Extraction failed for {file_name} with password: {password if password else 'None'}")