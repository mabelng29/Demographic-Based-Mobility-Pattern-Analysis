#I acknowledge the use of ChatGPT [https://chat.openai.com/] to help me with the coding part of the assignment.
#I entered the following prompt: “How do I combine two datafram into one dataframe without duplicates”
#                                "How do I create a barchart using matplotlib.pyplot"
#I used the output at the initial stage of the assessment task to help plan my essay.

import pandas as pd
import matplotlib.pyplot as plt

#Categorize number of WFH days per person into 4 categories
def categorize(days):
    if days == 0:
        return "Never"
    elif 1 <= days <= 2:
        return "Occasional"
    elif 3 <= days <= 5:
        return "Frequent"
    elif 6 <= days <= 7:
        return "Always"
    else:
        return None

def task2_2():

    person_df = pd.read_csv("/course/person.csv")

    wfh_columns = ["wfhmon", "wfhtue", "wfhwed", "wfhthu", "wfhfri", "wfhsat", "wfhsun"]

    #creates another new column "total_wfh" in original df
    # .sum(axis = 1), sums cross columns if(df[wfh_columns] == yes)
    person_df["total_wfh"] = (person_df[wfh_columns] == "Yes").sum(axis = 1)

    # Categorize wfh frequency for each person into "Never", "Occasional", "Frequent" and "Always"
    person_df["wfh_category"] = person_df["total_wfh"].apply(categorize)

    # Drop "Not in Work Force" employment types
    person_df = person_df[person_df["emptype"] != "Not in Work Force"]

    
    trips_df = pd.read_csv("/course/trips.csv")

    #Groups the DataFram (trips_df) by the column "persid", all rows belonging to the same person are put together
    #.size() counts how many rows are in each group
    #returns a series with "persid" as index and count as values
    #.reset_index(name = "total_trips") resets the index so "persid" becomes a normal column again ( not just the index), names counts column as "total_trips"
    trip_counts = trips_df.groupby("persid").size().reset_index(name = "total_trips")

    #Merging trip_counts into person_df and fill 0 for people with no trips
    #keep all rows from person_df (the left table) and add their "total_trips"
    person_trips_df = person_df.merge(trip_counts, on = "persid", how = "left")
    person_trips_df["total_trips"] = person_trips_df["total_trips"].fillna(0)

    #creates a DataFrame with average trip for each combinations
    #.mean() takes the mean of the "total_trips" column, get the average number of trips per person for each combinations
    #.reset_index() converts the grouped result back into a regular DataFrame, the grouping columns become normal columns again
    average_trip_df = person_trips_df.groupby(["sex", "emptype", "wfh_category"])["total_trips"].mean().reset_index()
    #rename collumn "total_trips" into "average_trips", inplace=True means makes changes in average_trip_df directly
    average_trip_df.rename(columns = {"total_trips": "average_trips"}, inplace = True)

    #creates a DataFrame average_trips filled in each category seperated by "sex" and "emptype"
    wfh_trips_df = average_trip_df.pivot_table(
        index=  ["sex", "emptype"],
        columns = "wfh_category",
        values = "average_trips",
        fill_value = 0
    )

    #Reorders the columns of wfh_trips_df to match category_order
    category_order = ["Never", "Occasional", "Frequent", "Always"]
    wfh_trips_df = wfh_trips_df[category_order]

    #Plot bar chart
    barchart = wfh_trips_df.plot(
        kind = "bar",
        figsize = (10, 6),
        colormap = "tab20"
    )
    #Set labels and title
    barchart.set_ylabel("Average Trips")
    barchart.set_xlabel("Gender, Employment Type")
    barchart.set_title("Average Trips per Person by WFH Frequency, Gender and Employment Type")
    barchart.legend(title = "WFH Category", bbox_to_anchor = (1.05, 1), loc = "upper left")

    #Adjust layout, save figure to "task2_2.png" file and close
    plt.tight_layout()
    plt.savefig("task2_2.png")
    plt.close()




    
