# Geospatial Data Visualization Package

## About
This package provides a convenient way to create heatmaps for geospatial data using Python's `GeoPandas` and `Matplotlib`.

## Features

- Merge DataFrames with GeoDataFrames
- Clean data by removing NA values
- Create customizable heatmaps with defined color transitions

## Directory Structure

The directory structure should be looking something like - 

```arduino
my_project/
│
├── plotting/
│   ├── __init__.py
│   └── plotting.py
│
├── scripts/
│   └── your_script.py
│
└── setup.py
```

### You can write this code in your `setup.py` file:

```python
from setuptools import setup, find_packages

setup(
    name='geospatial_visualization',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A module for plotting geospatial data visualizations using heatmaps.',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'geopandas',
        'matplotlib',
        'scikit-learn',  # Add any other dependencies your project needs
    ],
)

```

## Installation

To install this package, clone the repository and run the following command in the `my_project` directory:

```bash
pip install .
```

# Usage

Here’s how to use the `Plotting` class in your script:

```python
from plotting import Plotting

# Initializing the Plotting object
plotter = Plotting(map_file='path/to/shapefile.shp',
                   df='path/to/data.csv',
                   df_column_name='column_name',
                   merge_type='inner',
                   gdf_column_name='gdf_column_name')

# Cleaning the data
plotter.clean_data()

# Creating a heatmap
plotter.plotting(title='Heatmap Title',
                 column_to_plot='column_to_plot',
                 color1='red',
                 color2='pink',
                 color3='blue',
                 legend_title='Population')

```
