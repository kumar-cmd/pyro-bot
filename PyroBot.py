from pyrogram import Client, filters

# Replace 'API_ID' and 'API_HASH' with your actual values
bot_token = '6850047081:AAGYb8GOGhndbyN4tRCtXmdjdheHtxVVjXBg'
api_id = 2645433743
api_hash = "aff31ed425563fcc8f5fjdjdtd4410d98"

# Create the Pyrogram client
app = Client("pyrobot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
def start(client, message):
    message.reply("Hello! I'm your bot.")

app.run()
