import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
# import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap, LogNorm
# from matplotlib import mlab
# import matplotlib as mpl
import matplotlib.path as mpath
import matplotlib.patches as patch


class Plotting:
    def __init__(self, map_file: str, df: str, df_column_name: str, merge_type: str,
                 gdf_column_name: str, alignment: str = 'vertical'):
        self.map = map_file
        self.df = df
        self.column = df_column_name
        self.legend_alignment = alignment
        self.gdf_column = gdf_column_name
        self.type = merge_type

        if "csv" in self.df:
            self.data = pd.read_csv(self.df)
        elif "xl" in self.df:
            self.data = pd.read_excel(self.df)
        else:
            raise ValueError("Unsupported file format. Use CSV or Excel files.")

        self.gdf = gpd.read_file(self.map)
        self.data[self.column] = self.data[self.column].lower()
        self.gdf[self.gdf_column] = self.gdf[self.gdf_column].lower()

        self.merged = self.gdf.merge(self.df, right_on=self.gdf_column, left_on=self.column, how=self.type)

    def clean_data(self):
        """Remove all NA values from the data DataFrame."""
        self.data.dropna(inplace=True)
        print("NA values removed from the data DataFrame.")

    def preprocessing_gdf(self, case: str = None):
        if case == "lower":
            self.gdf[self.gdf_column] = self.gdf[self.gdf_column].str.lower()
            self.data[self.column] = self.data[self.column].str.lower()
        elif case == "capital":
            self.gdf[self.gdf_column] = self.gdf[self.gdf_column].str.capitalize()
            self.data[self.column] = self.data[self.column].str.capitalize()
        elif case == "upper":
            self.data[self.column] = self.data[self.column].str.upper()

    def plotting(self, title: str, column_to_plot: str, color1: str, color2: str, color3: str,
                 legend_title: str = 'Legend', na_color: str = 'grey'):

        if not hasattr(self, 'merged'):
            raise RuntimeError("Data not merged. Call 'merge_data' before plotting.")

        vmin = self.merged[column_to_plot].min()
        vmax = self.merged[column_to_plot].max()
        norm = LogNorm(vmin=vmin, vmax=vmax)

        custom_cmap = LinearSegmentedColormap.from_list(
            'custom_colormap',
            [(0, color1), (0.5, color2), (1, color3)],
            N=256
        )
        custom_cmap.set_bad(na_color)

        fig, ax = plt.subplots(1, figsize=(12, 12))
        ax.set_title(title, fontdict={'fontsize': 25, 'fontweight': 10, 'color': 'black'}, pad=0.01)

        cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=custom_cmap), ax=ax,
                          label=legend_title, orientation=self.legend_alignment, fraction=0.03, pad=0.01)
        cb.outline.set_visible(False)

        bot = -0.05
        top = 1.05

        xy_upper = np.array([[0, 1], [0, top], [1, top], [1, 1]])
        if self.legend_alignment == "horizontal":
            xy_upper = xy_upper[:, ::-1]

        color = cb.cmap(cb.norm(vmax))
        patch_upper = patch.PathPatch(
            mpath.Path(xy_upper, [mpath.Path.MOVETO, mpath.Path.CURVE4, mpath.Path.CURVE4, mpath.Path.CURVE4]),
            facecolor=color,
            linewidth=0,
            antialiased=False,
            transform=cb.ax.transAxes,
            clip_on=False,
        )
        cb.ax.add_patch(patch_upper)

        xy_lower = np.array([[0, 0], [0, bot], [1, bot], [1, 0]])
        if self.legend_alignment == "horizontal":
            xy_lower = xy_lower[:, ::-1]

        color = cb.cmap(cb.norm(vmin))
        patch_lower = patch.PathPatch(
            mpath.Path(xy_lower, [mpath.Path.MOVETO, mpath.Path.CURVE4, mpath.Path.CURVE4, mpath.Path.CURVE4]),
            facecolor=color,
            linewidth=0,
            antialiased=False,
            transform=cb.ax.transAxes,
            clip_on=False,
        )
        cb.ax.add_patch(patch_lower)

        xy_outline = np.array([[0, 0], [0, bot], [1, bot], [1, 0], [1, 1], [1, top], [0, top], [0, 1], [0, 0]])
        if self.legend_alignment == "horizontal":
            xy_outline = xy_outline[:, ::-1]

        curve = [mpath.Path.MOVETO, mpath.Path.CURVE4, mpath.Path.CURVE4, mpath.Path.CURVE4, mpath.Path.LINETO,
                 mpath.Path.CURVE4, mpath.Path.CURVE4, mpath.Path.CURVE4, mpath.Path.LINETO]
        path = mpath.Path(xy_outline, curve, closed=True)

        patch_outline = patch.PathPatch(
            path, facecolor="None", lw=1, transform=cb.ax.transAxes, clip_on=False
        )
        cb.ax.add_patch(patch_outline)
        ax.axis('off')

        self.merged.plot(column=column_to_plot, cmap=custom_cmap, norm=norm, linewidth=0.5, ax=ax,
                         edgecolor='0.2', legend=False, missing_kwds={'color': na_color})

        plt.show()
