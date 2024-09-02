import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime, timedelta


def scrapeOddsData():
    url = 'https://www.sportsbettingdime.com/mlb/public-betting-trends/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    web_page = response.content

    soup = BeautifulSoup(web_page, 'html.parser')

    tables = soup.find_all('table', class_='jss25 odds-table')
    all_teams_data = []

    for table in tables:
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if cells:
                team_name = cells[0].find(class_='jss71').text.strip()  # Assuming this finds the abbreviation directly
                if team_name == "WAS":
                    team_name = "WSH"
                spread = cells[1].find('span').text.strip() if cells[1].find('span') else None
                spread_money_pct = cells[2].text.strip() if cells[2] else None
                spread_bet_pct = cells[3].text.strip() if cells[3] else None
                
                money_line = cells[7].find('span').text.strip() if cells[7].find('span') else None
                money_line_money_pct = cells[8].text.strip() if cells[8] else None
                money_line_bet_pct = cells[9].text.strip() if cells[9] else None
                
                total = cells[10].find('span').text.strip() if cells[10].find('span') else None
                total_money_pct = cells[11].text.strip() if cells[11] else None
                total_bet_pct = cells[12].text.strip() if cells[12] else None

                team_data = {
                    'Team': team_name,
                    'Spread': spread,
                    'Spread Money %': spread_money_pct,
                    'Spread Bet %': spread_bet_pct,
                    'Money Line': money_line,
                    'Money Line Money %': money_line_money_pct,
                    'Money Line Bet %': money_line_bet_pct,
                    'Total': total,
                    'Total Money %': total_money_pct,
                    'Total Bet %': total_bet_pct,
                }
                all_teams_data.append(team_data)

    df_dime = pd.DataFrame(all_teams_data)
    return df_dime

def formatData(df_dime):
    # DataFrame groups every two rows together for matchups
    matchups = pd.DataFrame()
    for i in range(0, len(df_dime), 2):
        matchup = df_dime.iloc[i:i+2].reset_index(drop=True)
        matchups = pd.concat([matchups, matchup.T], axis=1)

    matchups.columns = range(matchups.shape[1])


    formatted_data = matchups.to_dict(orient='records')
    json_data = json.dumps(formatted_data)


    data = json.loads(json_data)

    matchups = []

    for i in range(0, len(data[0]), 2):
        matchup = {
            "Visitor": data[0][str(i)],
            "Home": data[0][str(i+1)],
            "VisitorSpread": data[1][str(i)],
            "HomeSpread": data[1][str(i+1)],
            "VisitorSpreadPercent": data[2][str(i)], # Money %
            "HomeSpreadPercent": data[2][str(i+1)], # Money %
            "VisitorSpreadBetPercent": data[3][str(i)],
            "HomeSpreadBetPercent": data[3][str(i+1)],
            "VisitorMoneyLine": data[4][str(i)],
            "HomeMoneyLine": data[4][str(i+1)],
            "VisitorMoneyLinePercent": data[5][str(i)], # Money %
            "HomeMoneyLinePercent": data[5][str(i+1)], # Money %
            "VisitorMoneyLineBetPercent": data[6][str(i)], # Bet %
            "HomeMoneyLineBetPercent": data[6][str(i+1)], # Bet %
            "TotalRuns": data[7][str(i)],
            "TotalMoneyPercentVisitor": data[8][str(i)], # Money % on total runs o/u
            "TotalMoneyPercentHome": data[8][str(i+1)], # Money % on total runs o/u
            "slug": f'{data[0][str(i)]}-{data[0][str(i+1)]}'
        }
        matchups.append(matchup)
        matchups_json = json.dumps(matchups)
        
    return matchups_json

def get_game_times(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        game_times = {}
        # Loop through the dates, looking for today's date
        for date_info in data['dates']:

            if date_info['date'] == datetime.now().strftime("%Y-%m-%d"):

                for game in date_info['games']:

                    game_date = datetime.fromisoformat(game['gameDate'].replace("Z", "+00:00")) - timedelta(hours=7)

                    game_time = game_date.strftime("%I:%M %p")

                    teams_key = f"{game['teams']['away']['team']['name']} @ {game['teams']['home']['team']['name']}"

                    game_times[teams_key] = game_time
        return game_times
    else:
        return f"Failed to fetch data: Status code {response.status_code}"


def includeGameTimes(game_times, matchups_json):
    # there is a small chance that teams that haven't played yet (in the past couple days) have the wrong abbreviation
    team_mapping = {
        "ARI": "Arizona Diamondbacks",
        "ATL": "Atlanta Braves",
        "BAL": "Baltimore Orioles",
        "BOS": "Boston Red Sox",
        "CHC": "Chicago Cubs",
        "CHW": "Chicago White Sox",
        "CIN": "Cincinnati Reds",
        "CLE": "Cleveland Guardians",
        "COL": "Colorado Rockies",
        "DET": "Detroit Tigers",
        "HOU": "Houston Astros",
        "KC": "Kansas City Royals",
        "LAA": "Los Angeles Angels",
        "LAD": "Los Angeles Dodgers",
        "MIA": "Miami Marlins",
        "MIL": "Milwaukee Brewers",
        "MIN": "Minnesota Twins",
        "NYM": "New York Mets",
        "NYY": "New York Yankees",
        "OAK": "Oakland Athletics",
        "PHI": "Philadelphia Phillies",
        "PIT": "Pittsburgh Pirates",
        "SD": "San Diego Padres",
        "SF": "San Francisco Giants",
        "SEA": "Seattle Mariners",
        "STL": "St. Louis Cardinals",
        "TB": "Tampa Bay Rays",
        "TEX": "Texas Rangers",
        "TOR": "Toronto Blue Jays",
        "WSH": "Washington Nationals"
    }

    data = json.loads(matchups_json)
    for item in data:
        # contruct the full name key from the abbreviations using the mapping
        visitor_full = team_mapping[item['Visitor']]
        home_full = team_mapping[item['Home']]
        full_name_key = f"{visitor_full} @ {home_full}"
        
        # find the corresponding game time and add it to the dictionary
        if full_name_key in game_times:
            item['GameTime'] = game_times[full_name_key]
        else:
            item['GameTime'] = "Today"

    # updated data back to JSON
    updated_json_data = json.dumps(data)
    # print(updated_json_data)
    # j_string = "'" + updated_json_data + "'"
    # print(j_string)
    return updated_json_data


def get_final_json():
    url = "https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1"
    final_string = includeGameTimes(get_game_times(url), formatData(scrapeOddsData()))
    return final_string
# if __name__ == '__main__':
    # url = "https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1"
    # final_string = includeGameTimes(get_game_times(url), formatData(scrapeOddsData()))
    # print(final_string)
    


def format_future_games(json_data):
    data = json.loads(json_data)
    team_mapping = {
        "Arizona Diamondbacks": "ARI",
        "Atlanta Braves": "ATL",
        "Baltimore Orioles": "BAL",
        "Boston Red Sox": "BOS",
        "Chicago Cubs": "CHC",
        "Chicago White Sox": "CHW",
        "Cincinnati Reds": "CIN",
        "Cleveland Guardians": "CLE",
        "Colorado Rockies": "COL",
        "Detroit Tigers": "DET",
        "Houston Astros": "HOU",
        "Kansas City Royals": "KC",
        "Los Angeles Angels": "LAA",
        "Los Angeles Dodgers": "LAD",
        "Miami Marlins": "MIA",
        "Milwaukee Brewers": "MIL",
        "Minnesota Twins": "MIN",
        "New York Mets": "NYM",
        "New York Yankees": "NYY",
        "Oakland Athletics": "OAK",
        "Philadelphia Phillies": "PHI",
        "Pittsburgh Pirates": "PIT",
        "San Diego Padres": "SD",
        "San Francisco Giants": "SF",
        "Seattle Mariners": "SEA",
        "St. Louis Cardinals": "STL",
        "Tampa Bay Rays": "TB",
        "Texas Rangers": "TEX",
        "Toronto Blue Jays": "TOR",
        "Washington Nationals": "WSH"
    }
    for game in data:
        game['away_team'] = team_mapping[game['away_team']]
        game['home_team'] = team_mapping[game['home_team']]
        datetime_object = datetime.strptime(game['game_time'], "%Y-%m-%dT%H:%M:%SZ")
        game['date'] = datetime_object.strftime("%Y-%m-%d")
#         game['time'] = datetime_object.strftime("%I:%M: %p") - timedelta(hours=7)
        new_date_obj = datetime_object - timedelta(hours=7)
        game['time'] = new_date_obj.strftime("%I:%M: %p")
        del game['game_time']

    return json.dumps(data, indent=4)


def fetch_future_games(start_date, end_date):
    url = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate={start_date}&endDate={end_date}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        all_games = []
        # Iterate through each day and collect games
        for date in data.get('dates', []):
            if len(all_games) < 12:
                remaining_slots = 12 - len(all_games)
                all_games.extend(date['games'][:remaining_slots])
        return all_games
    else:
        return None

def organize_into_json(games):
    organized_data = []
    for game in games:
        game_info = {
            'date': game['officialDate'],
            'away_team': game['teams']['away']['team']['name'],
            'home_team': game['teams']['home']['team']['name'],
            'venue': game['venue']['name'],
            'game_time': game['gameDate']
        }
        organized_data.append(game_info)
    return json.dumps(organized_data, indent=4)

def map_teams_to_abbr(json_data):
    data = json.loads(json_data)
    team_mapping = {
        "Arizona Diamondbacks": "ARI",
        "Atlanta Braves": "ATL",
        "Baltimore Orioles": "BAL",
        "Boston Red Sox": "BOS",
        "Chicago Cubs": "CHC",
        "Chicago White Sox": "CHW",
        "Cincinnati Reds": "CIN",
        "Cleveland Guardians": "CLE",
        "Colorado Rockies": "COL",
        "Detroit Tigers": "DET",
        "Houston Astros": "HOU",
        "Kansas City Royals": "KC",
        "Los Angeles Angels": "LAA",
        "Los Angeles Dodgers": "LAD",
        "Miami Marlins": "MIA",
        "Milwaukee Brewers": "MIL",
        "Minnesota Twins": "MIN",
        "New York Mets": "NYM",
        "New York Yankees": "NYY",
        "Oakland Athletics": "OAK",
        "Philadelphia Phillies": "PHI",
        "Pittsburgh Pirates": "PIT",
        "San Diego Padres": "SD",
        "San Francisco Giants": "SF",
        "Seattle Mariners": "SEA",
        "St. Louis Cardinals": "STL",
        "Tampa Bay Rays": "TB",
        "Texas Rangers": "TEX",
        "Toronto Blue Jays": "TOR",
        "Washington Nationals": "WSH"
    }
    for game in data:
        game['away_team'] = team_mapping[game['away_team']]
        game['home_team'] = team_mapping[game['home_team']]
        datetime_object = datetime.strptime(game['game_time'], "%Y-%m-%dT%H:%M:%SZ")
        game['date'] = datetime_object.strftime("%m/%d")
        new_date_obj = datetime_object - timedelta(hours=7)
        game['time'] = new_date_obj.strftime("%I:%M %p")
        del game['game_time']

    return json.dumps(data, indent=4)

def get_future_games_formatted():
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    week_later = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    games_data1 = fetch_future_games(tomorrow, week_later)
    if games_data1:
        games = organize_into_json(games_data1)
        return map_teams_to_abbr(games)
    else:
        return None
