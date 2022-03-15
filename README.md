Astropy Paper III
=================

<p align="center">
<a href="https://github.com/astropy/astropy-v5.0-paper/actions/workflows/showyourwork.yml">
<img src="https://github.com/astropy/astropy-v5.0-paper/actions/workflows/showyourwork.yml/badge.svg" alt="Article status"/>
</a>
<a href="https://github.com/astropy/astropy-v5.0-paper/blob/main-pdf/ms.pdf">
<img src="https://img.shields.io/badge/article-pdf-blue.svg?style=flat" alt="Read the article"/>
</a>
<a href="https://github.com/astropy/astropy-v5.0-paper/blob/main-pdf/dag.pdf">
<img src="https://img.shields.io/badge/article-dag-blue.svg?style=flat" alt="Article graph"/>
</a>
</p>

Scope of the Paper
------------------

Our goal is to produce a brief and informative description of major updates
about the Astropy Project, drawing on relevant changes or news since 2018 (the
last paper).


Journal
-------

The paper will be jointly submitted to the software section of the
Astrophysical Journal and the Journal of Open Source Software.


Coordinators
------------

Please feel free to reach out with comments or feedback by creating issues in
this repository, or by messaging any of the Paper Coordinators:

- Adrian Price-Whelan
- Nicholas Earl
- Pey Lian Lim

If you are contributing text to the paper, please see the [Contributing
document](https://github.com/astropy/astropy-v5.0-paper/blob/main/CONTRIBUTING.md).


Rules for Authorship
--------------------

We invite you to become a co-author if any of the following applies to you:

   - You have an official role in the project, as defined on http://www.astropy.org/team.html
   - You are a Voting Member, as listed on https://www.astropy.org/team.html#votingmembers
   - You have contributed code to the core package
   - You have contributed to Astropy Project infrastructure, including:
      - Sphinx plugins (within the Astropy organization)
      - Pytest plugins (within the Astropy organization)
      - Astropy package template
      - Astropy Website
      - Learn Astropy
   - You have contributed to one of the following Astropy coordinated packages (see http://affiliated.astropy.org/):
      - astropy-healpix
      - astroquery
      - ccdproc
      - photutils
      - regions
      - reproject
      - specutils / specreduce

If you would like to be a co-author, please complete the [Google form
here](https://forms.gle/M93XBNaGbPqoncuE8). If the above does not apply to you
but you feel that you should still be considered for co-authorship, please
complete the form and your application will be reviewed.

The author order will be 'The Astropy Collaboration' as the first author,
followed by people who have contributed significantly to the paper, in order of
contribution level (or alphabetically where contribution levels are similar),
and all other authors will then be listed alphabetically. A note will be
included to indicate the author list and how it was determined.

Building the paper locally
--------------------------

This paper and project uses
[showyourwork](https://github.com/rodluger/showyourwork/) to build the article.
This is a new tool that aims to improve the reproducibility of scientific
articles. Under the hood, this ultimately uses Latex to generate the rendered
PDF, but also uses [Snakemake](https://snakemake.readthedocs.io/) to enable
constructing a pipeline of dependencies that generate build components (e.g.,
figures, tables, datasets, etc.) automatically during the paper build process.
Importantly, **this means that you can not simply change directory into the src
path and use `pdflatex` to build the paper**. To build the PDF of the article,
you need to use the `Makefile` at the repository root. Building locally required
having `anaconda`, `snakemake`, and a Latex installation on your machine. With
these, in the repository root, run:

   make

This *should* automatically install all of the required dependencies into a
`conda` environment and build the paper with this environment. If this fails for
you, please open an issue.
