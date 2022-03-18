import pathlib
from git import Repo

this_path = pathlib.Path(__file__).parent.resolve()

repo = Repo(this_path / '../..')
try:
    tag = repo.git.describe("HEAD", exact_match=True, tags=True)
except Exception:
    tag = None
    short_sha = repo.head.commit.hexsha[:7]

if tag is None:
    header = f"Git commit: {short_sha}"
else:
    header = f"Git tag: {tag}"

command = r"\newcommand{\gitHeader}" + f"{{{header}}}" + "\n"

with open(this_path / '../generated/git-header.tex', "w") as f:
    f.write(command)
