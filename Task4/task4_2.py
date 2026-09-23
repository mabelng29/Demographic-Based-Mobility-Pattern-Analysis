# I acknowledge the use of ChatGPT [https://chat.openai.com/] to help do the coding for the assignment.
# I entered the following prompts: “How to categorise data in a dataframe. How to draw 2 grouped bar charts in Python” 
# I used the output as a starting point for writing the code to categorise data and visualise data.


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Categorise the journey's start time into groups
def categorise_journey_starttime(df): 
    
    bins = [0, 4, 5, 7, 9, 24]
    labels = ["Before 4am", "4-5am", "5-7am", "7-9am", "After 9am"]
    
    # Convert minute to hour
    # // integer devision gives the hour part 
    # Each value in bins is an integer hour, keeping the hour part fits neatly into these bins
    df["start_time_hour"] = df["start_time"] // 60
    
    # Categorise the journeys' start time into groups
    # pd.cut() is used to sort data values into discrete intervals (convert continuous numerical data into categorical data)
    # weekday_df["start_time_hour"] is the data to be binned
    # bins is the bin edges for segmentation
    # labels give names for these bins
    # right = True bins include the right endpoint (eg. 4 will fall into 0-4 bin, not 4-5)
    df["start_time_cat"] = pd.cut(df["start_time_hour"], 
        bins = bins, 
        labels = labels, 
        right = True
        )
    return df


# Plot the distribution of journey start time categories for each day type
def plot_starttime_distribution(jtw, jte, filename = "task4_2.png"): 
    # Creates a figure with 2 subplots arranged in 1 row, 2 columns
    # ax1 is the first plot
    # ax2 is the second plot
    # figsize makes is the overall figure 16inch wide and 6inch tall
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16, 6))
    # Adds a super-title across the entire figure, above both subplots
    fig.suptitle("Journey Start Time Distribution by Day Type")

    # Plot Journey to Work
    # Uses Seaborn's countplot on the jtw dataframe
    # x = "start_time_cat": categories of start time (before 4am, 4-5am) along the x-axis
    # hue = "dayType": bars are coloured and split by "dayType" (Weekday, Weekend)
    # ax=ax1: draw this plot on the first subplot (ax1)
    sns.countplot(data = jtw, x = "start_time_cat", hue = "dayType", ax = ax1)
    # Adds title "Journey to Work"
    ax1.set_title("Journey to Work")
    # Set x-axis label as "Start Time"
    ax1.set_xlabel("Start Time")
    # Set y-axis label as "Number of Journeys"
    ax1.set_ylabel("Number of Journeys")
    # Set legend title as "Day Type"
    ax1.legend(title="Day Type")
    # ax.containers holds the groups of bars created by Seaborn
    # ax.bar_label() adds numeric labels on top of each bar segment, showing the count value
    # label_type = "edge": places labels at the edge of each bar segment
    for container in ax1.containers:
        ax1.bar_label(container, label_type="edge", fontsize=8)
    
    # Plot Journey to Education
    sns.countplot(data = jte, x = "start_time_cat", hue = "dayType", ax = ax2)
    ax2.set_title("Journey to Education")
    ax2.set_xlabel("Start Time")
    ax2.set_ylabel("Number of Journeys")
    ax2.legend(title="Day Type")
    for container in ax2.containers:
        ax2.bar_label(container, label_type="edge", fontsize=8)
    
    # Adjusts spacing so the two subplots, axis labels, and legend don’t overlap.
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    

def task4_2():
    
    # Read CSV files into DataFrames
    jtw = pd.read_csv("/course/journey_to_work.csv")
    jte = pd.read_csv("/course/journey_to_education.csv")

    # Categorise journeys' start times
    jtw_starttime_cat = categorise_journey_starttime(jtw)
    jte_starttime_cat = categorise_journey_starttime(jte)

    # Plot the distributions of journey start times for work and education
    plot_starttime_distribution(jtw_starttime_cat, jte_starttime_cat)

    return 0
