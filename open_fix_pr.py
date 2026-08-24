"""
OmniSight - Week 3: GitHub PR Automation
--------------------------------------------
Takes a verified CSS fix (from the self-healing loop) and turns it into
a real GitHub Pull Request:
  1. Creates a new branch off your working branch (e.g. "Dibya")
  2. Commits the CSS fix as an actual file in that branch
  3. Opens a Pull Request with the AI's diagnosis in the description

Requirements:
    pip install PyGithub python-dotenv

Environment variables required (in .env):
    GITHUB_TOKEN
    GITHUB_REPO           e.g. "Dibyadhir/omnisight-self-healing-ui"
    GITHUB_BASE_BRANCH    e.g. "Dibya"

Run with:
    python open_fix_pr.py
"""

import os
import time
from dotenv import load_dotenv
from github import Github, GithubException

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


VERIFIED_CSS_FIX = """/* Auto-generated fix by OmniSight */

/* Reveal the hidden Finish button with contrasting background and text colors */
#finish {
  background-color: #e2231a !important;
  color: #ffffff !important;
}

/* Reset horizontal margin to bring the Total label back into view */
.summary_total_label {
  margin-left: 0 !important;
}
"""

AI_DIAGNOSIS_SUMMARY = """OmniSight detected two visual bugs on the checkout overview page:

1. **Invisible "Finish" Button** - The `#finish` button had matching white
   text and white background, making the primary call-to-action invisible.
2. **Hidden Total Price** - The `.summary_total_label` element had a
   `-600px` left margin, pushing the order total off-screen.

Both issues were verified as fixed after applying the attached CSS - the
Finish button and order total are now visible and usable.

This PR was opened automatically by the OmniSight self-healing pipeline.
Please review before merging."""

FIX_FILE_PATH = "fixes/checkout-overview-fix.css"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    token = os.environ.get("GITHUB_TOKEN")
    repo_name = os.environ.get("GITHUB_REPO")
    base_branch = os.environ.get("GITHUB_BASE_BRANCH", "main")

    if not token or not repo_name:
        raise RuntimeError(
            "GITHUB_TOKEN and/or GITHUB_REPO not set. Check your .env file."
        )

    print(f"Connecting to GitHub repo: {repo_name}")
    gh = Github(token)
    repo = gh.get_repo(repo_name)

    # Create a unique branch name so repeated runs don't collide
    timestamp = int(time.time())
    new_branch_name = f"fix/checkout-visibility-{timestamp}"

    print(f"Creating branch '{new_branch_name}' off '{base_branch}'...")
    base_ref = repo.get_branch(base_branch)
    repo.create_git_ref(ref=f"refs/heads/{new_branch_name}", sha=base_ref.commit.sha)

    print(f"Committing fix to '{FIX_FILE_PATH}'...")
    try:
        repo.create_file(
            path=FIX_FILE_PATH,
            message="OmniSight: auto-fix checkout button visibility + total alignment",
            content=VERIFIED_CSS_FIX,
            branch=new_branch_name,
        )
    except GithubException as e:
        print(f"Failed to commit file: {e}")
        return

    print("Opening Pull Request...")
    pr = repo.create_pull(
        title="[OmniSight] Auto-fix: checkout button visibility + total alignment",
        body=AI_DIAGNOSIS_SUMMARY,
        head=new_branch_name,
        base=base_branch,
    )

    print(f"\nSUCCESS - Pull Request opened:")
    print(pr.html_url)


if __name__ == "__main__":
    main()