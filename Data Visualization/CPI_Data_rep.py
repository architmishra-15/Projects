# -*- coding: utf-8 -*-
"""CPI_Data_rep.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JNMu6yF8MXg1y69gXodqahrv9FY8G17X
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('/content/CPI Wheat Data.csv')

df.head()

df = pd.read_csv('/content/CPI Wheat Data.csv')

df['Date'] = df['Year'].astype(str) + ' ' + df['Month']

df.head()

# Convert the 'Date' column to datetime format

df['Date'] = pd.to_datetime(df['Date'], format='%Y %B')

df.head()

plt.plot(df['Date'], df['Inflation (%)'], marker='o', linestyle='-', label='Consumer Price Index')
plt.xlabel('Date')
plt.ylabel('Inflation (%)')
plt.title('Consumer Price Index Trend (2023-2024)')
plt.xticks(rotation=45)  # Rotate x-axis labels for readability
plt.grid(True)
plt.legend()
plt.show()

# Filter data for the year 2024
df_2024 = df[df['Year'] == 2024]

# Filter data for Wheat/ Atta – PDS and Wheat/ Atta – Other Sources
wheat_pds = df_2024[df_2024['Item'] == 'Wheat/ Atta – PDS']
wheat_other = df_2024[df_2024['Item'] == 'Wheat/ Atta – Other Sources']

# Set an index for the bars
index = np.arange(len(wheat_pds))

# Set the width of the bars
bar_width = 0.35

# Create the grouped bar chart
fig, ax = plt.subplots()
summer = ax.bar(index, wheat_pds['Inflation (%)'], bar_width, label='Wheat/ Atta – PDS', color='red', alpha=0.7)
winter = ax.bar(index + bar_width, wheat_other['Inflation (%)'], bar_width, label='Wheat/ Atta – Other Sources', color='blue', alpha=0.7)

ax.set_xlabel('Month')
ax.set_ylabel('Inflation (%)')
ax.set_title('Comparison of Wheat/ Atta Prices (2024)')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(wheat_pds['Month'])
ax.legend()

plt.show()

# Filter data for Wheat/ Atta – PDS and Wheat/ Atta – Other Sources
wheat_pds = df[df['Item'] == 'Wheat/ Atta – PDS']
wheat_other = df[df['Item'] == 'Wheat/ Atta – Other Sources']

# Set an index for the bars
index = np.arange(len(wheat_pds))

# Set the width of the bars
bar_width = 0.35

plt.figure(figsize=(10, 6))  # Adjust width (10 inches) and height (6 inches)
# Create the grouped bar chart
fig, ax = plt.subplots()
ax.bar(index, wheat_pds['Inflation (%)'], bar_width, label='Wheat/ Atta – PDS', color='red', alpha=0.7)
ax.bar(index + bar_width, wheat_other['Inflation (%)'], bar_width, label='Wheat/ Atta – Other Sources', color='blue', alpha=0.7)

ax.set_xlabel('Month')
ax.set_ylabel('Inflation (%)')
ax.set_title('Comparison of Wheat/ Atta Prices (2024)')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(wheat_pds['Month'], rotation=45)  # Rotate x-axis labels
ax.legend()

plt.tight_layout()  # Adjust layout to prevent label overlap
plt.show()

df_2 = pd.read_csv("/content/CPI Rice Data.csv")
df_2.head()

df_2['Date'] = df_2['Year'].astype(str) + ' ' + df_2['Month']

df_2['Date'] = pd.to_datetime(df_2['Date'], format='%Y %B')

df_2.head()

df_2024_2 = df_2[df_2['Year'] == 2024]

# Filter data for Wheat/ Atta – PDS and Wheat/ Atta – Other Sources
wheat_pds = df_2024_2[df_2024_2['Item'] == 'Rice – PDS']
wheat_other = df_2024_2[df_2024_2['Item'] == 'Rice – Other Sources']

# Set an index for the bars
index = np.arange(len(wheat_pds))

# Set the width of the bars
bar_width = 0.35

# Create the grouped bar chart
fig, ax = plt.subplots()
summer = ax.bar(index, wheat_pds['Inflation (%)'], bar_width, label='Rice – PDS', color='red', alpha=0.7)
winter = ax.bar(index + bar_width, wheat_other['Inflation (%)'], bar_width, label='Rice – Other Sources', color='blue', alpha=0.7)

ax.set_xlabel('Month')
ax.set_ylabel('Inflation (%)')
ax.set_title('Comparison of Inflation of Rice Prices (2024)')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(wheat_pds['Month'])
ax.legend()

plt.show()

df_2024_2 = df_2[df_2['Year'] == 2024]

# Filter data for Wheat/ Atta – PDS and Wheat/ Atta – Other Sources
wheat_pds = df_2024_2[df_2024_2['Item'] == 'Rice – PDS']
wheat_other = df_2024_2[df_2024_2['Item'] == 'Rice – Other Sources']

# Set an index for the bars
index = np.arange(len(wheat_pds))

# Set the width of the bars
bar_width = 0.35

# Create the grouped bar chart
fig, ax = plt.subplots()
summer = ax.bar(index, wheat_pds['Index'], bar_width, label='Rice – PDS', color='red', alpha=0.7)
winter = ax.bar(index + bar_width, wheat_other['Index'], bar_width, label='Rice – Other Sources', color='blue', alpha=0.7)

ax.set_xlabel('Month')
ax.set_ylabel('Index')
ax.set_title('Comparison of Rice Prices (2024)')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(wheat_pds['Month'])
ax.legend()

plt.show()

