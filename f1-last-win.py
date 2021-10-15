import requests
from datetime import datetime
from shutil import copyfile

base_url = 'http://ergast.com/api/f1'
today = datetime.today()

drivers_url = f"{base_url}/current/drivers.json"
resp = requests.get(drivers_url).json()
drivers = resp['MRData']['DriverTable']['Drivers']

last_wins = {}
for idx, driver in enumerate(drivers):
    url = f"{base_url}/drivers/{driver['driverId']}/results/1.json?limit=130"
    resp = requests.get(url).json()
    wins = resp['MRData']['RaceTable']['Races']

    if wins:
        last_win = wins[-1]
        win_date = datetime.strptime(last_win['date'], '%Y-%m-%d')
        win_delta = today - win_date
        last_wins[driver['driverId']] = {'name': f"{driver['givenName']} {driver['familyName']}", 'days':win_delta.days}
        
sorted_wins = {k: v for k, v in sorted(last_wins.items(), key=lambda item: item[1]['days'])}

lines = [f"| ![{val['name']}](./driver_photos/{dId}.jpg) | {val['name']} | {val['days']} |\n" for dId, val in sorted_wins.items()]

copyfile('template.md', 'current.md')

with open('current.md', 'a') as file:
    for line in lines:
        file.write(line)