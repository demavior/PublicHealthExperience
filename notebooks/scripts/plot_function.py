import matplotlib.pyplot as plt
import numpy as np

def rating_correlation(df):
    """Calculate the correlation of the Rating Score with the other columns."""
    # Calculate correlation matrix among LINEAR SCORES
    corr_matrix = df.loc[:, df.columns[7:16]].corr()
    # Extract correlation coefficients for Rating Score
    rating_correlation = corr_matrix['Rating Score'].abs().sort_values(ascending=False).drop('Rating Score')
    return rating_correlation

def plot_barh(df, title, xlabel, ylabel, colors, xmax=None):
    xticks=None
    if xmax:
        xticks = np.arange(0, xmax*1.01, xmax/10)
    """Plot a horizontal bar chart for a DataFrame column."""
    plt.figure(figsize=(10, 6))
    df.plot(kind='barh', color=colors)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.gca().invert_yaxis()
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.xticks(xticks)
    plt.show()

def plot_barh_correlation(df, region=None, state=None):
    """Plot a horizontal bar chart for correlation data."""
    # Filter the DataFrame by state or region
    name = None
    if region:
        df = df[df['Region'] == region]
        name = region
    if state:
        df = df[df['State'] == state]
        name = df['State Name'].iloc[0]
    # Calculate the correlation of the Rating Score with the other columns
    correlation_df=rating_correlation(df)
    # Set colors top 2 green and bottom 2 red
    colors = ['green' if Measure in correlation_df[:2].index else 'red' if Measure in correlation_df[-2:].index else 'blue' for Measure in correlation_df.index.values]
    plot_barh(correlation_df, 
              'Importance of Categories for Patient Satisfaction'+(' in '+name if name else ''),
              "Correlation with Rating Score", 
              "Categories", 
              colors, 
              xmax=1)

def plot_region_correlation(completed_df):
    """Plot correlation by region."""
    # Define regions and corresponding colors
    region_colors = {
        'Midwest': 'green',
        'South': 'lightblue',
        'West': 'blue',
        'Northeast': 'darkblue',
        'U.S. Territories': 'red'
    }
    # Plot the correlation by region
    plt.figure(figsize=(10, 6))
    for i, (region, color) in enumerate(region_colors.items(), start=1):
        correlation_df = rating_correlation(completed_df[completed_df['Region'] == region]) 
        nation_correlation = rating_correlation(completed_df)
        correlation_df = correlation_df.reindex(nation_correlation.index)
        plt.barh(np.arange(len(correlation_df)) + i*0.15, correlation_df.values, height=0.15, color=color, label=region)
    # Customizing the plot
    plt.title('Importance of Categories for Patient Satisfaction by Region')
    plt.xlabel('Correlation with Rating Score')
    plt.ylabel('Categories')
    plt.yticks(np.arange(len(correlation_df)), correlation_df.index)
    plt.gca().invert_yaxis()
    plt.legend(loc='upper left', bbox_to_anchor=(.78, 0.30))
    plt.tight_layout()
    plt.show()

def plot_comparison_by_region(df, category):
    colors = ['green','blue','blue','blue','red']
    plot_barh(df[category].sort_values(ascending=False), 
              category + ' by Region', 
              category, 
              'Region', 
              colors,
              100)