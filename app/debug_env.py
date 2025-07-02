import os
from dotenv import load_dotenv

print("--- STARTING DEBUG SCRIPT ---")
print("Attempting to load .env file...")
load_dotenv()
print(".env file load attempt finished.")

bot_token = os.environ.get("SLACK_BOT_TOKEN")
app_token = os.environ.get("SLACK_APP_TOKEN")

print(f"SLACK_BOT_TOKEN found: {bool(bot_token)}")
print(f"SLACK_APP_TOKEN found: {bool(app_token)}")

if not bot_token or not app_token:
    print("\nERROR: One or more tokens were NOT found. The bot cannot start.")
    print("Please check that your .env file is named correctly and is in the project's root directory.")
else:
    print("\nSUCCESS: Both required tokens were found!")

print("--- DEBUG SCRIPT FINISHED ---")