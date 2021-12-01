"""
TODO: describe
"""

# Standard library
import datetime
import pathlib

# Third-party
import ads
import astropy.table as at
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_papers(query, rows_per_page=100, max_pages=100):
    """
    Parameters
    ----------
    query : str
    rows_per_page : int (optional)
    max_pages : int (optional)

    Returns
    -------
    search_query : `ads.SearchQuery`
    papers_df : `pandas.DataFrame`
    """
    q = ads.SearchQuery(q=query,
                        sort="date",
                        max_pages=max_pages,
                        rows=rows_per_page,
                        fl=["identifier", "title", "author", "year",
                            "pubdate", "pub", "citation_count"])

    all_dicts = []
    for paper in q:
        # Get arxiv ID
        aid = [":".join(t.split(":")[1:]) for t in paper.identifier
               if t.startswith("arXiv:")]

        all_dicts.append(dict(
            authors='; '.join(paper.author) if paper.author else '',
            year=int(paper.year) if paper.year is not None else -1,
            pubdate=paper.pubdate if paper.pubdate is not None else '',
            title=paper.title[0] if paper.title is not None else '',
            pub=paper.pub if paper.pub is not None else '',
            arxiv=aid[0] if len(aid) else '',
            citations=(paper.citation_count
                       if paper.citation_count is not None else 0)
        ))

    papers = at.Table(sorted(all_dicts, key=lambda x: x['pubdate'],
                             reverse=True))

    # Convert list of papers to pandas DataFrame
    df = papers.to_pandas()
    df['pubdate'] = np.array([
        datetime.datetime(
            int(x.split('-')[0]),  # year
            max(1, int(x.split('-')[1])),  # month
            1  # first day of the month
        )
        for x in df['pubdate']
    ])
    df.index = df['pubdate']
    df = df.sort_index()

    return q, df


def get_dfs(cache_path):
    cache_path = pathlib.Path(cache_path)
    queries = {
        'Python': (
            'full:"python" property:"refereed" collection:"astronomy"'),
        'IDL': (
            'full:"idl" property:"refereed" collection:"astronomy"'),
        'Matlab': (
            'full:"matlab" property:"refereed" collection:"astronomy"'),
        'Julia': (
            'full:"julia" property:"refereed" collection:"astronomy"'),
        'FORTRAN': (
            'full:"fortran" property:"refereed" collection:"astronomy"')
    }

    dfs = {}
    for name, query in queries.items():
        filename = cache_path / f'{name}.csv'
        if not filename.exists():
            q, papers_df = get_papers(query, rows_per_page=1000, max_pages=100)
            papers_df.to_csv(filename)

        dfs[name] = pd.read_csv(filename,
                                index_col='pubdate',
                                parse_dates=True)

    return dfs


def plot_yearly_mentions(paper_dfs):
    fig, ax = plt.subplots(figsize=(8, 6), constrained_layout=True)

    for i, (name, df) in enumerate(paper_dfs.items()):
        g = df.groupby(by=[df.index.year]).count()
        group_dates = np.array([datetime.date(x, 1, 1) for x in g.index])
        mentions = g['pubdate.1'].values

        if name.lower() == 'julia':
            jmask = group_dates > datetime.date(2012, 1, 1)
            group_dates = group_dates[jmask]
            mentions = mentions[jmask]

        ax.plot(group_dates,
                mentions,
                marker='', drawstyle='steps-mid',
                lw=2, label=name, zorder=-i)

    ax.set_xlim(datetime.date(1991, 8, 1),
                datetime.date(2021, 6, 1))  # 2021.5

    ax.legend(loc='upper left', fontsize=16)

    ax.set_xlabel('Time [year]')
    ax.set_ylabel('Full-text mentions per year')

    fig.savefig("python-mentions.pdf", bbox_inches="tight")


if __name__ == "__main__":
    cache_path = pathlib.Path('cache/prog-lang-fulltext')
    cache_path.mkdir(exist_ok=True, parents=True)

    paper_dfs = get_dfs(cache_path)
    plot_yearly_mentions(paper_dfs)
