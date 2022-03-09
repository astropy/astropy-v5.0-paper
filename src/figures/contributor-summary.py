# -*- coding: utf-8 -*-
# Ideas for plots:
# - Commits per month
# - Commiters per month
# - Lines of code added/removed per month (harder)
# - Contributors x commits in bins of astropy eras
# - Breakdown of career stage of top N committers in different eras (early, mid, present)
#     - Eras: 2012–2015, 2015–2018, 2018–present
#     - Or maybe only include committers that contribute a certain number of line changes?
#
#
# Stretch goals:
# - For committers, did they start by opening an issue or go right to PR?

# ---

# +
from collections import defaultdict
import datetime
import pathlib

from astropy.time import Time
import astropy.units as u
from git import Repo
import matplotlib.pyplot as plt
import numpy as np
# -

astropy_repo_path = pathlib.Path(
    '/Users/apricewhelan/projects/astropy-all/astropy')

repo = Repo(astropy_repo_path)

first_commit_hash = repo.git.log('--pretty=format:%h', '--reverse').split('\n')[0]
first_commit = list(repo.iter_commits(max_count=1, rev=first_commit_hash))[0]
first_date = Time(first_commit.committed_date, format='unix')
first_date.datetime

# Date of last commit in v5.0
v50_date = Time(datetime.datetime(2021, 11, 19))
total_days = int((v50_date - first_date).jd)
total_days

# ### Time ranges:

month_bins = (
    first_date + np.arange(0, total_days, 30).astype(int) * u.day
)

# +
# 4 bin edges for 3 eras
era_edges = (
    first_date + np.linspace(0, total_days, 4).astype(int) * u.day
)

eras = {
    'early': (era_edges[0], era_edges[1]),
    'mid': (era_edges[1], era_edges[2]),
    'recent': (era_edges[2], era_edges[3]),
}
print(
    f"Each era is ~{(eras['early'][1]-eras['early'][0]).jd/365:.1f} years"
)

for name, era in eras.items():
    print(f"{name}: {era[0].datetime:%Y-%m-%d} to {era[1].datetime:%Y-%m-%d}")
# -

# ### Plot style things:

figsize = (8.5, 6)
style = dict(color='k')

# ## Commits per month

commits_per_month = []
for after_dt, before_dt in zip(month_bins[:-1].datetime,
                               month_bins[1:].datetime):
    count = repo.git.rev_list(['--count', '--all', '--no-merges',
                               f'--after={after_dt:%Y-%m-%d}',
                               f'--before={before_dt:%Y-%m-%d}'])
    commits_per_month.append(int(count))

freeze_dates = [
    '2021-10-29', '2021-05-03', '2020-10-26', '2020-04-24', '2019-11-10',
    '2019-04-24', '2018-10-28', '2017-12-24', '2017-06-27', '2016-12-07',
    '2016-05-13', '2015-10-15', '2014-12-19', '2014-05-02',
]
freeze_dates = Time(freeze_dates, format='iso')

# +
fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)
ax.plot(
    month_bins[:-1].datetime,
    commits_per_month,
    drawstyle='steps',
    marker='',
    **style
)

_label = True
for _date in freeze_dates.datetime:
    if _label:
        kw = dict(label='feature freeze')
        _label = False
    else:
        kw = dict()
    ax.axvline(_date, color='tab:blue', alpha=0.2, zorder=-10, marker='',
               **kw)

ax.set_xlim(month_bins[0].datetime, month_bins[-1].datetime)
ax.set_xlabel('date')
ax.set_ylabel('commits per month')

ax.legend(loc='upper left', fontsize=18)
# -

# ## Committers per month

committers_per_month = []
for after_dt, before_dt in zip(month_bins[:-1],
                               month_bins[1:]):
    shortlog = repo.git.shortlog(
        'HEAD', s=True, n=True, no_merges=True,
        after=f"{after_dt.datetime:%Y-%m-%d}",
        before=f"{(before_dt + 1*u.day).datetime:%Y-%m-%d}"
    )
    committers_per_month.append(len(shortlog.split('\n')))

fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)
ax.plot(
    month_bins[:-1].datetime,
    committers_per_month,
    drawstyle='steps',
    marker='',
    **style
)
ax.set_xlim(month_bins[0].datetime, month_bins[-1].datetime)
ax.set_xlabel('date')
ax.set_ylabel('committers per month')

# +
fig, axes = plt.subplots(2, 1, figsize=(8, 8),
                         sharex=True,
                         constrained_layout=True)

ax = axes[0]
ax.plot(
    month_bins[:-1].datetime,
    commits_per_month,
    drawstyle='steps',
    marker='',
    **style
)

_label = True
for _date in freeze_dates.datetime:
    if _label:
        kw = dict(label='feature freeze')
        _label = False
    else:
        kw = dict()
    ax.axvline(_date, color='tab:blue', alpha=0.2, zorder=-10, marker='',
               **kw)

ax.set_xlim(month_bins[0].datetime, month_bins[-1].datetime)
# ax.set_xlabel('date')
ax.set_ylabel('commits per month')

ax.legend(loc='upper left', fontsize=18)

# ---

ax = axes[1]
ax.plot(
    month_bins[:-1].datetime,
    committers_per_month,
    drawstyle='steps',
    marker='',
    **style
)
ax.set_xlim(month_bins[0].datetime, month_bins[-1].datetime)
ax.set_xlabel('date')
ax.set_ylabel('committers per month')

fig.savefig('commits_committers_per_month.pdf')
# -

# ## Number of commits x number of committers

full_shortlog = repo.git.shortlog(
    'HEAD', s=True, n=True, no_merges=True,
    before=f"{(v50_date + 1*u.day).datetime:%Y-%m-%d}"
).split('\n')
full_n_commits = [int(x.split('\t')[0]) for x in full_shortlog]

# +
fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)

_bins = 10 ** np.arange(0, 4+1e-3, 0.2)
ax.hist(full_n_commits, bins=_bins,
        histtype='stepfilled', color='tab:blue')

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('number of Git commits')
ax.set_ylabel('number of Git committers')

ax.plot(_bins, 150*_bins**-0.5, marker='')

xticks = [1, 10, 100, 1000]
ax.set_xticks(xticks)
ax.set_xticklabels([str(tick) for tick in xticks])

yticks = [1, 10, 100]
ax.set_yticks(yticks)
ax.set_yticklabels([str(tick) for tick in yticks])

ax.set_ylim(0.5, 200)
ax.set_xlim(_bins.min(), _bins.max())

ax.text(100, 20, r'$\propto \frac{1}{\sqrt{N}}$', fontsize=20)
# -

era_n_commits = {}
era_shortlogs = {}
for name, era_lim in eras.items():
    _shortlog = repo.git.shortlog(
        'HEAD', s=True, n=True, no_merges=True,
        after=f"{era_lim[0].datetime:%Y-%m-%d}",
        before=f"{(era_lim[1] + 1*u.day).datetime:%Y-%m-%d}"
    ).split('\n')
    era_shortlogs[name] = _shortlog
    era_n_commits[name] = np.array([int(x.split('\t')[0]) for x in _shortlog])

# +
_bins = np.logspace(-5, 0, 25)

fig, axes = plt.subplots(1, 3,
                         figsize=(15, 6),
                         sharex=True, sharey=True,
                         constrained_layout=True)

for ax, (name, _n_commits) in zip(axes, era_n_commits.items()):
    ax.hist(
        _n_commits / sum(_n_commits),
        bins=_bins,
        lw=2,
        histtype='step',
        label=name
    )
    ax.plot(_bins, 1.2e0*_bins**-0.5, marker='', color='tab:blue')
    ax.set_title(f"{name}\n{eras[name][0].datetime:%Y-%m} – {eras[name][1].datetime:%Y-%m}")

axes[-1].text(1e-2, 20, r'$\propto \frac{1}{\sqrt{N}}$',
              fontsize=20, color='tab:blue')

ax.set_xscale('log')
ax.set_yscale('log')

# for ax in axes:
axes[1].set_xlabel('fraction of total Git commits in time period')
axes[0].set_ylabel('number of Git committers')

xticks = 10 ** np.arange(-5., 0+1, 1)
ax.set_xticks(xticks)
ax.set_xlim(10**-4.5, 1e0)

yticks = [1, 10, 100]
ax.set_yticks(yticks)
ax.set_yticklabels([str(tick) for tick in yticks])

ax.set_ylim(0.5, 200)

fig.savefig('Ncommitters_vs_frac_commits.pdf')
# -

# ## Career stages

import astropy.table as at

for name, era in eras.items():
    print(name, "mid date: ",
          (era[0] + (era[1] - era[0]).jd * u.day / 2).datetime.date())

for name, shortlog in era_shortlogs.items():
    _tmp = np.array([l.strip().split('\t') for l in shortlog])
    _data = at.Table({'name': _tmp[:, 1], 'ncommits': _tmp[:, 0].astype(int)})
    subtbl = _data[_data['ncommits'] >= 50]  # .pprint()
    print(len(subtbl))
    subtbl.pprint()

# See top contributor Google sheet here: https://docs.google.com/spreadsheets/d/1iGiWn-KTG88lMZ6_79y1NkoK7kJ5-u5K6AajlQ8xVm0/edit#gid=1945969023

# +
top_contr_data = {
    'early': [9, 8, 6],
    'mid': [9, 11, 3],
    'recent': [10, 13, 3]
}
labels = ['research staff / faculty', 'software engineer', 'student']

fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)

ind = np.arange(len(labels))
width = 0.25

colors = ['C1', 'C2', 'C3']

for i, (name, _data) in enumerate(top_contr_data.items()):
    ax.bar(ind + i*width, _data, width, label=name, color=colors[i], alpha=0.8)

ax.set_title('Number of contributors with >50 commits per era')

ax.set_xticks(ind + width)
ax.set_xticklabels(labels)
ax.legend(loc='upper right', fontsize=18,
          title='Era:', title_fontsize=19)

ax.set_ylim(0, 15)

fig.savefig('top_contributors_career.pdf')
