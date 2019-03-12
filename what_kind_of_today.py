import sys
import requests
from datetime import date
from datetime import datetime

today = datetime.now()

response = requests.get("http://api.github.com/users/patternexon/repos")

repos = response.json()

any_update = 0

for repo in repos:
    repo_name = repo['name']
    update_time = datetime.strptime(repo['updated_at'],"%Y-%m-%dT%H:%M:%SZ")
    if(abs(today - update_time).days < 1):
        any_update = 1
if (any_update):
    print("You are ok - today was a push day")
else:
    print("Well son, you are loosing the battle")