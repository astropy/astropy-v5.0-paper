"""
Generate the affiliated package table items file.
"""
import json
import re


# Downloaded registry into static directory as of 2022-03-12

with open('../static/registry.json') as data_file:
    data = json.load(data_file)

# with open('bib_mapping.json') as data_file:
#     bib_map = json.load(data_file)

package_list = sorted(data['packages'], key=lambda k: k['name'].lower())
print(package_list)

row = (
    '\\href{{{url}}}{{{name}}} & '
    '\\href{{https://pypi.python.org/pypi/{pypi_name}}}{{{3}}} & '
    '{maintainer} & {cite_key} \\\\\n'
)

with open("../generated/affiliated-table.tex", "w") as f1:
    for item in package_list:

        # citealt = ("\\citealt{{{0}}}".format(bib_map[item["name"]])
        #            if item["name"] in bib_map
        #            else "")

        maintainer = re.sub(' [<(].*?[>)]', '', item["maintainer"])

        name = re.sub('_', '\_', item["name"])

        f1.write(
            row.format(
                url=item["repo_url"],
                name=name,
                pypi_name=item['pypi_name'],
                maintainer=maintainer,
                cite_key='test'
            )
        )
