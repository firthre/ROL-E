import discord
from discord.ext import commands

# Bot token here
TOKEN = 'xxxxxxxxxxxxxxxx'

# ID of the channel where the bot will post its message
CHANNEL_ID = 1234567890

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Reply to this message with the name of the Linux distribution you use!")

@bot.event
async def on_message(message):
    # If the message is from the bot itself, ignore
    if message.author == bot.user:
        return

    if message.reference:
        referenced_message = await message.channel.fetch_message(message.reference.message_id)
        if referenced_message.author == bot.user:
            # Check if the role already exists
            role = discord.utils.get(message.guild.roles, name=message.content)

            if any(role.name == message.content for role in message.author.roles):
                # If user already has that role, remove
                await message.author.remove_roles(role)
                # Keep this commented to reduce messages?
                #await message.channel.send(f"{message.author.mention} has been removed from the {message.content} role!")
                return

            if role is None:
                # If role does not exist, create it
                role = await message.guild.create_role(name=message.content, reason="New Linux distribution role")

            # Assign the role to the user
            await message.author.add_roles(role)
            await message.channel.send(f"{message.author.mention} has been assigned the {message.content} role!")

bot.run(TOKEN)
