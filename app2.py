import json
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Webflow API credentials
WEBFLOW_API_TOKEN = "6e3d49b65c31a1c0b89a743608ad8ad6253120a139bfe7bbb62326106fac43f8"
WEBFLOW_COLLECTION_ID = "66c75f7ffe7a454d852036f5"



def fetch_matchups():
    # Your API endpoint for fetching matchup data
    api_url = "https://todaysport-lerxv37nxa-uc.a.run.app/"
    response = requests.get(api_url)
    if response.status_code == 200:
        matchups_str = response.text
        # print("Raw matchups string:", matchups_str)  # Print the raw string for debugging
        try:
            matchups = json.loads(matchups_str)
            return matchups
            # print("Parsed matchups:", matchups)  # Print the parsed matchups to ensure correctness
        except json.JSONDecodeError as e:
            # print(f"Failed to parse JSON: {e}")
            return []
        
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

# matchups = [{"Visitor": "CLE", "Home": "NYY", "VisitorSpread": "+1.5", "HomeSpread": "-1.5", "VisitorSpreadPercent": "14%", "HomeSpreadPercent": "86%", "VisitorSpreadBetPercent": "9%", "HomeSpreadBetPercent": "91%", "VisitorMoneyLine": "+150", "HomeMoneyLine": "-165", "VisitorMoneyLinePercent": "7%", "HomeMoneyLinePercent": "93%", "VisitorMoneyLineBetPercent": "13%", "HomeMoneyLineBetPercent": "87%", "TotalRuns": "o8", "TotalMoneyPercentVisitor": "94%", "TotalMoneyPercentHome": "6%", "GameTime": "10:05 AM"}, {"Visitor": "COL", "Home": "WSH", "VisitorSpread": "+1.5", "HomeSpread": "+1.5", "VisitorSpreadPercent": "29%", "HomeSpreadPercent": "71%", "VisitorSpreadBetPercent": "28%", "HomeSpreadBetPercent": "72%", "VisitorMoneyLine": "+115", "HomeMoneyLine": "-124", "VisitorMoneyLinePercent": "7%", "HomeMoneyLinePercent": "93%", "VisitorMoneyLineBetPercent": "25%", "HomeMoneyLineBetPercent": "75%", "TotalRuns": "o9", "TotalMoneyPercentVisitor": "80%", "TotalMoneyPercentHome": "20%", "GameTime": "10:05 AM"}, {"Visitor": "MIL", "Home": "STL", "VisitorSpread": "-1.5", "HomeSpread": "+1.5", "VisitorSpreadPercent": "92%", "HomeSpreadPercent": "8%", "VisitorSpreadBetPercent": "85%", "HomeSpreadBetPercent": "15%", "VisitorMoneyLine": "-120", "HomeMoneyLine": "+105", "VisitorMoneyLinePercent": "85%", "HomeMoneyLinePercent": "15%", "VisitorMoneyLineBetPercent": "68%", "HomeMoneyLineBetPercent": "32%", "TotalRuns": "o7.5", "TotalMoneyPercentVisitor": "97%", "TotalMoneyPercentHome": "3%", "GameTime": "11:15 AM"}, {"Visitor": "DET", "Home": "CHC", "VisitorSpread": "+1.5", "HomeSpread": "-1.5", "VisitorSpreadPercent": "45%", "HomeSpreadPercent": "55%", "VisitorSpreadBetPercent": "20%", "HomeSpreadBetPercent": "80%", "VisitorMoneyLine": "+176", "HomeMoneyLine": "-198", "VisitorMoneyLinePercent": "42%", "HomeMoneyLinePercent": "58%", "VisitorMoneyLineBetPercent": "18%", "HomeMoneyLineBetPercent": "82%", "TotalRuns": "o7.5", "TotalMoneyPercentVisitor": "98%", "TotalMoneyPercentHome": "2%", "GameTime": "11:20 AM"}, {"Visitor": "TB", "Home": "OAK", "VisitorSpread": "-1.5", "HomeSpread": "+1.5", "VisitorSpreadPercent": "57%", "HomeSpreadPercent": "43%", "VisitorSpreadBetPercent": "62%", "HomeSpreadBetPercent": "38%", "VisitorMoneyLine": "-118", "HomeMoneyLine": "+105", "VisitorMoneyLinePercent": "65%", "HomeMoneyLinePercent": "35%", "VisitorMoneyLineBetPercent": "68%", "HomeMoneyLineBetPercent": "33%", "TotalRuns": "o7.5", "TotalMoneyPercentVisitor": "90%", "TotalMoneyPercentHome": "11%", "GameTime": "12:37 PM"}, {"Visitor": "CIN", "Home": "PIT", "VisitorSpread": "+1.5", "HomeSpread": "-1.5", "VisitorSpreadPercent": "33%", "HomeSpreadPercent": "67%", "VisitorSpreadBetPercent": "14%", "HomeSpreadBetPercent": "86%", "VisitorMoneyLine": "+130", "HomeMoneyLine": "-140", "VisitorMoneyLinePercent": "25%", "HomeMoneyLinePercent": "75%", "VisitorMoneyLineBetPercent": "26%", "HomeMoneyLineBetPercent": "74%", "TotalRuns": "o7.5", "TotalMoneyPercentVisitor": "96%", "TotalMoneyPercentHome": "4%", "GameTime": "03:40 PM"}, {"Visitor": "LAA", "Home": "TOR", "VisitorSpread": "+1.5", "HomeSpread": "-1.5", "VisitorSpreadPercent": "20%", "HomeSpreadPercent": "80%", "VisitorSpreadBetPercent": "11%", "HomeSpreadBetPercent": "89%", "VisitorMoneyLine": "+143", "HomeMoneyLine": "-158", "VisitorMoneyLinePercent": "29%", "HomeMoneyLinePercent": "71%", "VisitorMoneyLineBetPercent": "16%", "HomeMoneyLineBetPercent": "84%", "TotalRuns": "o8.5", "TotalMoneyPercentVisitor": "7%", "TotalMoneyPercentHome": "93%", "GameTime": "04:07 PM"}, {"Visitor": "HOU", "Home": "BAL", "VisitorSpread": "+1.5", "HomeSpread": "-1.5", "VisitorSpreadPercent": "13%", "HomeSpreadPercent": "87%", "VisitorSpreadBetPercent": "11%", "HomeSpreadBetPercent": "89%", "VisitorMoneyLine": "+136", "HomeMoneyLine": "-155", "VisitorMoneyLinePercent": "17%", "HomeMoneyLinePercent": "83%", "VisitorMoneyLineBetPercent": "19%", "HomeMoneyLineBetPercent": "81%", "TotalRuns": "o8.5", "TotalMoneyPercentVisitor": "22%", "TotalMoneyPercentHome": "78%", "GameTime": "04:08 PM"}, {"Visitor": "PHI", "Home": "ATL", "VisitorSpread": "+1.5", "HomeSpread": "+1.5", "VisitorSpreadPercent": "51%", "HomeSpreadPercent": "49%", "VisitorSpreadBetPercent": "48%", "HomeSpreadBetPercent": "52%", "VisitorMoneyLine": "-104", "HomeMoneyLine": "-110", "VisitorMoneyLinePercent": "46%", "HomeMoneyLinePercent": "54%", "VisitorMoneyLineBetPercent": "41%", "HomeMoneyLineBetPercent": "59%", "TotalRuns": "o8", "TotalMoneyPercentVisitor": "19%", "TotalMoneyPercentHome": "81%", "GameTime": "04:08 PM"}, {"Visitor": "NYM", "Home": "SD", "VisitorSpread": "+1.5", "HomeSpread": "-1.5", "VisitorSpreadPercent": "44%", "HomeSpreadPercent": "56%", "VisitorSpreadBetPercent": "18%", "HomeSpreadBetPercent": "82%", "VisitorMoneyLine": "+136", "HomeMoneyLine": "-146", "VisitorMoneyLinePercent": "29%", "HomeMoneyLinePercent": "71%", "VisitorMoneyLineBetPercent": "26%", "HomeMoneyLineBetPercent": "74%", "TotalRuns": "o7.5", "TotalMoneyPercentVisitor": "95%", "TotalMoneyPercentHome": "5%", "GameTime": "06:40 PM"}]

# def update_webflow_cms(matchups):
#     endpoint = f"https://api.webflow.com/v2/collections/{WEBFLOW_COLLECTION_ID}/items"
#     headers = {
#         "Authorization": f"Bearer {WEBFLOW_API_TOKEN}",
#         "Content-Type": "application/json",
#         "accept-version": "1.0.0"
#     }

#     for matchup in matchups:
#         # print("Processing matchup:", matchup)  # Debugging print to check each matchup's type and content
#         print("Type of matchup:", type(matchup))  # Print the type of matchup to ensure it's a dictionary
        
#         # Ensure matchup is a dictionary before accessing its keys
#         if isinstance(matchup, dict):
#             slug = matchup['Visitor'].lower()+'-'+matchup['Home'].lower()
#             print(slug)
#             data = {
#                 "fields": {
#                     # "name": f'{matchup["Visitor"]} vs {matchup["Home"]}',
#                     # "visitor-home": slug,
#                     # "slug": slug,
#                     # "visitor-team": matchup["Visitor"],
#                     # "home-team": matchup["Home"]
#                     # "game-date": matchup["GameTime"]  # You might want to format the date properly
#                     # "visitor-logo": {"url": "path_to_visitor_logo"},  # Replace with actual URL
#                     # "home-logo": {"url": "path_to_home_logo"},  # Replace with actual URL
#                     # "visitor-spread": matchup["VisitorSpread"],
#                     # "home-spread": matchup["HomeSpread"],
#                     # "visitor-moneyline": matchup["VisitorMoneyLine"],
#                     # "home-moneyline": matchup["HomeMoneyLine"],
#                     # Add odds and other relevant data fields here
#                 }
#             }
#             response = requests.post(endpoint, headers=headers, json=data)
#             print(response.text)
#             if response.status_code == 200:
#                 print(f"Successfully updated item: {slug}")
#             else:
#                 print(f"Failed to update item: {response.text}")
#         else:
#             print(f"Unexpected data type: {type(matchup)} - {matchup}")

# @app.route('/update-webflow', methods=['GET'])
# def update_webflow():
#     # matchups = fetch_matchups()
#     update_webflow_cms(matchups)
#     return jsonify({"status": "success", "message": "Webflow CMS updated with latest matchups"}), 200

# url = f"https://api.webflow.com/v2/collections/{WEBFLOW_COLLECTION_ID}/items"

# headers = {
#     "Authorization": f"Bearer {WEBFLOW_API_TOKEN}",
#     "Content-Type": "application/json",
#     "accept-version": "1.0.0"
# }

# # Example data for one matchup
# data = {
#     "fieldData": {
#         "name": "CLE vs NYY",
#         "slug": "cle-nyy",
#         "visitor-team": "CLE",
#         "home-team": "NYY",
        
#         # Add other fields here
#     },
#     "isArchived": False,
#     "isDraft": False
# }

# response = requests.post(url, headers=headers, json=data)
# print(response.text)

# if response.status_code == 202:
#     print("Item created successfully.")
# else:
#     print(f"Failed to create item: {response.text}")
    
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True, port=8080)


def update_webflow_cms(matchups):
    endpoint = f"https://api.webflow.com/v2/collections/{WEBFLOW_COLLECTION_ID}/items"
    headers = {
        "Authorization": f"Bearer {WEBFLOW_API_TOKEN}",
        "Content-Type": "application/json",
        "accept-version": "1.0.0"
    }
    
    for matchup in matchups:
        if isinstance(matchup, dict):
            slug = matchup['Visitor'].lower() + '-' + matchup['Home'].lower()
            print(f"Processing matchup: {slug}")
            
            data = {
                "fieldData": {
                    "name": f'{matchup["Visitor"]} vs {matchup["Home"]}',
                    "slug": slug,
                    "visitor-team": matchup["Visitor"],
                    "home-team": matchup["Home"],
                    "visitor-spread": matchup["VisitorSpread"],
                    "home-spread": matchup["HomeSpread"],
                    "visitor-moneyline": matchup["VisitorMoneyLine"],
                    "home-moneyline": matchup["HomeMoneyLine"],
                    "game-time": matchup["GameTime"]
                },
                "isArchived": False,
                "isDraft": False
            }
            response = requests.post(endpoint, headers=headers, json=data)
            if response.status_code == 202:
                print(f"Successfully updated item: {slug}")
            else:
                print(f"Failed to update item: {response.text}")

                
@app.route('/update-webflow', methods=['GET'])
def update_webflow():
    matchups = fetch_matchups()
    if matchups:
        update_webflow_cms(matchups)
        return jsonify({"status": "success", "message": "Webflow CMS updated with latest matchups"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to fetch matchups data"}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
