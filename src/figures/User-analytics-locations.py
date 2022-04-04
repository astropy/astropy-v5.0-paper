# -*- coding: utf-8 -*-
# +
import copy

import astropy.coordinates as coord
import astropy.table as at
import matplotlib as mpl
import matplotlib.pyplot as plt
# %matplotlib inline
import numpy as np

import pandas as pd
import geopandas as gp
# -

# Voting members:

# +
voting_member_locations = [
    "Boston, MA USA", 
    "Baltimore, MD USA", 
    "St. Andrews, Scotland", 
    "Amherst, MA USA", 
    "Paris, France", 
    "Madrid, Spain", 
    "Baltimore, MD USA", 
    "Marseille, France", 
    "Ann Arbor, MI USA", 
    "Moorhead, MN USA", 
    "New York, NY USA", 
    "Baltimore, MD USA", 
    "Baltimore, MD USA", 
    "Urbana, IL USA", 
    "Baltimore, MD USA", 
    "Hilo, Hawaii USA", 
    "Gainesville, FL USA", 
    "New York, NY USA", 
    "Baltimore, MD USA", 
    "Boston, MA USA", 
    "Göttingen, Germany", 
    "Baltimore, MD USA", 
    "Sheffield, England", 
    "Bern, Switzerland", 
    "Holmfirth, England", 
    "Toronto, Canada", 
    "New York, NY USA", 
    "Holmfirth, England", 
    "Greenbelt, MD USA", 
    "Pasadena, CA USA", 
    "Penticton, Ontario, Canada", 
    "Greenbelt, MD USA", 
    "Pasadena, CA USA", 
    "Baltimore, MD USA", 
    "Toronto, Canada", 
    "Potsdam, Germany", 
    "dwingeloo, netherlands", 
    "Baltimore, MD USA", 
    "La Serena, Chile", 
    "Toronto, Canada", 
    "Hong Kong"
]

coco_locations = [
    "Boston, MA USA", 
    "Baltimore, MD USA", 
    "Moorhead, MN USA",
    "New York, NY USA",
    "New York, NY USA"
]

# +
_loc_cache = {}
for name in voting_member_locations:
    if name not in _loc_cache:
        _loc_cache[name] = coord.EarthLocation.of_address(name)
        
for name in coco_locations:
    if name not in _loc_cache:
        _loc_cache[name] = coord.EarthLocation.of_address(name)

# +
voting_member_lonlat = np.array([
    [x.lon.degree, x.lat.degree] 
    for x in _loc_cache.values()
])

coco_lonlat = np.array([
    [_loc_cache[x].lon.degree, 
     _loc_cache[x].lat.degree] 
    for x in coco_locations
])
# -

analytics = at.Table.read(
    '../static/Astropy-2021-location-analytics.csv', 
    format='ascii.csv'
).filled('')
analytics['Country'] = analytics['Country'].astype(str)
analytics['Users'] = np.array([
    x.replace(',', '') for x in analytics['Users']],
    dtype=int
)
analytics

# +
world = gp.read_file(gp.datasets.get_path('naturalearth_lowres'))
world = at.Table.from_pandas(world)
world['Country'] = world['name'].astype(str)

analytics_name_map = {
    'Bosnia and Herz.': 'Bosnia & Herzegovina',
    'Dem. Rep. Congo': 'Congo - Kinshasa',
    'Congo': 'Congo - Brazzaville',
    "Côte d'Ivoire": "Côte d’Ivoire",
    "Dominican Rep.": "Dominican Republic",
    "Eq. Guinea": "Equatorial Guinea",
    "Guinea-Bissau": "Guinea",
    "Macedonia": "North Macedonia",
    "Myanmar": "Myanmar (Burma)",
    "Trinidad and Tobago": "Trinidad & Tobago",
    "Somaliland": "Somalia",
    "W. Sahara": "Western Sahara",
    'United States of America': 'United States'
}
for k, v in analytics_name_map.items():
    world['Country'][world['Country'] == k] = v
# -

np.isin(world['name'], analytics['Country']).sum()

# +
joined = at.join(world, analytics, keys='Country', join_type='left')
joined['Users'] = joined['Users'].filled(0)

good_mask = (joined['pop_est'] > 0) & (joined['Users'] > 0)
plot_world = gp.GeoDataFrame(joined.to_pandas())
# -

joined[joined['Users'] < 0]['name', 'Country', 'Users']

water_color = '#d6f3ff'
cmap = copy.copy(plt.get_cmap('magma'))
cmap.set_bad(color='w')

# +
fig, ax = plt.subplots(
    figsize=(12, 8.),
    constrained_layout=True
)
huh = plot_world.plot(
    column='Users',
    norm=mpl.colors.LogNorm(1, 1e5), 
    ax=ax,
    cmap=cmap,
    legend=True,
    legend_kwds={'label': "Number of Users per Country",
                 'orientation': "horizontal"}
)
ax.set_ylim(-180, 180)
ax.set_ylim(-90, 90)
ax.set_facecolor(water_color)

ax.scatter(
    voting_member_lonlat[:, 0], 
    voting_member_lonlat[:, 1],
    marker='o', s=40, edgecolor='#aaaaaa', linewidth=0.7,
    color='tab:green', label='voting member'
)

ax.scatter(
    coco_lonlat[:, 0], 
    coco_lonlat[:, 1],
    marker='o', s=40, edgecolor='#aaaaaa', linewidth=0.7,
    color='tab:red', label='coordination committee'
)
ax.legend(loc='lower left', fontsize=16)

ax.annotate('16/41 voting members\n4/5 CoCo members', 
            xy=(-72, 39), xytext=(-65, 23), ha='left', 
            fontsize=11, color='#444444',
            arrowprops=dict(facecolor='#555555', 
                            width=2, headwidth=8, headlength=10))

ax.add_patch(mpl.patches.Ellipse((-74, 40.5), 12, 5, angle=36, 
                                 facecolor='none', edgecolor='#aaaaaa'))

ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

ax.set_title("Astropy Documentation Web Analytics for Year 2021")

ax.set_xlim(-180, 180)
ax.set_ylim(-90, 90)
ax.set_facecolor(water_color)

fig.savefig('docu_analytics.pdf')
# -


