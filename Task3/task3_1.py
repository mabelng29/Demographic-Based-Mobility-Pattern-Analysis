import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def task3_1():
    # Step 1: Load raw journey data from CSV, set column 0 as the index (get rid of the intial index column)
    df = pd.read_csv("/course/journey_to_work.csv", index_col=0)
    
    # Group the main modes of travel

    # First, define lists of specific modes that fall into each broad category (Public/Private/Active) 
    public_modes = ["Public Bus", "School Bus", "Train", "Tram"]
    private_modes = ["Vehicle Driver", "Vehicle Passenger", "Taxi", "Taxi / Rideshare"]
    active_modes = ["Bicycle", "Walking", "Motorcycle", "e-Scooter", "Scooter"]


    # Use lambda function with map() to assign each "main_journey_mode" to active/private/public categories
    # Create new column "transport_modes" to store these groups; 
    # label uncategorized modes as "Other" to handle the edge cases
    df['transport_modes'] = df['main_journey_mode'].map(lambda x: 
    "Public" if x in public_modes else
    "Private" if x in private_modes else
    "Active" if x in active_modes else
    "Other")
    df = df[df['transport_modes'] != "Other"].copy()
    df_grouped_by_modes = df.groupby('transport_modes')

    # Calculate the wasted_time and num_of_stops
    df['wasted_time'] = df['journey_elapsed_time'] - df['journey_travel_time']
    df['wasted_time_group'] = df['wasted_time'].map(lambda x: 
    "0" if x==0 else
    "1-5 (including 5)" if 1 <= x <= 5 else
    "5-10 (including 10)" if 6 <= x <= 10 else
    "10-30 (including 30)" if 11 <= x <= 30 else
    "30+")

    # if deleted, the labels later shown in x-axis of graph is unordered (e.g., "30+" might sort before "10-30")
    # Define a list of "category_order" to set logical sequence (from 0 to 30+ min)
    category_order = ["0", "1-5 (including 5)", "5-10 (including 10)", "10-30 (including 30)", "30+"]
    df['wasted_time_group'] = pd.Categorical(
        df['wasted_time_group'],
        categories=category_order,
        ordered=True
    )

    df_grouped_by_wasted_time = df.groupby('wasted_time_group')
    
    # identify the num_of_stops related data in the excel : the main modes used in each of the destination
    # iterate the data and count the number of stops
    stops_col_name = df.columns[11:26]
    # .notnull() marks valid stops as True; adds up these boolean values across columns for each row (row-wise),
    # giving the total number of stops per journey.
    df['num_of_stops'] = df[stops_col_name].notnull().sum(axis=1)
    df['num_of_stops_group'] = df['num_of_stops'].map(lambda x: 
    "0" if x==1 else
    "1" if x==2 else
    "2" if x==3 else
    "3+")
    df_grouped_by_num_of_stops = df.groupby('num_of_stops_group')


    #(b)
    journey_to_work_cleaned = df.to_csv("journey_to_work_cleaned.csv", index=True)

    # Declaration
    #I acknowledge the use of DouBao [https://www.doubao.com/] in the graph plotting codes section
    #I entered the following prompt: “how to draw grouped histogram that helps me to visualize the relationship between different wasted time in different travel modes.” 
    #I used the output as a starting point for generating ideas of how the code structure of grouped bars looks like, how to add global legends and learn some possible techniques that could makes graph looks cleaner.


    # Group data by 3 key variables (transport_modes, wasted_time_group, num_of_stops_group)
    # .size() counts the number of journeys in each group; reset_index() converts groupby result (how many counts in journey groups) to DataFrame
    # Name the count column to be "journey_count"
    plot_data = df.groupby(['transport_modes', 'wasted_time_group', 'num_of_stops_group']).size().reset_index(name='journey_count')

    # Calculate total journeys per transport mode("active/private/public") (to compute proportions later)
    # if get rid of reset_index() mode totals would return Series with transport modes as index which would throw errors when merged
    mode_totals = plot_data.groupby('transport_modes')['journey_count'].sum().reset_index()
    plot_data = plot_data.merge(mode_totals, on='transport_modes', suffixes=('', '_total'))
    plot_data['proportion'] = plot_data['journey_count'] / plot_data['journey_count_total']


    # Initialize figure with 1 row, 3 columns (1 chart per transport mode)
    # figsize=(30, 9): Wide enough for 3 charts, tall enough to avoid label overlap
    fig, axes = plt.subplots(1, 3, figsize=(30, 9))

    # Define order of transport modes (matches axes[0]=Active, axes[1]=Private, axes[2]=Public)
    travel_modes = ['Active', 'Private', 'Public']

    # get 4 distinct colors from seaborn's "Set2" palette (1 color per stop group: 0,1,2,3+)
    colors = sns.color_palette("Set2", n_colors=4)  # 4 colors for 4 stop groups

    # Loop through each transport mode to build its chart
    for i, mode in enumerate(travel_modes):
        mode_data = plot_data[plot_data['transport_modes'] == mode]
        
        # Pivot data for grouped bars:
        # Rows = wasted_time_group (x-axis)
        # Columns = num_of_stops_group (different colored bars per stop group)
        # Values = proportion (y-axis)
        # Pivot and FORCE inclusion of all stop groups (0,1,2,3+)
        pivot_data = mode_data.pivot(
            index='wasted_time_group', 
            columns='num_of_stops_group', 
            values='proportion'
        ).reindex(columns=["0", "1", "2", "3+"]) # forces all stop groups to appear (even if 0 proportion)
        


        # ax=axes[i]: Assign chart to the i-th subplot 
        # width=0.8: Wide bars for readability; edgecolor='black': Defines bar borders (avoids color blending)
        # legend=False: Disable per-chart legend (we’ll add a global legend later)
        pivot_data.plot(kind='bar', ax=axes[i], color=colors, width=0.8, edgecolor='black', legend=False)
  
        
        # clearly identifies the transport mode
        # title: Clearly identifies the transport mode (fontsize=14: stands out but not overwhelming)
        axes[i].set_title(f'{mode} Travel Mode', fontsize=14)
        axes[i].set_xlabel('Wasted Time Group', fontsize=12)
        if i == 0:
            axes[i].set_ylabel('Proportion of Journeys', fontsize=12)
        axes[i].tick_params(axis='x', rotation=45)


        # Set custom y-axis limits per mode:
        # - Tailors y-range to the mode’s proportion range (avoids empty space, improves readability)
        if mode == "Active":
            axes[i].set_ylim(0, 1.0)
        elif mode == "Private":
            axes[i].set_ylim(0, 0.8)
        elif mode == "Public":
            axes[i].set_ylim(0, 0.4)

        # Add percentage labels (only non-zero)
        # ha='center', va='center': Aligns label perfectly with bar
        for p in axes[i].patches:
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            if height > 0:
                axes[i].text(x + width/2, y + height + 0.02, f'{height:.1%}', ha='center', va='center', fontsize=9)

    # Add global legend (includes all stop groups)
    # Extract legend handles (colors) and labels (stop groups) from the first subplot (all charts use the same colors)

    # title='Number of Stops': Explains what the legend represents
    # bbox_to_anchor=(0.5, 1.05): Positions legend slightly above the figure (avoids overlap with charts)
    # ncol=4: Arranges legend items in 1 row (4 columns) for compactness
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles, labels,
        title='Number of Stops',
        title_fontsize=12,
        fontsize=10,
        loc='upper center',
        bbox_to_anchor=(0.5, 1.05),
        ncol=4
    )

    plt.savefig('task3_1.png', dpi=300, bbox_inches='tight')
    plt.close()


    return
