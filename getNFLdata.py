import requests
from datetime import datetime, timedelta

def fetch_game_details(game_url):
    game_response = requests.get(game_url)
    if game_response.status_code == 200:
        return game_response.json()
    else:
        return None

def fetch_game_odds(odds_url):
    odds_response = requests.get(odds_url)
    if odds_response.status_code == 200:
        return odds_response.json()
    else:
        return None
    
def reformat_NFL_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%MZ')
    new_date_obj = date_obj - timedelta(hours=7)
    return new_date_obj.strftime('%m/%d %I:%M %p')

def get_team_logos():
    logoMap = {}
    url = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams'
    response = requests.get(url)
    data = response.json()
    for team in data['sports'][0]['leagues'][0]['teams']:
        logoMap[team['team']['abbreviation']] = team['team']['logos'][0]['href']
    return logoMap

def is_game_today_or_in_future(date_str):
    game_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%MZ')
    current_utc_time = datetime.utcnow()
    
    return game_date >= current_utc_time
    
def format_NFL_json(seasonYear, seasonType, weekNum):
    # Fetch team logos
    team_logos = get_team_logos()

    # TODO: implement logic to update seasonType and weekNum based on current date

    gamesURL = f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{seasonYear}/types/{seasonType}/weeks/{weekNum}/events"
    response = requests.get(gamesURL)
    data = response.json()
    
    if seasonType == 1:
        seasonTypeName = 'Preseason'
    elif seasonType == 2:
        seasonTypeName = 'Regular Season'
    elif seasonType == 3:
        seasonTypeName = 'Postseason'

    all_games = []

    # Loop through each game reference
    for game_ref in data['items']:
        game_url = game_ref['$ref']
        game_data = fetch_game_details(game_url)
        
        if game_data:
            game_date_str = game_data.get('date', 'N/A')
            
            if is_game_today_or_in_future(game_date_str):
                short_name = game_data.get('shortName', 'N/A')
                
                game_date = reformat_NFL_date(game_date_str)
                
                
                # Extract home and away team abbreviations
                if 'VS' in short_name:
                    home_team, away_team = short_name.split(' VS ')
                else:
                    away_team, home_team = short_name.split(' @ ')
                home_logo = team_logos.get(home_team, 'N/A')
                away_logo = team_logos.get(away_team, 'N/A')
                
                competitions = game_data.get('competitions', [])
                if competitions:
                    competition = competitions[0]
                    odds_ref = competition.get('odds', {}).get('$ref', '')
                    
                    if odds_ref:
                        odds_data = fetch_game_odds(odds_ref)
                        if odds_data and 'items' in odds_data and odds_data['items']:
                            odds_item = odds_data['items'][0]

                            spread = odds_item.get('spread', 'N/A')
                            over_under = odds_item.get('overUnder', 'N/A')
                            away_team_spread_odds = odds_item.get('awayTeamOdds', {}).get('current', {}).get('spread', {}).get('alternateDisplayValue', 'N/A')
                            home_team_spread_odds = odds_item.get('homeTeamOdds', {}).get('current', {}).get('spread', {}).get('alternateDisplayValue', 'N/A')
                            away_team_Pspread_odds = odds_item.get('awayTeamOdds', {}).get('current', {}).get('pointSpread', {}).get('alternateDisplayValue', 'N/A')
                            home_team_Pspread_odds = odds_item.get('homeTeamOdds', {}).get('current', {}).get('pointSpread', {}).get('alternateDisplayValue', 'N/A')
                            away_team_moneyline_odds = odds_item.get('awayTeamOdds', {}).get('current', {}).get('moneyLine', {}).get('alternateDisplayValue', 'N/A')
                            home_team_moneyline_odds = odds_item.get('homeTeamOdds', {}).get('current', {}).get('moneyLine', {}).get('alternateDisplayValue', 'N/A')
                            
                            game_details = {
                                'short_name': short_name,
                                'away_team': away_team,
                                'home_team': home_team,
                                'game_date': game_date,
                                'spread': spread,
                                'over_under': over_under,
                                'away_team_spread_odds': away_team_spread_odds,
                                'home_team_spread_odds': home_team_spread_odds,
                                'away_team_Pspread_odds': away_team_Pspread_odds,
                                'home_team_Pspread_odds': home_team_Pspread_odds,
                                'away_team_moneyline_odds': away_team_moneyline_odds,
                                'home_team_moneyline_odds': home_team_moneyline_odds,
                                'home_logo': home_logo,
                                'away_logo': away_logo,
                                'week': weekNum,
                                'season': seasonTypeName
                            }
                            all_games.append(game_details)
    return all_games


def final_NFL_json():
    seasonYear = 2024
    seasonType = 2
    weekNum = 1
    all_games = format_NFL_json(seasonYear, seasonType, weekNum)
    desired_games_count = 32  # Adjust this number as needed

    while len(all_games) < desired_games_count:
        weekNum += 1
        # if weekNum > 4 and seasonType == 1:
        #     seasonType += 1
        #     weekNum = 1
        if weekNum > 18 and seasonType == 2:  # Move from Regular Season to Postseason
            seasonType = 3
            weekNum = 1
        additional_games = format_NFL_json(seasonYear, seasonType, weekNum)
        all_games.extend(additional_games)
        
        # Break if no additional games are found to avoid infinite loop
        if not additional_games:
            break

    return all_games
