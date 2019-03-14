from pathlib import Path 
import requests
from datetime import date
from datetime import datetime, timedelta
from pprint import pprint, pformat
import logging


logPath="."
fileName=Path(__file__).stem

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}.log".format(logPath, fileName)),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

today = datetime.now()
logger.debug("The time is %s", today)
yesterday = today - timedelta(days=1)
logger.debug("And thus yesterday was %s", yesterday)

response = requests.get("http://api.github.com/users/patternexon/repos")

repos = response.json()

any_update = None

for repo in repos:
    repo_name = repo['name']
    update_time = datetime.strptime(repo['updated_at'],"%Y-%m-%dT%H:%M:%SZ")
    logger.info("For repo %s the last update time was %s",repo_name, update_time)
    if(abs(today - update_time).days < 1):
        any_update = 1
        url_commits_since_yesterday = repo['url']+'/commits?since='+ datetime.strftime(yesterday,"%Y-%m-%dT%H:%M:%SZ")
        logger.debug("Url for commits since yesterday %s", url_commits_since_yesterday)
        commits_since_yesterday = requests.get(url_commits_since_yesterday).json()
        commit_count = len(commits_since_yesterday) 
        logger.debug("Number of commits since yesterday: %s", commit_count)
        if commit_count > 5:
            print("Now you are COMMITTED")
if any_update:
    print("You are ok - today was a push day")
else:
    print("Well son, you are loosing the battle")