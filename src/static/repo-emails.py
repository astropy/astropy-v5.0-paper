from collections import defaultdict
import pathlib
import git

# Get all emails that have contributed to astropy repositories:
repos_path = pathlib.Path(
    '~/projects/astropy-all/astropy-sustainability/cache/repos'
).expanduser().resolve()

repos = {}
for path in repos_path.glob("*"):
    if path.parts[-1].startswith('.'):
        continue

    repo_name = path.parts[-1]
    repos[repo_name] = git.Repo(path)

all_emails = []
for repo_name, repo in repos.items():
    shortlog_raw = repo.git.shortlog(
        'HEAD', s=True, n=True, e=True, no_merges=True,
    )
    lines = shortlog_raw.split('\n')

    shortlog = defaultdict(lambda *_: 0)
    for line in lines:
        ncommits, name_email = line.strip().split('\t')
        _, email = name_email.split('<')
        email = email[:-1]
        all_emails.append(email)
all_emails = set(all_emails)

_emails = [f'{x}\n' for x in list(set(all_emails))
           if 'users.noreply' not in x
           and 'github' not in x
           and '.local' not in x
           and 'HP-Pavilion' not in x
           and '@' in x
           and 'gitter.im' not in x
           and '0101010101.com' not in x
           and x != 'anonymous@overleaf.com']

with open('repo-emails.txt', 'w') as f:
    f.writelines(_emails)
repo_emails = [x.strip() for x in _emails]

# Load the form emails:
with open("form-emails.txt", "r") as f:
    form_emails = [x.strip() for x in f.readlines()]

all_emails = sorted(set(repo_emails + form_emails))
print(len(all_emails))
print()
print("--- BATCH 1: ---")
print(", ".join(all_emails[:400]))

print("\n\n\n--- BATCH 2: ---")
print(", ".join(all_emails[400:]))
