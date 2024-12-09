import discord
from discord.ext import commands
from discord import app_commands
import json
import random
import os

class PingCog(commands.Cog):
    def __init__(self, bot):
        print("PingCogLoaded")
        self.bot = bot

    @app_commands.command(name="ping")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong",ephemeral=True)