from pathlib import Path 
import requests
from datetime import date
from datetime import datetime, timedelta
from pprint import pprint, pformat
import logging
import matplotlib.pyplot as plt
import pandas as pd

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
def render_data_frame(commits_per_date):
    #pd.DataFrame(commits_per_date, index=['commits']).plot(kind='bar')
    df = pd.DataFrame(commits_per_date)
    logger.debug(df) 
    #df.groupby([commits_per_date.keys])
    #plt.show()

def draw_bar_graph(commits_per_date):
    plt.bar(range(len(commits_per_date)),list(commits_per_date.values()),
    align='center',tick_label=list(commits_per_date.keys()))
    plt.show()

def get_branches(repo_name, duration):
    r = requests.get("https://api.github.com:443/repos/patternexon/sapola/branches")
    branches = r.json()
    count = 0
    commits_per_branch = {}
    for branch in branches:
        logger.debug("Now running for %s", branch['name'])
        commits_per_branch[branch['name']] = get_all_commits_in_a_branch_since(repo_name, duration, branch['name'])
        #count =+ get_commits_since(repo_name, duration,branch['name'])
    logger.debug(commits_per_branch)
    render_data_frame(commits_per_branch)
    return count

def get_all_commits_in_a_branch_since(repo_name, duration, branch="master"):
    since = today - timedelta(days=duration)
    url_all_commits ="https://api.github.com:443/repos/patternexon/"+repo_name+'/commits?sha='+branch
    logger.debug("Getting %s", url_all_commits)
    all_commits = requests.get(url_all_commits).json()
    commits_per_date = {}
    for commit in all_commits:
        commit_datetime = datetime.strptime(commit['commit']['author']['date'],"%Y-%m-%dT%H:%M:%SZ")
        if commit_datetime > since:
            logger.debug("The date is %s", commit_datetime)
            commit_date = commit_datetime.strftime("%Y-%m-%d")
            if commit_date in commits_per_date:
                commits_per_date[commit_date] += 1
            else:
                commits_per_date[commit_date] = 1
    logger.debug(commits_per_date)
    return commits_per_date


def get_commits_since(repo_name, duration, branch="master"):
    since = today - timedelta(days=duration)
    url_commits_since = repo['url']+'/commits?since='+ datetime.strftime(since,"%Y-%m-%dT%H:%M:%SZ")
    logger.debug("Url for commits since %s %s", duration, url_commits_since)
    commits_since = requests.get(url_commits_since).json()
    logger.debug("Commits retrieved: %s", len(commits_since))
    commits_per_date = {}
    for commit_detail in commits_since:
        logger.info(commit_detail['commit']['committer']['date'])
        commit_date = datetime.strptime(commit_detail['commit']['committer']['date'],"%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
        if commit_date in commits_per_date:
            commits_per_date[commit_date] += 1
        else:
            commits_per_date[commit_date] = 1
    commit_count = len(commits_since) 
    logger.debug("Number of commits since %s day(s): %s", duration, commit_count)
    draw_bar_graph(commits_per_date)
    render_data_frame(commits_per_date)
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
        commit_count = get_branches(repo_name, 1)
        #commit_count = get_commits_since(repo_name,1)
        any_update = 1
        if commit_count > 5:
            print("Now you are COMMITTED")
if any_update:
    print("You are ok - today was a push day")
else:
    print("Well son, you are loosing the battle")   