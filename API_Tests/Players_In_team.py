import os
import requests
import json

class TeamFetcher:
    def __init__(self):
        # Ensure the directory for storing team data exists
        self.directory = 'Team_By_ID'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    # Function to fetch team data from VR Master League API (Search by name)
    def fetch_team_data(self, game, team_name):
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

    # Function to fetch detailed data for a team using the team ID
    def fetch_team_details(self, game, team_id):
        try:
            # Build the API URL to get detailed information about the team
            api_url = f'https://api.vrmasterleague.com/teams/{team_id}'  # Correct endpoint format
            
            # Print the API URL before making the request
            print(f"Fetching detailed data from URL: {api_url}")

            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            
            return response.json()
        except Exception as e:
            print(f"Failed to fetch details for team ID '{team_id}' in game '{game}': {e}")
            return None

    # Function to print player names from the detailed team data
    def print_player_names(self, game, team_name):
        team_data = self.fetch_team_data(game, team_name)

        if team_data:
            print(f"Team Data for {team_name} in {game}:")
            
            # Find a case-insensitive match for the team name
            matched_team = next((team for team in team_data if team['name'].lower() == team_name.lower()), None)

            if matched_team:
                team_id = matched_team['id']
                print(f"Found matching team '{matched_team['name']}' with ID: {team_id}")
                
                # Fetch detailed team information using the team ID
                team_details = self.fetch_team_details(game, team_id)
                if team_details and 'team' in team_details and 'players' in team_details['team']:
                    players = team_details['team']['players']
                    
                    print(f"Player Names in Team '{matched_team['name']}':")
                    for player in players:
                        print(player['playerName'])  # Print the player's name
                else:
                    print(f"Failed to fetch player data for team '{matched_team['name']}'")
            else:
                print(f"No exact match found for team '{team_name}' (case-insensitive).")
        else:
            print(f"No data found for team '{team_name}' in game '{game}'.")

# Example usage:
if __name__ == "__main__":
    # Allow user to input game and team name
    game = input("Enter the game name (e.g., onward, breachers): ").strip()
    team_name = input("Enter the team name: ").strip()

    # Fetch and print the player names
    team_fetcher = TeamFetcher()
    team_fetcher.print_player_names(game, team_name)
