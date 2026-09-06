import os
from dotenv import load_dotenv
from github import Github

load_dotenv()


def get_github_connection():
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise ValueError("GITHUB_TOKEN is not set")

    github = Github(token)

    return github


def get_github_user():
    github = get_github_connection()
    user = github.get_user()

    return {
        "username": user.login,
        "name": user.name,
    }


def get_repository_details():
    github = get_github_connection()

    repo = github.get_repo("Dibyadhir/omnisight-self-healing-ui")

    return {
        "name": repo.name,
        "full_name": repo.full_name,
        "description": repo.description,
        "default_branch": repo.default_branch,
    }


def get_branches():
    github = get_github_connection()

    repo = github.get_repo("Dibyadhir/omnisight-self-healing-ui")

    branches = repo.get_branches()

    return [branch.name for branch in branches]


def get_repository_files():
    github = get_github_connection()

    repo = github.get_repo("Dibyadhir/omnisight-self-healing-ui")

    contents = repo.get_contents("")

    return [item.path for item in contents]


def get_file_content(file_path):
    github = get_github_connection()

    repo = github.get_repo("Dibyadhir/omnisight-self-healing-ui")

    file = repo.get_contents(file_path)

    return file.decoded_content.decode("utf-8")


def test_github_access():
    github = get_github_connection()

    repo = github.get_repo("Dibyadhir/omnisight-self-healing-ui")

    return {
        "repository": repo.full_name,
        "branches": [branch.name for branch in repo.get_branches()],
        "root_files": [item.path for item in repo.get_contents("")],
    }


def create_branch(branch_name):
    github = get_github_connection()

    repo = github.get_repo("Dibyadhir/omnisight-self-healing-ui")

    source_branch = repo.default_branch
    source = repo.get_branch(source_branch)

    repo.create_git_ref(
        ref=f"refs/heads/{branch_name}",
        sha=source.commit.sha
    )

    return branch_name


def get_file_sha(file_path, branch_name="module4-khushboo"):
    github = get_github_connection()

    repo = github.get_repo("Dibyadhir/omnisight-self-healing-ui")

    file = repo.get_contents(file_path, ref=branch_name)

    return file.sha


def update_file(
    file_path,
    new_content,
    commit_message,
    branch_name="module4-khushboo"
):
    github = get_github_connection()

    repo = github.get_repo("Dibyadhir/omnisight-self-healing-ui")

    file = repo.get_contents(file_path, ref=branch_name)

    result = repo.update_file(
        path=file_path,
        message=commit_message,
        content=new_content,
        sha=file.sha,
        branch=branch_name
    )

    return {
        "path": file_path,
        "commit_sha": result["commit"].sha,
        "branch": branch_name
    }


