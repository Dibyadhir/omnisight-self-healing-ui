import os

from github import Github
from dotenv import load_dotenv


load_dotenv()


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")


def get_github_repo():
    """
    Connect to the configured GitHub repository.
    """

    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN is not configured")

    if not GITHUB_REPO:
        raise ValueError("GITHUB_REPO is not configured")

    github = Github(GITHUB_TOKEN)

    return github.get_repo(GITHUB_REPO)