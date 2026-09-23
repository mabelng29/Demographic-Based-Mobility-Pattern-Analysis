# I acknowledge the use of ChatGPT [https://chat.openai.com/] to help do the coding for the assignment.
# I entered the following prompts: “How to categorise data in a dataframe. How to draw a grouped bar chart in Python” 
# I used the output as a starting point for writing the code to categorise data and visualise data. 


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Categorise weekday journey travel times into groups.
def categorise_weekday_traveltime(df): 

    # Extract data for weekdays
    # Create another dataframe that only includes the rows where the "dayType" column has the value "Weekday"
    #.copy() is used to create a separate dataframe (to avoid warnings)
    weekday_df = df[df["dayType"] == "Weekday"].copy()

    # Categorise each journey's travel time into groups
    # pd.cut() is used to sort data values into discrete intervals (convert continuous numerical data into categorical data)
    # weekday_df["journey_travel_time"] is the data to be binned
    # bins is the bin edges for segmentation
    # labels give names for these bins
    # right = True bins include the right endpoint (eg. 15 will fall into 0-15 bin, not 15-30)
    # use float("inf") means everything greater than 60 goes into the last bin
    bins = [0, 15, 30, 60, float("inf")]
    labels = ["0-15", "15-30", "30-60", "60+"]
    weekday_df["journey_travel_time_cat"] = pd.cut(weekday_df["journey_travel_time"], 
        bins = bins, 
        labels = labels, 
        right = True
        )
    return weekday_df


# Plot the distribution of travel time categories by home suburb region. 
def plot_traveltime_distribution(df, filename, title):
    
    # Plot a bar chart
    # Creates a new matplotlib figure of size 8inch wide and 6inch tall (to make sure the format of the graph)
    plt.figure(figsize=(8,6))
    # Creates a grouped bar chart
    # x: Take the values from the column "homesubregion_ASGS" in the dataframe and put them along the x-axis
    # Each unique value in that column becomes a sparate label on the x-axis
    # The height of each bar correspons to the count of rows that fall into that region 
    # hue: Seaborn splits each bar into sub-bars based on the categories in "journey_travel_time_cat"
    # Each category gets a colour
    ax = sns.countplot(data = df, x = "homesubregion_ASGS", hue = "journey_travel_time_cat")
    # Add x-axis label
    plt.xlabel("Home Suburb Region")
    # Add y-axis label
    plt.ylabel("Number of Journeys")
    # Sets the chart title from the function's argument title
    plt.title(title)
    # Add a legend, with the legend title set to "Travel Time Category (minutes)"
    plt.legend(title="Travel Time Category (minutes)")
    # Add bar labels
    # ax.containers holds the groups of bars created by Seaborn
    # ax.bar_label() adds numeric labels on top of each bar segment, showing the count value
    # label_type = "edge": places labels at the edge of each bar segment
    for container in ax.containers:
        ax.bar_label(container, label_type="edge", fontsize=8)
    # Adjust layout, prevents overlapping of labels, title, and legend 
    plt.tight_layout()
    # Save the figure to the file path provied in filename
    plt.savefig(filename, dpi=300)

    
def task4_1():

    # Read CSV files into DataFrames
    jtw = pd.read_csv("/course/journey_to_work.csv")
    jte = pd.read_csv("/course/journey_to_education.csv")

    # Categorise weekday journey travel times
    jtw_traveltime_cat = categorise_weekday_traveltime(jtw)
    jte_traveltime_cat = categorise_weekday_traveltime(jte)

    # Plot the distributions of journey travel times for work and education
    plot_traveltime_distribution(jtw_traveltime_cat, "task4_1_JTW.png", 
                                  "Weekday Journey to Work Travel Time by Home Suburb Region")
    plot_traveltime_distribution(jte_traveltime_cat, "task4_1_JTE.png", 
                                  "Weekday Journey to Education Travel Time by Home Suburb Region")
                                  
    return 0






