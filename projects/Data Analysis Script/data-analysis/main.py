"""
    Filename: data-analysis/main.py
    Developer: Matthew Pool
    Purpose: Data analysis of the annual temperature anomalies
    (annual temperature deviation from the long-term average temperature),
    based on NASA's global surface temperature dataset
    Data Source: https://data.giss.nasa.gov/gistemp/
"""
import pandas as pd  # For data manipulation & analysis
import matplotlib.pyplot as plt  # For data visualizations
import numpy as np  # For numerical computing with N-dimensional arrays
                    # Vectorized operations operate on whole arrays instead of individual elements

# Dataset source file
filename = 'temperatures.csv'

# Load data into a pandas DataFrame (df)
df = pd.read_csv(filename, skiprows=1)  # Skips top title row (1)

# List of column names in dataset to analyze
monthly_columns = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Clean: replace '***' values with NaN (ignored by pandas), and convert to float for arithmetic operations
df[monthly_columns] = df[monthly_columns].replace({'***': np.nan}).astype(float)

# Calculate annual mean temperature deviation for each year
# axis=1 : compute horizontally across columns
df['Annual_Mean'] = df[monthly_columns].mean(axis=1)

# Plot the annual mean temperature anomalies
plt.figure(figsize=(14, 7))  # (width, height)

# Data points
x = df['Year']  # x-axis values
y = df['Annual_Mean']  # y-axis values

# scatter plot
#plt.scatter(x, y, color='blue', marker='o')
# line chart
plt.plot(x, y, color='blue', linestyle='-')

# Polynomial best-fit line
coef = np.polyfit(x, y, 3)  # 3 degrees (cubic)
polynomial = np.poly1d(coef)  # creates best-fit polynomial
y_poly_fit = polynomial(x)  # calculated fitted y-values from each x-value
plt.plot(x, y_poly_fit, color='red', linewidth=1.5, linestyle='-')

# y=0.00 horizontal dashed line
plt.axhline(0, color='blue', linewidth=1, linestyle='--', label='Average Temperature')

# Labels
plt.xlabel('Year')
plt.ylabel('Temperature Deviation (°C)')
plt.title('Annual Global Surface Temperature Anomalies')

plt.grid(True)  # Provides plot gridlines
plt.show()  # Renders and displays plot
