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
        user_id = input("Enter the ID of the user you want to send a message to (or 'exit' to quit): ")
        if user_id.lower() == 'exit':
            break

        try:
            user = await bot.fetch_user(int(user_id))
            if user:
                message_content = input("Enter the message you want the bot to send: ")
                await user.send(message_content)
                print(f'Message sent to {user.name} ({user.id})')
            else:
                print('User not found.')
        except discord.NotFound:
            print('User not found.')
        except discord.Forbidden:
            print("The bot doesn't have permission to send direct messages to that user.")

bot.run('MTExMzY0NTAyMzAyMDQ2MjExMQ.GVHsJA.Hs9dezJbFtqna3tL8JZ-lpu2W0p9unvCyHCYak')
