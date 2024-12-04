import os
import requests
import json

class MatchFetcher:
    def __init__(self):
        # Ensure the directory for storing match data exists
        self.directory = 'Match_By_Team'
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

    # Function to recursively search for the upcomingMatches key in the data
    def find_upcoming_matches(self, data):
        matches = []

        # If the data is a dictionary, check if the key is present
        if isinstance(data, dict):
            if "upcomingMatches" in data:
                matches.extend(data["upcomingMatches"])
            
            # Recursively check nested dictionaries or lists
            for key, value in data.items():
                matches.extend(self.find_upcoming_matches(value))
        
        # If the data is a list, check each item
        elif isinstance(data, list):
            for item in data:
                matches.extend(self.find_upcoming_matches(item))

        return matches

    # Function to save the upcoming matches response to a JSON file
    def save_upcoming_matches(self, team_name, upcoming_matches):
        # Create a file path based on team name
        file_path = os.path.join(self.directory, f'{team_name}_upcoming_matches.json')

        try:
            with open(file_path, 'w') as json_file:
                json.dump(upcoming_matches, json_file, indent=4)
            print(f"Upcoming matches data for '{team_name}' has been saved to '{file_path}'")
        except Exception as e:
            print(f"Failed to save upcoming matches for '{team_name}': {e}")

    # Function to fetch team data and save the upcoming matches
    def fetch_and_save_upcoming_matches(self, game, team_name):
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
                if team_details:
                    # Find upcoming matches in the team details
                    upcoming_matches = self.find_upcoming_matches(team_details)
                    if upcoming_matches:
                        # Save the entire upcoming matches response to a JSON file
                        self.save_upcoming_matches(matched_team['name'], upcoming_matches)
                    else:
                        print(f"No upcoming matches found for team '{matched_team['name']}'")
                else:
                    print(f"Failed to fetch detailed information for team '{matched_team['name']}'")
            else:
                print(f"No exact match found for team '{team_name}' (case-insensitive).")
        else:
            print(f"No data found for team '{team_name}' in game '{game}'.")

    # Function to fetch detailed data for a team using the team ID (removed storing team data)
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


# Example usage:
if __name__ == "__main__":
    # Allow user to input game and team name
    game = input("Enter the game name (e.g., onward, breachers): ").strip()
    team_name = input("Enter the team name: ").strip()

    # Fetch and save the upcoming match data
    match_fetcher = MatchFetcher()
    match_fetcher.fetch_and_save_upcoming_matches(game, team_name)
