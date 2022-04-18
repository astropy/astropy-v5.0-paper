# -*- coding: utf-8 -*-
# +
import os
import pathlib

import astropy.table as at
import matplotlib as mpl
import matplotlib.pyplot as plt
# %matplotlib inline
import numpy as np

from pylatexenc.latexencode import unicode_to_latex
from git import Repo

# +
authors = at.Table.read('../static/authors-raw.csv')
authors = authors.filled('')

# Sort by last name:
argsort = np.argsort([
    x.split()[-1] 
    for x in authors['Your name (as it will appear in the journal)']
])
authors = authors[argsort]
# -

name_col = 'Your name (as it will appear in the journal)'
email_col = 'Email address you use with Git'
affil_col = 'Institutional affiliation'

# Fix some author input:

# +
_mask = authors[name_col] == 'Benjamin Winkel'
_fixed = r'Max-Planck-Institut f{\"u}r Radioastronomie, Auf dem H{\"u}gel 69, 53121 Bonn, Germany'
authors[affil_col][_mask] = _fixed

_mask = np.array(['Salgado' in x 
                  for x in authors['Your name (as it will appear in the journal)']])
_fixed = r"Jes\'us~Salgado"
assert _mask.sum() == 1
authors[name_col][_mask] = _fixed
# -

# Now process:

form_emails = authors[email_col]

_astropy_path = os.environ.get('ASTROPY_REPO_PATH', '../../../astropy')
astropy_repo_path = pathlib.Path(_astropy_path)
repo = Repo(astropy_repo_path)

emails = repo.git.log(
    'HEAD', 
    format="%ae"
).split("\n")
unq_emails = set([x.lower() for x in emails])

with open("../static/authors-emails-vetted.txt", "r") as f:
    vetted_emails = [x.strip() for x in f.readlines()]

# Unvetted authors:

unvetted = authors[
    ~(np.isin(authors[email_col], list(unq_emails)) | 
      np.isin(authors['Email Address'], list(unq_emails)) |
      np.isin(authors[email_col], vetted_emails))
]
unvetted[name_col, email_col].pprint(max_width=1000)

if len(unvetted) > 0:
    raise RuntimeError("Unvetted authors in the authorship form results!")

all_authors = []
for row in authors:
    # Author name
    name = row['Your name (as it will appear in the journal)']
    if "\\" not in name:
        name = unicode_to_latex(name)
    name = name.replace(" ", "~")

    if len(row['Your ORCID (if you have one)']) > 0:
        orcid = f"[{row['Your ORCID (if you have one)'].strip()}]"
    else:
        orcid = ''
    author = rf"\author{orcid}{{{name}}}"

    # Affiliation
    if (
            len(row['Institutional affiliation']) > 0 
            and row['Institutional affiliation'] != 'None'
            and row['Institutional affiliation'] != 'Unaffiliated'
    ):
        affils = row['Institutional affiliation'].split(";")
        affil = '\n' + "\n".join([rf"\affiliation{{{a.strip()}}}" for a in affils])
        affil = affil.replace("#", "No.")
        affil = affil.replace(" &", r" \&")
        affil = affil.replace(r"\´", r"\'")
        affil = affil.replace("’", "'")
    else:
        affil = '\n' + r'\noaffiliation'

    # Alt affiliation / footnotes:
    if len(row['Footnote to your name?']) > 0 and row['Footnote to your name?'] != 'None':
        # TODO: is this right?
        altaffil = '\n' + rf"\altaffiliation{{{row['Footnote to your name?']}}}"
    else:
        altaffil = ''

    full_author_block = author + affil + altaffil + "\n"
    all_authors.append(full_author_block)
#     print(full_author_block)

with open('../static/authors.tex', 'w') as f:
    f.write("\n".join(all_authors))


