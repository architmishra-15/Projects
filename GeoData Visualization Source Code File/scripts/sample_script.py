from plotting.plotting import Plotting

# Define the file paths and parameters
map_file = 'path_to_your_shapefile.shp'
data_file = 'path_to_your_data.csv'
df_column_name = 'your_data_column'
gdf_column_name = 'your_shapefile_column'
merge_type = 'inner'  # or 'outer', 'left', 'right' depending on your needs
legend_alignment = 'vertical'  # or 'horizontal'

# Create an instance of the Plotting class
plotter = Plotting(
    map_file=map_file,
    df=data_file,
    df_column_name=df_column_name,
    merge_type=merge_type,
    gdf_column_name=gdf_column_name,
    alignment=legend_alignment
)

# Clean the data
plotter.clean_data()

# Preprocess the GeoDataFrame (optional)
plotter.preprocessing_gdf(case='lower')

# Plot the heatmap
plotter.plotting(
    title='Your Plot Title',
    column_to_plot='your_column_to_plot',
    color1='red',
    color2='pink',
    color3='blue',
    legend_title='Your Legend Title',
    na_color='grey'
)
