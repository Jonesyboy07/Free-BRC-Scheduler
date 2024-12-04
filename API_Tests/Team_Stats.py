import requests
import time

class TeamFetcher:
    def __init__(self):
        pass

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

    # Function to fetch statistics between two teams using their IDs
    def fetch_team_statistics(self, game, team_id1, team_id2):
        try:
            # Build the API URL to get the statistical information between two teams
            api_url = f'https://api.vrmasterleague.com/{game}/Teams/{team_id1}/{team_id2}'

            # Print the API URL before making the request
            print(f"Fetching statistics from URL: {api_url}")

            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            
            return response.json()
        except Exception as e:
            print(f"Failed to fetch statistics between teams '{team_id1}' and '{team_id2}' in game '{game}': {e}")
            return None

    # Function to print the statistics between two teams
    def print_team_statistics(self, game, team_name1, team_name2):
        # Fetch the team data for both teams
        team_data1 = self.fetch_team_data(game, team_name1)
        team_data2 = self.fetch_team_data(game, team_name2)

        if team_data1 and team_data2:
            # Extract the team IDs from the fetched team data
            team_id1 = team_data1[0]['id']  # Assuming the first match is the correct one
            team_id2 = team_data2[0]['id']  # Assuming the first match is the correct one
            
            print(f"Team 1 ID: {team_id1}, Team 2 ID: {team_id2}")
            
            # Fetch the statistical data between the two teams
            stats = self.fetch_team_statistics(game, team_id1, team_id2)

            if stats:
                print(f"Statistics between '{team_name1}' and '{team_name2}':")
                print(stats)  # Print the entire statistics response
            else:
                print(f"No statistical data found between teams '{team_name1}' and '{team_name2}'.")
        else:
            print(f"Failed to fetch data for one or both teams '{team_name1}' and '{team_name2}'.")

# Example usage:
if __name__ == "__main__":
    # Allow user to input game and team names
    game = input("Enter the game name (e.g., onward, breachers): ").strip()
    team_name1 = input("Enter the first team name: ").strip()
    team_name2 = input("Enter the second team name: ").strip()

    # Fetch and print the statistics between the two teams
    team_fetcher = TeamFetcher()
    team_fetcher.print_team_statistics(game, team_name1, team_name2)
