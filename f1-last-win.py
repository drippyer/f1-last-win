import requests
from datetime import datetime

base_url = 'http://ergast.com/api/f1'
today = datetime.today()

drivers_url = f"{base_url}/current/drivers.json"
resp = requests.get(drivers_url).json()
drivers = resp['MRData']['DriverTable']['Drivers']

for idx, driver in enumerate(drivers):
    url = f"{base_url}/drivers/{driver['driverId']}/results/1.json?limit=130"
    resp = requests.get(url).json()
    wins = resp['MRData']['RaceTable']['Races']

    if wins:
        last_win = wins[-1]
        win_date = datetime.strptime(last_win['date'], '%Y-%m-%d')
        win_delta = today - win_date

        print(f"{driver['familyName']}: {win_delta.days} days")