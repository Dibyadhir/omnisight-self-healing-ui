from backend.services.github_service import get_github_repo


def main():
    repo = get_github_repo()

    print("GitHub connection successful")
    print("Repository:", repo.full_name)
    print("Default branch:", repo.default_branch)

    print("\nBranches:")
    for branch in repo.get_branches():
        print("-", branch.name)

    # -----------------------------------------
    # Step 1: Create a test branch
    # -----------------------------------------
    branch_name = "omnisight-test-fix"

    source_branch = repo.get_branch(repo.default_branch)

    try:
        repo.create_git_ref(
            ref=f"refs/heads/{branch_name}",
            sha=source_branch.commit.sha
        )
        print(f"\nNew branch created: {branch_name}")

    except Exception as e:
        if "Reference already exists" in str(e):
            print(f"\nBranch already exists: {branch_name}")
        else:
            raise

    # -----------------------------------------
    # Step 2: Update README.md
    # -----------------------------------------
    file_path = "README.md"
    commit_message = "Test automated GitHub fix commit"

    file = repo.get_contents(
        file_path,
        ref=branch_name
    )

    new_content = (
        file.decoded_content.decode("utf-8")
        + "\n\n<!-- OmniSight automated fix test -->\n"
    )

    repo.update_file(
        path=file_path,
        message=commit_message,
        content=new_content,
        sha=file.sha,
        branch=branch_name
    )

    print(f"\nFile updated: {file_path}")
    print(f"Commit created: {commit_message}")

    # -----------------------------------------
    # Step 3: Create Pull Request
    # -----------------------------------------
    existing_pr = None

    for pr in repo.get_pulls(
        state="open",
        head=f"{repo.owner.login}:{branch_name}",
        base=repo.default_branch
    ):
        existing_pr = pr
        break

    if existing_pr:
        print("\nPull Request already exists!")
        print("PR Number:", existing_pr.number)
        print("PR URL:", existing_pr.html_url)

    else:
        pr = repo.create_pull(
            title="OmniSight automated fix test",
            body=(
                "This Pull Request was created automatically "
                "by OmniSight using PyGithub."
            ),
            head=branch_name,
            base=repo.default_branch
        )

        print("\nPull Request created successfully!")
        print("PR Number:", pr.number)
        print("PR URL:", pr.html_url)


if __name__ == "__main__":
    main()