from pyrogram import Client, filters

# Replace 'API_ID' and 'API_HASH' with your actual values
app = Client("my_bot", api_id="API_ID", api_hash="API_HASH")

@app.on_message(filters.command("start"))
def start(client, message):
    message.reply("Hello! I'm your bot.")

app.run()
