import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter

def mapVisualizationUsa(dataframe, state_column_name, variable):
    """Generate a map visualization for the USA."""

    # Merge DataFrame wtih gdf
    gdf = gpd.read_file('../data/raw/cb_2018_us_state_500k')
    gdf = gdf.merge(dataframe, left_on='STUSPS', right_on=state_column_name)

    # Apply this the gdf to ensure that all states are assigned colors by the same function
    def makeColorColumn(gdf, variable, vmin, vmax):
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax, clip=True)
        mapper = plt.cm.ScalarMappable(norm=norm, cmap=plt.cm.YlOrBr)
        gdf['value_determined_color'] = gdf[variable].apply(lambda x: mcolors.to_hex(mapper.to_rgba(x)))
        return gdf
    gdf = makeColorColumn(gdf, variable, gdf[variable].min(), gdf[variable].max())
    visframe = gdf.to_crs('epsg:2163')

    # Create the map
    fig, ax = plt.subplots(1, figsize=(16, 12))
    ax.axis('off')
    ax.set_title('Patient Satisfaction - ' + variable, fontdict={'fontsize': '42', 'fontweight': '1'})

    # Create colorbar legend
    fig = ax.get_figure()
    cbax = fig.add_axes([0.8, 0.3, 0.03, 0.25])
    cbax.set_title(variable, fontdict={'fontsize': '15', 'fontweight': '0'})
    # Add continuous color scale 
    sm = plt.cm.ScalarMappable(cmap="YlOrBr", norm=plt.Normalize(vmin=gdf[variable].min(), vmax=gdf[variable].max()))
    comma_fmt = FuncFormatter(lambda x, p: format(x/100, '.0%'))
    fig.colorbar(sm, cax=cbax, format=comma_fmt)
    cbax.tick_params(labelsize=16)
    ax.annotate("Data: Centers for Medicare & Medicaid Services Data, snapshot date 01/31/2024", xy=(0.22, .085), xycoords='figure fraction', fontsize=14, color='#555555')

    # Note: we're going state by state here because of unusual coloring behavior when trying to plot the entire dataframe using the "value_determined_color" column
    for row in visframe.itertuples():
        if row.STUSPS not in ['AK', 'HI']:
            c = gdf[gdf.STUSPS == row.STUSPS][0:1].value_determined_color.item()
            visframe[visframe.STUSPS == row.STUSPS].plot(color=c, linewidth=0.8, ax=ax, edgecolor='0.8')
            # Add State labels to the map
            ax.text(row.geometry.centroid.x, row.geometry.centroid.y, row.STUSPS, fontsize=10, ha='center')