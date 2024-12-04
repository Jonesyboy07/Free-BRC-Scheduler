import requests

class PlayerFetcher:
    def __init__(self):
        pass

    # Function to fetch player data from VR Master League API
    def fetch_player_data(self, player_name):
        try:
            # Build the API URL dynamically based on the player's name
            api_url = f'https://api.vrmasterleague.com/Players/Search'
            params = {"name": player_name}
            
            # Print the API URL before making the request
            print(f"Fetching data from URL: {api_url}?name={player_name}")

            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

            return response.json()
        except Exception as e:
            print(f"Failed to fetch data for player '{player_name}': {e}")
            return None

    # Function to print the entire player data response
    def print_player_data(self, player_name):
        player_data = self.fetch_player_data(player_name)

        if player_data:
            if player_data:  # Check if data is returned
                if isinstance(player_data, list) and len(player_data) > 0:
                    player = player_data[0]  # Assuming the first match is the one we want
                    print(f"Player Data for {player_name}:")
                    print(f"ID: {player['id']}")
                    print(f"Name: {player['name']}")
                    print(f"Image URL: {player['image']}")
                else:
                    print(f"No player found with the name '{player_name}'.")
            else:
                print(f"No data found for player '{player_name}'.")
        else:
            print(f"No data found for player '{player_name}'.")

# Example usage:
if __name__ == "__main__":
    # Allow user to input player name
    player_name = input("Enter the player name: ").strip()

    # Fetch and print the player data
    player_fetcher = PlayerFetcher()
    player_fetcher.print_player_data(player_name)
