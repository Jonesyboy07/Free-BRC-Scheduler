import requests
import json
import os

class PlayerFetcher:
    def __init__(self):
        self.folder_path = "Player_By_ID"  # Folder to store player data
        # Ensure the folder exists
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

    # Function to fetch player data from VR Master League API by player name
    def fetch_player_data_by_name(self, player_name):
        try:
            # Build the API URL dynamically based on the player's name
            api_url = 'https://api.vrmasterleague.com/Players/Search'
            params = {"name": player_name}
            
            # Print the API URL before making the request
            print(f"Fetching data from URL: {api_url}?name={player_name}")

            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data for player '{player_name}': {e}")
            return None

    # Function to fetch player data from VR Master League API by playerID (not userID)
    def fetch_player_data_by_id(self, player_id):
        try:
            # Build the API URL dynamically based on the playerID
            api_url = f'https://api.vrmasterleague.com/Players/{player_id}'
            
            # Print the API URL before making the request
            print(f"Fetching data from URL: {api_url}")

            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data for player ID '{player_id}': {e}")
            return None

    # Function to save player data to a file (Raw JSON)
    def save_player_data_to_file(self, player_name, player_data_combined):
        # Define the file path for saving the combined player data as JSON
        file_path = os.path.join(self.folder_path, f"{player_name}.json")

        # Save the combined player data to the file in JSON format
        with open(file_path, "w") as json_file:
            json.dump(player_data_combined, json_file, indent=4)
        
        print(f"Player data saved to {file_path}")

    # Function to save the formatted player data to a file (Formatted JSON)
    def save_formatted_player_data_to_file(self, player_name, player_data_combined):
        # Create a formatted version of the combined data
        formatted_data = self.format_player_data(player_name, player_data_combined)

        # Define the file path for saving the formatted player data
        formatted_file_path = os.path.join(self.folder_path, f"Formatted_{player_name}.json")

        # Save the formatted data to the file in JSON format
        with open(formatted_file_path, "w") as formatted_json_file:
            json.dump(formatted_data, formatted_json_file, indent=4)
        
        print(f"Formatted player data saved to {formatted_file_path}")

    # Function to format the combined player data (Customize it based on your structure)
    def format_player_data(self, player_name, player_data_combined):
        # Create a clean, formatted version of the combined JSON data
        formatted_data = {
            "player_name": player_name,
            "players": []
        }

        for player_data in player_data_combined:
            formatted_data["players"].append({
                "player_info": {
                    "player_name": player_name,
                    "user_logo": player_data["user"]["userLogo"],
                    "country": player_data["user"]["country"],
                    "nationality": player_data["user"]["nationality"],
                    "date_joined": player_data["user"]["dateJoinedUTC"],
                    "discord_tag": player_data["user"]["discordTag"],
                    "team": {
                        "team_name": player_data["thisGame"]["bioCurrent"]["teamName"],
                        "team_logo": player_data["thisGame"]["bioCurrent"]["teamLogo"]
                    }
                },
                "game_info": {
                    "game_name": player_data["thisGame"]["game"]["gameName"],
                    "team_mode": player_data["thisGame"]["game"]["teamMode"],
                    "match_mode": player_data["thisGame"]["game"]["matchMode"],
                    "game_url": player_data["thisGame"]["game"]["urlComplete"]
                },
                "role_info": {
                    "role": player_data["thisGame"]["bioCurrent"]["role"],
                    "is_team_owner": player_data["thisGame"]["bioCurrent"]["isTeamOwner"],
                    "is_team_starter": player_data["thisGame"]["bioCurrent"]["isTeamStarter"]
                },
                "additional_info": {
                    "stream_url": player_data["user"]["streamUrl"],
                    "steam_id": player_data["user"]["steamID"],
                    "is_terminated": player_data["user"]["isTerminated"]
                }
            })

        return formatted_data

    # Function to print and save the player data response by player name
    def print_and_save_player_data_by_name(self, player_name):
        player_data = self.fetch_player_data_by_name(player_name)

        if player_data:
            if isinstance(player_data, list) and len(player_data) > 0:
                # List to store player data for exact matches
                matching_player_data = []

                # Loop through the players and check for an exact match (case-insensitive)
                for player in player_data:
                    # Check the 'name' key for an exact match (case-insensitive)
                    if player.get("name", "").lower() == player_name.lower():
                        print(f"Found exact match for player '{player_name}' with ID: {player['id']}")
                        player_details = self.fetch_player_data_by_id(player['id'])
                        if player_details:
                            matching_player_data.append(player_details)
                
                if not matching_player_data:
                    print(f"No exact match found for player '{player_name}'.")
                else:
                    # Save the combined data for all matching players in one file
                    self.save_player_data_to_file(player_name, matching_player_data)
                    # Save the formatted data for all matching players in one file
                    self.save_formatted_player_data_to_file(player_name, matching_player_data)
            else:
                print(f"No players found for the name '{player_name}'.")
        else:
            print(f"No data found for player '{player_name}'.")


# Example usage:
if __name__ == "__main__":
    # Allow user to input player name
    player_name = input("Enter the player name: ").strip()

    # Fetch and print the full player data by player name and save to a file
    player_fetcher = PlayerFetcher()
    player_fetcher.print_and_save_player_data_by_name(player_name)
