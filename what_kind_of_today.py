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


def get_commits_since(repo_name, duration):
    since = today - timedelta(days=duration)
    url_commits_since = repo['url']+'/commits?since='+ datetime.strftime(since,"%Y-%m-%dT%H:%M:%SZ")
    logger.debug("Url for commits since %s %s", duration, url_commits_since)
    commits_since = requests.get(url_commits_since).json()
    commits_per_date = {}
    for commit_detail in commits_since:
        logger.info(commit_detail['commit']['committer']['date'])
        commit_date = datetime.strptime(commit_detail['commit']['committer']['date'],"%Y-%m-%dT%H:%M:%SZ").date()
        if commit_date in commits_per_date:
            commits_per_date[commit_date] += 1
        else:
            commits_per_date[commit_date] = 1
    for c_date, c_count in commits_per_date.items():
        print(c_date, c_count)
    commit_count = len(commits_since) 
    logger.debug("Number of commits since %s day(s): %s", duration, commit_count)
    return commit_count




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
        commit_count = get_commits_since(repo_name,3)
        any_update = 1
        if commit_count > 5:
            print("Now you are COMMITTED")
if any_update:
    print("You are ok - today was a push day")
else:
    print("Well son, you are loosing the battle")   