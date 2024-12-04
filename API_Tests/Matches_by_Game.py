import os
import requests
import json
from datetime import datetime

class MatchFetcher:
    def __init__(self):
        pass

    # Function to fetch match data from the VR Master League API
    def fetch_match_data(self, game, region=None, filters=None, posMin=1):
        try:
            # Construct the base API URL
            api_url = f'https://api.vrmasterleague.com/{game}/Matches'
            
            # Define query parameters
            params = {}
            if region:
                params['region'] = region
            if filters:
                params['filters'] = filters
            if posMin:
                params['posMin'] = posMin

            # Print the API URL before making the request
            print(f"Fetching data from URL: {api_url} with params: {params}")

            # Make the API request
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            
            return response.json()
        except Exception as e:
            print(f"Failed to fetch match data for game '{game}': {e}")
            return None

    # Function to filter and return upcoming and unscheduled matches
    def filter_upcoming_unscheduled_matches(self, match_data):
        upcoming_matches = match_data.get('matchesScheduledUpcoming', [])
        unscheduled_matches = match_data.get('matchesUnscheduled', [])
        
        return upcoming_matches, unscheduled_matches

    # Function to clean and format match data
    def clean_match_data(self, match_data):
        cleaned_data = []
        
        for match in match_data:
            home_team = match.get("homeTeam", {})
            away_team = match.get("awayTeam", {})
            casting_info = match.get("castingInfo", {})
            
            # Format match data with cleaner fields, including team IDs
            cleaned_match = {
                "matchID": match.get("matchID"),
                "week": match.get("week"),
                "scheduledTime": self.format_scheduled_time(match.get("dateScheduledUTC")),
                "homeTeam": {
                    "teamID": home_team.get("teamID"),
                    "name": home_team.get("teamName"),
                    "division": home_team.get("divisionName"),
                    "logo": home_team.get("teamLogo"),
                },
                "awayTeam": {
                    "teamID": away_team.get("teamID"),
                    "name": away_team.get("teamName"),
                    "division": away_team.get("divisionName"),
                    "logo": away_team.get("teamLogo"),
                },
                "betCounts": {
                    "homeBetCount": match.get("homeBetCount"),
                    "awayBetCount": match.get("awayBetCount"),
                },
                "castUpvotes": match.get("castUpvotes"),
                "isScheduled": match.get("isScheduled"),
                "isChallenge": match.get("isChallenge"),
                "isCup": match.get("isCup"),
                "vodUrl": match.get("vodUrl"),
                "homeHighlights": match.get("homeHighlights"),
                "awayHighlights": match.get("awayHighlights"),
            }
            
            cleaned_data.append(cleaned_match)
        
        return cleaned_data

    # Function to format the scheduled time to a readable format
    def format_scheduled_time(self, scheduled_time):
        try:
            return datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            return None

    # Function to save filtered match data to a JSON file
    def save_filtered_match_data(self, game, upcoming_matches, unscheduled_matches):
        # Create the "Match_By_Game" folder if it doesn't exist
        folder_path = "Match_By_Game"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")
        
        # Define the file path to save the data for upcoming and unscheduled matches
        file_path = os.path.join(folder_path, f"Matches_{game}.json")
        filtered_data = {
            "upcomingMatches": upcoming_matches,
            "unscheduledMatches": unscheduled_matches
        }
        
        # Save the filtered data to the file
        with open(file_path, "w") as json_file:
            json.dump(filtered_data, json_file, indent=4)
            print(f"Filtered match data saved to {file_path}")
        
        # Save cleaner, formatted data to Matches_Filtered_Game.json
        file_path_filtered = os.path.join(folder_path, f"Matches_Filtered_{game}.json")
        
        # Clean and format the upcoming and unscheduled matches
        formatted_upcoming = self.clean_match_data(upcoming_matches)
        formatted_unscheduled = self.clean_match_data(unscheduled_matches)

        cleaned_data = {
            "upcomingMatches": formatted_upcoming,
            "unscheduledMatches": formatted_unscheduled
        }

        # Save the formatted data to a separate file
        with open(file_path_filtered, "w") as json_file_filtered:
            json.dump(cleaned_data, json_file_filtered, indent=4)
            print(f"Formatted match data saved to {file_path_filtered}")

    # Function to fetch, filter, print, clean, and save match data
    def fetch_filter_print_save(self, game, region=None, filters=None, posMin=1):
        match_data = self.fetch_match_data(game, region, filters, posMin)

        if match_data:
            # Filter the matches to get upcoming and unscheduled ones
            upcoming_matches, unscheduled_matches = self.filter_upcoming_unscheduled_matches(match_data)
            
            # Print the filtered data
            print(f"Upcoming Matches for {game}:")
            print(json.dumps(upcoming_matches, indent=4))
            
            print(f"Unscheduled Matches for {game}:")
            print(json.dumps(unscheduled_matches, indent=4))
            
            # Save the filtered match data to a JSON file
            self.save_filtered_match_data(game, upcoming_matches, unscheduled_matches)
        else:
            print(f"No match data found for game '{game}'.")

# Example usage:
if __name__ == "__main__":
    # Allow user to input game name
    game = input("Enter the game name (e.g., onward, breachers): ").strip()

    # Optional: Allow user to filter by region, divisions, and position
    region = input("Enter region (optional, e.g., NA, EU): ").strip() or None
    filters = input("Enter filters (optional, e.g., master, diamond): ").strip() or None
    posMin = int(input("Enter minimum position (default is 1): ").strip() or 1)

    # Fetch, filter, print, and save the match data
    match_fetcher = MatchFetcher()
    match_fetcher.fetch_filter_print_save(game, region, filters, posMin)
