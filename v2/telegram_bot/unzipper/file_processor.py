import os
import re
import uuid
from datetime import datetime
from pymongo import MongoClient

# MongoDB-ga ulanish
client = MongoClient('mongodb+srv://AdministratorofDB113234:pH9pAEW9PBerB8yG@serverlessinstance0.zjywvmi.mongodb.net/')
db = client['TIdb']
collection = db['leak_leakpassword']

def process_directory(directory):
    """
    Berilgan katalogdagi barcha .txt fayllarni qayta ishlaydi.
    """
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        if os.path.isdir(item_path):
            process_directory(item_path)
        elif item.endswith('.txt'):
            process_txt_file(item_path)
            print(f"✅ Finished processing TXT file: {item_path}")

    try:
        os.rmdir(directory)
        print(f"🗑 Deleted directory: {directory}")
    except Exception as e:
        print(f"⚠ Could not delete directory {directory}: {e}")

def process_txt_file(txt_path):
    """
    Berilgan .txt faylni o‘qiydi va undagi ma'lumotlarni MongoDB-ga qo‘shadi.
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    lines = []

    for encoding in encodings:
        try:
            with open(txt_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
            print(f"📖 Read file with encoding {encoding}: {txt_path}")
            break
        except UnicodeDecodeError:
            continue

    if not lines:
        print(f"⚠ Warning: Could not decode file {txt_path} with provided encodings.")
        return

    # Tuzatilgan regex: URL, username va password aniq ajratiladi
    regex_pattern = r'^(?:https?://)?([a-zA-Z0-9.-]+\.uz):([^:\s]+):([^:\s]+)$'

    added_entries = []
    added_count = 0
    invalid_count = 0

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()

        match = re.match(regex_pattern, line)
        if match:
            url = match.group(1)  # .uz bilan tugaydigan domen
            username = match.group(2)  # Username
            password = match.group(3)  # Password
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            unique_id = str(uuid.uuid4())

            existing_entry = collection.find_one({"url": url, "username": username, "password": password})
            if not existing_entry:
                try:
                    collection.insert_one({
                        "id": unique_id,
                        "url": url,
                        "username": username,
                        "password": password,
                        "time": current_time
                    })
                    added_entries.append(f"{url}:{username}:{password}")
                    added_count += 1
                    print(f"✅ [Line {line_number}] Added to MongoDB: {url}:{username}:{password} at {current_time}")
                except Exception as e:
                    print(f"❌ [Line {line_number}] Error adding to MongoDB: {e}")
            else:
                print(f"⚠ [Line {line_number}] Duplicate entry found, skipping: {url}:{username}:{password}")
        else:
            invalid_count += 1
            print(f"⚠ [Line {line_number}] Invalid format or not a .uz domain, skipping line: {line}")

    try:
        if os.path.exists(txt_path):
            os.remove(txt_path)
            print(f"🗑 Deleted processed TXT file: {txt_path}")
        else:
            print(f"⚠ File not found, could not delete: {txt_path}")
    except Exception as e:
        print(f"❌ Error deleting file: {e}")

    print(f"\n📊 **Processing Summary**")
    print(f"🔹 Total Lines Processed: {len(lines)}")
    print(f"✅ Added: {added_count}")
    print(f"⚠ Skipped (Invalid Format): {invalid_count}")

    if added_entries:
        print("\n📌 **Newly Added Entries:**")
        for entry in added_entries:
            print(f"➕ {entry}")
    else:
        print("\nℹ No new entries were added.")
