"""
Generate the affiliated package table items file.
"""
import json
import pathlib
import re
from pylatexenc.latexencode import unicode_to_latex


this_path = pathlib.Path(__file__).parent.resolve()

# Downloaded registry into static directory as of 2022-03-12

with open(this_path / '../static/registry.json') as data_file:
    data = json.load(data_file)

with open(this_path / '../static/affiliated-refs.bib') as bib_file:
    bib_text = bib_file.read()

pattr = re.compile(r"@[a-zA-Z]+\{([a-zA-Z:0-9\-]+),[\s\S]+?[\}]{0,1}\n\}")
bib_map = {}
for m in pattr.finditer(bib_text):
    cite_name = m.groups()[0]
    bib_record = m.string[m.start():m.end()]

    pkg_name = cite_name
    if ":" in cite_name:
        pkg_name = cite_name.split(':')[0]

    if pkg_name not in bib_map:
        bib_map[pkg_name] = {'bib': [bib_record], 'cite': [cite_name]}
    else:
        bib_map[pkg_name]['bib'].append(bib_record)
        bib_map[pkg_name]['cite'].append(cite_name)

package_list = sorted(data['packages'], key=lambda k: k['name'].lower())

row = (
    '\\href{{{url}}}{{{name}}} & '
    '\\href{{https://pypi.python.org/pypi/{pypi_name}}}{{{pypi_name}}} & '
    '{maintainer} & {cite_command} \\\\\n'
)

lines = []
for pkg in package_list:
    if pkg['name'] == 'astropy core package':
        continue

    if pkg['name'] not in bib_map:
        print(f"{pkg['name']} not in bib file")

    cite_cmd = ""
    if pkg['name'] in bib_map:
        cite_cmd = r",\newline ".join([
            f"\\citet{{{cite_key}}}"
            for cite_key in bib_map[pkg['name']]['cite']
        ])

    # Parse list of maintainers to make line wrapping better:
    maintainer_block = re.sub(' [<(].*?[>)]', '', pkg["maintainer"])
    maintainers = [x.split(',') for x in maintainer_block.split(' and ')]
    maintainers = [x.strip() for x in sum(maintainers, [])
                   if len(x.strip()) > 0]
    maintainers = [unicode_to_latex(x).replace(" ", "~")
                   for x in maintainers]

    name = re.sub('_', r'\_', pkg["name"])
    pypi_name = re.sub('_', r'\_', pkg["pypi_name"])

    lines.append(
        row.format(
            url=pkg["repo_url"],
            name=name,
            pypi_name=pypi_name,
            maintainer=r",\newline ".join(maintainers),
            cite_command=cite_cmd
        )
    )

print("\n".join(lines))

with open(this_path / "../generated/affiliated-table.tex", "w") as f1:
    f1.writelines(lines)
