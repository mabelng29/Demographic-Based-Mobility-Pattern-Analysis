import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
def task3_2():
    df = pd.read_csv("journey_to_work_cleaned.csv", index_col=0)

    # Use lambda function with map() to assign each "journey_distance" to various categories
    # Create new column "journey_distance_group" to store these groups; 
    df['journey_distance_group'] = df['journey_distance'].map(lambda x: 
    "0-10" if 1<=x<=10 else
    "10-20" if 11<=x<=20 else
    "20-40" if 21<=x<=40 else
    "40+")
    df_grouped_by_distance = df.groupby('journey_distance_group')

    # writting json file with frequency and percentage of wasted time per distance group
    json_data = {}
    key_distance = ["0-10", "10-20", "20-40", "40+"]
    key_wasted_time = ["0", "1-5 (including 5)", "5-10 (including 10)", "10-30 (including 30)", "30+"]
    for distance in key_distance:
        json_data[distance] = {"frequency": {}, "percentage": {}}

        distance_subset = df[df['journey_distance_group'] == distance]
        # Calculate total number of journeys in this distance group (for percentage calculations)
        total_journeys = len(distance_subset)
        # Loop through each wasted time group to compute frequency and percentage
        for wt in key_wasted_time:
            freq = len(distance_subset[distance_subset['wasted_time_group'] == wt])
            json_data[distance]["frequency"][wt] = freq
            json_data[distance]["percentage"][wt] = round((freq/total_journeys) * 100, 2) 
    
    with open("task3_2.json", "w") as f:
        json.dump(json_data, f, indent=4)
    

    # Declaration

    #I acknowledge the use of DouBao [https://www.doubao.com/] in the graph plotting codes section
    #I entered the following prompt: “how to draw grouped histogram that helps me to visualize the relationship between different wasted time in each distance categories.” 
    #I used the output as a starting point for generating ideas of how the code structure of grouped bars looks like and learn some possible techniques that could makes graph looks cleaner.


    
    plot_data = []
    # transfer JSON data into dataframe
    # Extract percentage values from JSON and append to list as dictionaries
    for distance in key_distance:
        for wt in key_wasted_time:
            plot_data.append({
                "distance_group": distance,
                "wasted_time_group": wt,
                "percentage": json_data[distance]["percentage"][wt]
            })
    # Convert list of dictionaries to DataFrame (columns: distance_group, wasted_time_group, percentage)
    df_plot = pd.DataFrame(plot_data)
    
    #Create grouped bar chart
    bar_width = 0.15
    x = np.arange(len(key_distance))  # Positions for distance groups on x-axis (0, 1, 2, 3 for "0-10" to "40+")
    fig, ax = plt.subplots(figsize=(12, 6))

    # Loop through each wasted time group to plot bars
    for i, wt_group in enumerate(key_wasted_time):
        subset = df_plot[df_plot["wasted_time_group"] == wt_group]
        # Plot bars: x + i*bar_width shifts each group horizontally (avoid bars overlap)
        bars = ax.bar(
            x + i * bar_width,
            subset["percentage"], # Height = percentage value
            width=bar_width,
            label=wt_group,   # Label for legend (wasted time group)
            alpha=0.8,
            edgecolor="black" 
        )

        # Add percentage labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + 1,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=8)
    
    ax.set_title("Percentage of Wasted Time Groups by Journey Distance", fontsize=14, pad=20)
    ax.set_xlabel("Journey Distance Group", fontsize=12)
    ax.set_ylabel("Percentage (%)", fontsize=12)
    ax.set_ylim(0, 100)  
    # Center x-ticks under each group of bars
    ax.set_xticks(x + bar_width * (len(key_wasted_time) - 1) / 2)
    ax.set_xticklabels(key_distance, fontsize=10)

    ax.legend(title="Wasted Time Group", bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=10)

    plt.savefig("task3_2.png", dpi=300, bbox_inches="tight")
    plt.close()


    return
