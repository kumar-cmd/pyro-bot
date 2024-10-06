from pyrogram import Client, filters
from PIL import Image, ImageDraw, ImageFont
import textwrap
import seaborn as sns
import random
from io import BytesIO
import os
import asyncio




colors = sns.color_palette('dark', 10)  # You can choose any other palette as well

def select_random_color():
    """Select a random color from the Seaborn tab10 color palette."""
    color = random.choice(colors)
    return tuple([int(c * 255) for c in color])



def create_graphics(logo_path, quote, footer_text):
    # Load the logo image
    logo = Image.open(logo_path).convert("RGBA")

    # Resize the logo to a specific width while maintaining the aspect ratio
    logo_width = 150  # Desired width of the logo
    aspect_ratio = logo.height / logo.width
    logo_height = int(logo_width * aspect_ratio)
    logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

    # Create a font for the quote and footer
    quote_font = ImageFont.truetype("NotoSansDevanagari-Regular.ttf", 40)
    footer_font = ImageFont.truetype("NotoSansDevanagari-Regular.ttf", 32)

    # Wrap the quote text using textwrap
    wrapped_quote = textwrap.fill(quote, width=40)  # Wrap text to 40 characters width
    wrapped_quote_lines = wrapped_quote.split('\n')

    # print(wrapped_quote, wrapped_quote_lines)

    # Calculate the total height required for the wrapped quote
    quote_height = sum([ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox((0,0), line, font=quote_font)[3] for line in wrapped_quote_lines])
    # print(quote_height)

    # Set the base height and increase it based on the quote height
    base_height = logo_height + 100  # Base height to accommodate logo and some padding
    graphics_height = base_height + quote_height + 220  # Extra space for the quote
    # print(graphics_height, base_height, quote_height)
    # Create a new image for the graphics
    graphics_width = 800  # Set a fixed width for the graphics
    graphics = Image.new("RGBA", (graphics_width, graphics_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(graphics)

    # Paste the logo at the top-left corner
    graphics.paste(logo, (20, 20))  # Add some padding

    color = select_random_color()
    # Draw the wrapped quote in the center
    quote_y = logo_height + 50  # Position the quote below the logo
    for line in wrapped_quote_lines:
        draw.text((logo_width*0.8, quote_y), line, font=quote_font, fill="black")
        quote_y += draw.textbbox((0,0), line, font=quote_font)[3]+20   # Move down to the next line

    # # Wrap the footer text using textwrap
    # wrapped_footer = textwrap.fill(footer_text, width=40)  # Wrap footer text
    wrapped_footer_lines = footer_text # wrapped_footer.split('\n')

    # Draw the footer at the bottom right
    footer_y = graphics_height - (len(wrapped_footer_lines) * draw.textbbox((0,0), wrapped_footer_lines[0], font=footer_font)[3]) - 40   # Padding from bottom
    for line in wrapped_footer_lines:
        footer_x = graphics_width - draw.textbbox((0,0), line, font=footer_font)[0] - 250  # Padding
        draw.text((footer_x, footer_y), line, font=footer_font, fill="gray")
        footer_y += draw.textbbox((0,0), line, font=footer_font)[3]*1.3  # Move down to the next line

    output_io = BytesIO()
    graphics.save(output_io, format="PNG")
    output_io.seek(0)  # Move the cursor to the beginning of the BytesIO stream

    return output_io





# Replace 'API_ID' and 'API_HASH' with your actual values
bot_token = os.environ.get("bot_token")
api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_hash")

# Create the Pyrogram client
app = Client("pyrobot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

colors = sns.color_palette('deep', 10)  # You can choose any other palette as well

def select_random_color():
    """Select a random color from the Seaborn tab10 color palette."""
    return random.choice(colors)


# A simple command to start the bot and greet the user
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(f"Hello, {message.from_user.first_name}! I'm your bot.")


@app.on_message(filters.command("p"))
async def generate_image(client, message):
    # Get the input text from the message
    txt = message.text.split(' ', 1)[1] # Extract text after the command
    
    if not txt:
        await message.reply_text("Please provide text for the image. Usage: /jpegimage your_text")
        return

    await message.reply_text(f"1")

    logo_path = "logo.png"  # Path to your logo image
    footer_text = ["आदि शंकराचार्य, ", "निश्चलानंद सरस्वती"]
    await message.reply_text(f"2")
    image_io = create_graphics(logo_path, txt, footer_text)

    # Send the image to the user
    await message.reply_text(f"Hello, sending photo")
    await client.send_photo(message.chat.id, photo=image_io)


# # An echo handler that sends back the same message received
# @app.on_message(filters.text)
# async def echo(client, message):
#     await message.reply_text(message.text)

# Handler to detect when a voice chat starts
@app.on_message(filters.video_chat_started)
async def on_voice_chat_started(client, message):
    chat_id = message.chat.id
    await message.reply(f"Voice chat started in {message.chat.title}!")
    # print(f"Voice chat started in {message.chat.title} (ID: {chat_id})")

# Handler to detect when a voice chat ends
@app.on_message(filters.video_chat_ended)
async def on_voice_chat_ended(client, message):
    chat_id = message.chat.id
    await message.reply(f"Voice chat ended in {message.chat.title}.")
    # print(f"Voice chat ended in {message.chat.title} (ID: {chat_id})")

@app.on_message(filters.video_chat_members_invited)
async def members_invited(client, message):
    chat_id = message.chat.id
    inviter = message.from_user.first_name if message.from_user else "Unknown"

    # List of invited members
    invited_members = [user.first_name for user in message.video_chat_members_invited]

    # Notify who invited whom
    await message.reply_text(f"Hello, sending invited info")
    await message.chat.send_message(f"{inviter} invited: {', '.join(invited_members)} to the video chat.")
   

app.run()

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))  # Use the PORT environment variable
#     app.run(port=port)
    
