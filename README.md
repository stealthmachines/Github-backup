<img width="1905" height="566" alt="image" src="https://github.com/user-attachments/assets/1c8f51ca-dfdf-4dc9-8032-d72677a7e2ef" />
<img width="869" height="766" alt="image" src="https://github.com/user-attachments/assets/4f0f8c56-cdcb-47aa-9d3d-764b715b4381" />

1) Generate a Github Token for API over at https://github.com/settings/tokens
2) Place this script (gitbackup.py) in a folder by itself
3) In CMD, type: $env:GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxx" (replace with your API token) and hit ENTER - this places the token "password" as an environmental variable
4) Type 'py gitbackup.py' and hit ENTER

# That's it, you're done.


# Other Environments / Instructions
Linux/macOS

export GITHUB_TOKEN=github_pat_xxxxxxxxxxxxxxxxx
python github_backup.py

Windows PowerShell

$env:GITHUB_TOKEN="github_pat_xxxxxxxxxxxxxxxxx"
python github_backup.py

Windows CMD

set GITHUB_TOKEN=github_pat_xxxxxxxxxxxxxxxxx
python github_backup.py

Then run:

python github_backup.py
Option 2: Hardcode It (Simplest)

Replace:

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

with:

GITHUB_TOKEN = "github_pat_xxxxxxxxxxxxxxxxx"

and remove or comment out:

if not GITHUB_TOKEN:
    raise RuntimeError(
        "Set GITHUB_TOKEN environment variable first."
    )

Example:

GITHUB_TOKEN = "github_pat_xxxxxxxxxxxxxxxxx"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}
Option 3: Token File (My Preference for Local Backups)

Create a file:

token.txt

containing:

github_pat_xxxxxxxxxxxxxxxxx

Then change the script to:

with open("token.txt", "r", encoding="utf-8") as f:
    GITHUB_TOKEN = f.read().strip()

This avoids putting the token in source code while keeping execution simple.

One additional recommendation: after the backup finishes, compress the entire backup directory:

tar -czf github_backup.tar.gz github_backup

or on Windows:

Compress-Archive github_backup github_backup.zip

That gives you a portable snapshot containing the mirrored repositories and metadata.

