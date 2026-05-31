#!/usr/bin/env python3

import json
import os
import subprocess
import requests
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
BACKUP_ROOT = Path("github_backup")

if not GITHUB_TOKEN:
    raise RuntimeError(
        "Set GITHUB_TOKEN environment variable first."
    )

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

BACKUP_ROOT.mkdir(exist_ok=True)

# ============================================================
# HELPERS
# ============================================================

def github_get(url):
    results = []

    while url:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()

        data = r.json()

        if isinstance(data, list):
            results.extend(data)
        else:
            return data

        url = None

        if "next" in r.links:
            url = r.links["next"]["url"]

    return results


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ============================================================
# USER INFO
# ============================================================

user = github_get("https://api.github.com/user")
username = user["login"]

print(f"Backing up account: {username}")

save_json(
    BACKUP_ROOT / "account.json",
    user
)

# ============================================================
# REPOSITORIES
# ============================================================

repos = github_get(
    "https://api.github.com/user/repos?per_page=100"
)

repos_dir = BACKUP_ROOT / "repos"
repos_dir.mkdir(exist_ok=True)

for repo in repos:
    name = repo["name"]
    full_name = repo["full_name"]

    print(f"[REPO] {full_name}")

    repo_dir = repos_dir / f"{name}.git"

    clone_url = repo["clone_url"]

    if not repo_dir.exists():
        subprocess.run(
            [
                "git",
                "clone",
                "--mirror",
                clone_url,
                str(repo_dir)
            ],
            check=True
        )
    else:
        subprocess.run(
            [
                "git",
                "--git-dir",
                str(repo_dir),
                "remote",
                "update"
            ],
            check=True
        )

    metadata_dir = BACKUP_ROOT / "metadata" / name
    metadata_dir.mkdir(parents=True, exist_ok=True)

    save_json(metadata_dir / "repo.json", repo)

    try:
        issues = github_get(
            f"https://api.github.com/repos/{full_name}/issues?state=all&per_page=100"
        )
        save_json(metadata_dir / "issues.json", issues)
    except Exception as e:
        print("issues:", e)

    try:
        pulls = github_get(
            f"https://api.github.com/repos/{full_name}/pulls?state=all&per_page=100"
        )
        save_json(metadata_dir / "pulls.json", pulls)
    except Exception as e:
        print("pulls:", e)

    try:
        releases = github_get(
            f"https://api.github.com/repos/{full_name}/releases?per_page=100"
        )
        save_json(metadata_dir / "releases.json", releases)
    except Exception as e:
        print("releases:", e)

# ============================================================
# GISTS
# ============================================================

gists_dir = BACKUP_ROOT / "gists"
gists_dir.mkdir(exist_ok=True)

gists = github_get(
    "https://api.github.com/gists?per_page=100"
)

save_json(
    gists_dir / "gists.json",
    gists
)

for gist in gists:
    gid = gist["id"]
    gist_clone_url = gist["git_pull_url"]

    target = gists_dir / f"{gid}.git"

    print(f"[GIST] {gid}")

    if not target.exists():
        subprocess.run(
            [
                "git",
                "clone",
                "--mirror",
                gist_clone_url,
                str(target)
            ],
            check=True
        )
    else:
        subprocess.run(
            [
                "git",
                "--git-dir",
                str(target),
                "remote",
                "update"
            ],
            check=True
        )

print("\nBackup complete.")
