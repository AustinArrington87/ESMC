import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_groupwise_scaled_bars(data, title):
    # Contrasting colors for the regions
    region_colors = ['#E63946', '#A8DADC', '#457B9D', '#F4A261', '#2A9D8F', '#E9C46A', '#D83367', '#1D3557', '#F4E1D2', '#F1FAEE']
    
    # Number of emission types (columns) and regions
    num_emission_types = len(data.columns)
    num_regions = len(data)
    
    barWidth = 1 / (num_regions + 2)
    positions = [[i + j*barWidth for i in range(num_emission_types)] for j in range(num_regions)]

    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Create twin axes for each emission type
    axes = [ax]
    for i in range(num_emission_types - 1):
        axes.append(ax.twinx())

    # Plot bars, set y-axis labels, and add tick labels
    for idx, col in enumerate(data.columns):
        # Determine maximum absolute value for the current group
        max_group_value = data[col].abs().max() * 1.1
        
        # Set y-axis scale for the current group
        axes[idx].set_ylim(-max_group_value, max_group_value)
        
        # Hide y-axis labels and ticks
        axes[idx].set_yticklabels([])
        axes[idx].yaxis.set_ticks_position('none')
        
        # Plot bars for each region and add offset tick labels
        for region_idx, region in enumerate(data.index):
            bar = axes[idx].bar(positions[region_idx][idx], data.at[region, col], width=barWidth, color=region_colors[region_idx], label=region if idx == 0 else "")
            
            # Add offset tick labels to bars
            height = bar[0].get_height()
            offset = max_group_value * 0.02  # Offset value for labels
            position = height + offset if height > 0 else height - offset
            axes[idx].text(bar[0].get_x() + bar[0].get_width()/2, position, f"{height:.2f}", ha='center', va='bottom' if height > 0 else 'top', fontsize=8, color='black')

    # Set x-axis labels and title
    ax.set_xticks([r + barWidth for r in range(num_emission_types)], minor=False)
    ax.set_xticklabels(data.columns, fontdict=None, minor=False)
    plt.title(title)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    ax.legend(loc="upper left")

    plt.tight_layout()
    plt.show()

def plot_groupwise_scaled_bars_custom_x(data, title, x_axis_1, x_axis_2):
    # Contrasting colors for the regions
    region_colors = ['#E63946', '#A8DADC', '#457B9D', '#F4A261', '#2A9D8F', '#E9C46A', '#D83367', '#1D3557', '#F4E1D2', '#F1FAEE']
    
    # Number of emission types (columns) and regions
    num_emission_types = len(data.columns)
    num_regions = len(data)
    
    barWidth = 1 / (num_regions + 2)
    positions = [[i + j*barWidth for i in range(num_emission_types)] for j in range(num_regions)]

    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Create twin axes for each emission type
    axes = [ax]
    for i in range(num_emission_types - 1):
        axes.append(ax.twinx())

    # Plot bars, set y-axis labels, and add tick labels
    for idx, col in enumerate(data.columns):
        # Determine maximum absolute value for the current group
        max_group_value = data[col].abs().max() * 1.1
        
        # Set y-axis scale for the current group
        axes[idx].set_ylim(-max_group_value, max_group_value)
        
        # Hide y-axis labels and ticks
        axes[idx].set_yticklabels([])
        axes[idx].yaxis.set_ticks_position('none')
        
        # Plot bars for each region and add offset tick labels
        for region_idx, region in enumerate(data.index):
            bar = axes[idx].bar(positions[region_idx][idx], data.at[region, col], width=barWidth, color=region_colors[region_idx], label=region if idx == 0 else "")
            
            # Add offset tick labels to bars
            height = bar[0].get_height()
            offset = max_group_value * 0.02  # Offset value for labels
            position = height + offset if height > 0 else height - offset
            axes[idx].text(bar[0].get_x() + bar[0].get_width()/2, position, f"{height:.2f}", ha='center', va='bottom' if height > 0 else 'top', fontsize=8, color='black')

    # Set x-axis labels and title
    ax.set_xticks([r + barWidth for r in range(num_emission_types)], minor=False)
    ax.set_xticklabels([x_axis_1, x_axis_2], fontdict=None, minor=False)
    plt.title(title)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    ax.legend(loc="upper left")

    plt.tight_layout()
    plt.show()



def plot_impacts(data, title):
            # Plotting the corrected grouped bar chart with properly aligned offset tick labels for "Individual Impact" dataset
        # Expanding the color palette to ensure unique colors for each bar
    expanded_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', 
                    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', 
                    '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5']

    # Plotting the grouped bar chart with unique colors for each bar
    fig, ax = plt.subplots(figsize=(20, 10))

    # Limiting the colors to the number of practices available
    bar_colors = expanded_colors[:len(data['Parsed Practice'].unique()) * 2]  # Two colors for each practice (removals and reductions)
    bars = data.groupby(['Region', 'Parsed Practice']).sum()[['GHG Emission Removals (tCO2e)', 'GHG Emission Reductions (tCO2e)']]

    bars.unstack().plot(kind='bar', ax=ax, width=0.8, color=bar_colors)

    # Adding properly aligned offset tick labels to each sub-bar
    for container in ax.containers:
        for bar in container:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3 * np.sign(height)),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, color='black')

    # Setting title, labels, and legend position
    plt.title(title)
    plt.xlabel('Region')
    plt.ylabel('Impact Value')
    plt.xticks(rotation=45, ha="right", rotation_mode="anchor")
    plt.tight_layout()
    plt.legend(title='Practice Change', loc='upper left')
    plt.show()


def plot_practice_impacts(data, title):
    # Light shades of green and blue
    light_colors = ['#a8e6cf', '#a2d5f2']

    # Plotting the grouped bar chart for "Practice Impact" dataset with light green and blue colors
    fig, ax = plt.subplots(figsize=(15, 8))

    data.set_index('Parsed Practice')[['GHG Emission Removals (tCO2e)', 'GHG Emission Reductions (tCO2e)']].plot(kind='bar', ax=ax, color=light_colors, width=0.8)

    # Adding properly aligned offset tick labels to each sub-bar
    for container in ax.containers:
        for bar in container:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3 * np.sign(height)),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, color='black')

    # Setting title, labels, and legend position
    plt.title(title)
    plt.xlabel('Practice Change')
    plt.ylabel('Impact Value')
    plt.xticks(rotation=45, ha="right", rotation_mode="anchor")
    plt.tight_layout()
    plt.legend(title='Type of Emission', loc='upper left')
    plt.show()

def plot_yearly_practice_impacts(data, title):
        # Expanding the color palette for the unique bars
    unique_colors = ['#a8e6cf', '#a2d5f2', '#ff9999', '#ffd1a8', '#c2c2f0', '#ffb3e6', '#99ff99', '#ffcc99', '#c2c2f0']

    # Plotting the grouped bar chart for "Yearly Practice Impact" dataset with unique colors for each practice change
    fig, ax = plt.subplots(figsize=(20, 10))
    yearly_bars = data.groupby(['year_string', 'Parsed Practice']).sum()[['GHG Emission Removals (tCO2e)', 'GHG Emission Reductions (tCO2e)']]

    # Using only the required number of unique colors for the practices available in the dataset
    practice_unique_colors = unique_colors[:len(data['Parsed Practice'].unique())]

    yearly_bars.unstack(level=0).plot(kind='bar', ax=ax, width=0.8, color=practice_unique_colors)

    # Adding properly aligned offset tick labels to each sub-bar
    for container in ax.containers:
        for bar in container:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3 * np.sign(height)),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, color='black')

    # Setting title, labels, and legend position
    plt.title('Yearly Practice Impact by Year and Practice Change')
    plt.xlabel('Practice Change')
    plt.ylabel('Impact Value')
    plt.xticks(rotation=45, ha="right", rotation_mode="anchor")
    plt.tight_layout()
    plt.legend(title='Year', loc='upper left')
    plt.show()

def plot_individual_yearly_impacts(data, title):
    # Expanding the color palette for the unique bars within regions
    expanded_colors_for_individual = ['#a8e6cf', '#a2d5f2', '#ff9999', '#ffd1a8', '#c2c2f0', '#ffb3e6', '#99ff99', '#ffcc99', '#c2c2f0', '#ff6666']

    # Plotting the grouped bar chart for "Yearly Individual Impact" dataset with unique colors for each practice change within regions
    fig, ax = plt.subplots(figsize=(20, 10))

    # Using only the required number of unique colors for the regions available in the dataset
    region_unique_colors = expanded_colors_for_individual[:len(data['Region'].unique()) * 2]
    yearly_individual_bars = data.groupby(['Region', 'year_string']).sum()[['GHG Emission Removals (tCO2e)', 'GHG Emission Reductions (tCO2e)']]

    yearly_individual_bars.unstack(level=1).plot(kind='bar', ax=ax, width=0.8, color=region_unique_colors)

    # Adding properly aligned offset tick labels to each sub-bar
    for container in ax.containers:
        for bar in container:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3 * np.sign(height)),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, color='black')

    # Setting title, labels, and legend position
    plt.title(title)
    plt.xlabel('Region')
    plt.ylabel('Impact Value')
    plt.xticks(rotation=45, ha="right", rotation_mode="anchor")
    plt.tight_layout()
    plt.legend(title='Year', loc='upper left')
    plt.show()

#df = pd.read_excel("Model_Emission_Results.xlsx")
print("Enter filename for Emissions Data to be analyzed...")
df = pd.read_excel(input())


"""impact on GHG grouped by region and crop type"""
region_crop_emission = df.groupby(['Region'])[['GHG Emission Removals (tCO2e)', 'GHG Emission Reductions (tCO2e)', 'N2o (direct) reduction', 'N2o (indirect) reduction', 'Methane reduction', 'Emission reduction']].sum()
region_emission = region_crop_emission.copy()

"""impact on GHG grouped by region"""
region_emission['Aggregated Region'] = region_emission.index.str.split('(').str[0]
region_emission = region_emission.groupby("Aggregated Region")[['GHG Emission Removals (tCO2e)', 'GHG Emission Reductions (tCO2e)', 'N2o (direct) reduction', 'N2o (indirect) reduction', 'Methane reduction', 'Emission reduction']].sum()

"""change as a result of practice change"""
df['Parsed Practice'] = df['Practice Change'].str.strip('{}').str.split(',')
df_exploded = df.explode('Parsed Practice')
df_exploded['Parsed Practice'] = df_exploded['Parsed Practice'].str.strip(' "')

"""impact of individual practices"""
individual_impact = df_exploded.groupby(['Region', 'Parsed Practice']).agg({
    'GHG Emission Removals (tCO2e)': 'sum',
    'GHG Emission Reductions (tCO2e)': 'sum'
}).reset_index()

"""impact of combined practices"""
combined_impact = df.groupby(['Region', 'Practice Change']).agg({
    'GHG Emission Removals (tCO2e)': 'sum',
    'GHG Emission Reductions (tCO2e)': 'sum'
}).reset_index()

"""total impact grouped by parsed practice"""
practice_impact = df_exploded.groupby(['Parsed Practice']).agg({
    'GHG Emission Removals (tCO2e)': 'sum',
    'GHG Emission Reductions (tCO2e)': 'sum'
}).reset_index()
#print(practice_impact)

yearly_region_crop_emission = df.groupby(['year_string', 'Region'])[['GHG Emission Removals (tCO2e)', 'GHG Emission Reductions (tCO2e)', 'N2o (direct) reduction', 'N2o (indirect) reduction', 'Methane reduction', 'Emission reduction']].sum()


"""yearly individual impact"""
yearly_individual_impact = df_exploded.groupby(['year_string', 'Region']).agg({
    'GHG Emission Removals (tCO2e)': 'sum',
    'GHG Emission Reductions (tCO2e)': 'sum'
    #'N2o (direct) reduction': 'sum', 
    #'N2o (indirect) reduction': 'sum', 
    #'Methane reduction': 'sum', 
    #'Emission reduction':'sum',
    #'Weighted Avg Yield': 'mean',
    #'Volume of Goods (lbs)': 'mean'
}).reset_index()
#print(yearly_individual_impact)

"""yearly combined practice impact"""
yearly_combined_impact = df.groupby(['year_string', 'Practice Change']).agg({
    'GHG Emission Removals (tCO2e)': 'sum',
    'GHG Emission Reductions (tCO2e)': 'sum'
}).reset_index()

#print(yearly_combined_impact)

"""yearly practice impact"""
yearly_practice_impact = df_exploded.groupby(['year_string', 'Parsed Practice']).agg({
    'GHG Emission Removals (tCO2e)': 'sum',
    'GHG Emission Reductions (tCO2e)': 'sum'
}).reset_index()

"""impact for volume of goods based on region and crop type"""
region_crop_emission['Volume of Goods (lbs)'] = df.groupby(['Region'])[['Volume of Goods (lbs)']].sum()
region_crop_emission['Volume Per GHG Removal'] = region_crop_emission['Volume of Goods (lbs)'] / region_crop_emission['GHG Emission Removals (tCO2e)']
region_crop_emission['Volume Per GHG Reduction'] = region_crop_emission['Volume of Goods (lbs)'] / region_crop_emission['GHG Emission Reductions (tCO2e)']


"""report exel"""
with pd.ExcelWriter('report.xlsx') as writer:
    region_crop_emission.to_excel(writer, sheet_name='Region-Crop Emissions')
    region_emission.to_excel(writer, sheet_name='Region Emissions')
    individual_impact.to_excel(writer, sheet_name='Individual Impact')
    combined_impact.to_excel(writer, sheet_name='Combined Impact')
    practice_impact.to_excel(writer, sheet_name='Practice Impact')
    yearly_individual_impact.to_excel(writer, sheet_name='Yearly Individual Impact')
    yearly_combined_impact.to_excel(writer, sheet_name='Yearly Combined Impact')
    yearly_practice_impact.to_excel(writer, sheet_name='Yearly Practice Impact')


"""plotting"""
plot_groupwise_scaled_bars_custom_x(region_crop_emission[['Volume Per GHG Removal', 'Volume Per GHG Reduction']], 'Region-Crop Volume (lbs) Per Emission Type', 'Volume (lbs) GHG Removals', 'Volume (lbs) GHG Reductions')
plot_groupwise_scaled_bars(region_crop_emission[['Volume Per GHG Removal']], 'Region-Crop Emissions by Emission Type')
plot_groupwise_scaled_bars(region_emission, 'Region Emissions by Emission Type')
plot_impacts(individual_impact, 'Individual Impact by Emission Type')
plot_practice_impacts(practice_impact, 'Practice Impact by Emission Type')
plot_yearly_practice_impacts(yearly_practice_impact, 'Yearly Practice Impact by Year and Practice Change')
plot_individual_yearly_impacts(yearly_individual_impact, 'Yearly Individual Impact by Year and Region')
