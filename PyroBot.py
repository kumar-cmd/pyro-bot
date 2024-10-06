from pyrogram import Client, filters
import os

# Replace 'API_ID' and 'API_HASH' with your actual values
bot_token = os.environ.get("bot_token")
api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_hash")

# Create the Pyrogram client
app = Client("pyrobot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
def start(client, message):
    message.reply("Hello! I'm your bot.")

# An echo handler that sends back the same message received
@app.on_message(filters.text)
async def echo(client, message):
    await message.reply_text(message.text)
    
app.run()
