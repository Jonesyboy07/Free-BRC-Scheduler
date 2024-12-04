import requests
import time

class TeamFetcher:
    def __init__(self):
        pass

    # Function to fetch team data from VR Master League API
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

    # Function to print the entire team data response
    def print_team_data(self, game, team_name):
        team_data = self.fetch_team_data(game, team_name)

        if team_data:
            print(f"Team Data for {team_name} in {game}:")
            print(team_data)  # Print the entire response (as a dictionary)
        else:
            print(f"No data found for team '{team_name}' in game '{game}'.")

# Example usage:
if __name__ == "__main__":
    # Allow user to input game and team name
    game = input("Enter the game name (e.g., onward, breachers): ").strip()
    team_name = input("Enter the team name: ").strip()

    # Fetch and print the team data
    team_fetcher = TeamFetcher()
    team_fetcher.print_team_data(game, team_name)


