import discord
from discord.ext import commands
from discord import app_commands
import requests
import json

class TeamByNameCog(commands.Cog):
    def __init__(self, bot):
        print("TeamByNameCogLoaded")
        self.bot = bot

    @app_commands.command(name="team-by-name")
    async def teambyname(self, interaction: discord.Interaction, game_name: str,team_name: str):
        team_data = await self.fetch_team_data(game_name,team_name)

        team_name = team_data[0]["name"]
        team_logo = f"https://vrmasterleague.com{team_data[0]["image"]}"
        embed = discord.Embed(
            title=f"{team_name}",
            color=discord.Color.green(),
        ) 
        embed.set_image(url=team_logo)
        await interaction.response.send_message(embed=embed)

    async def fetch_team_data(self, game, team_name):
        try:
            # Build the API URL dynamically based on the game and team
            api_url = f'https://api.vrmasterleague.com/{game}/Teams/Search'
            params = {"name": team_name}
            
            # Print the API URL before making the request
            print(f"Fetching data from URL: {api_url}?name={team_name}")

            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            
            return response.json()
        except Exception as e:
            print(f"Failed to fetch data for team '{team_name}' in game '{game}': {e}")
            return None