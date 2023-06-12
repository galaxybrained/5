import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

    while True:
        message_content = input("Enter the message you want the bot to send (or 'exit' to quit): ")
        if message_content.lower() == 'exit':
            break

        channel_id = 1113661118527848471  # Replace with the desired channel ID

        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(message_content)
            print('Message sent!')
        else:
            print(f'Channel with ID {channel_id} not found.')

bot.run('1113661118527848468')

