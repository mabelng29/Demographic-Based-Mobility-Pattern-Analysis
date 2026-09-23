#I acknowledge the use of ChatGPT [https://chat.openai.com/] to help me with the coding part of this assignment.
#I entered the following prompts: “How do I create a new dataframe with just a few selected catogories from the original dataframe”
#                                 "How do I create a barchart using matplotlib.pyplot"
#I used the output to help me writing the code.

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


def task2_1():
    df = pd.read_csv("/course/person.csv")

    wfh_columns = ["wfhmon", "wfhtue", "wfhwed", "wfhthu", "wfhfri", "wfhsat", "wfhsun"]

    #creates another new column "total_wfh" in original df
    # .sum(axis = 1), sums cross columns if(df[wfh_columns] == yes)
    df["total_wfh"] = (df[wfh_columns] == "Yes").sum(axis = 1)

    # Categorize wfh frequency for each person into "Never", "Occasional", "Frequent" and "Always"
    df["wfh_category"] = df["total_wfh"].apply(categorize)

    # Drop "Not in Work Force" employment types
    df = df[df["emptype"] != "Not in Work Force"]

    # All possible combinations of sex and emptype and each WFH category
    sexes = df['sex'].unique()
    emptypes = df['emptype'].unique()
    categories = ["Never", "Occasional", "Frequent", "Always"]

    all_combinations = pd.MultiIndex.from_product(
        [sexes, emptypes, categories], 
        names = ["sex", "emptype", "wfh_category"]
    )

    #Groups df by three columns "sex", "emptype" and "wfh_category" and counts number of rows in each group
    #return a Series with multiple index 
    counts = df.groupby(["sex", "emptype", "wfh_category"]).size()
    #Includes zero-count for combinations not in the data
    counts = counts.reindex(all_combinations, fill_value = 0)


    # group "sex" and "emptype" and sum the number of same type of "sex" and "emptype"
    proportions = counts / counts.groupby(level=[0,1]).transform('sum')
    # Convert Series to DataFrame
    proportions_df = proportions.to_frame(name='proportion').reset_index()


    # Creates a new DataFrame for proportion of each categories seperated with "sex" and "emptype"
    wfh_patterns_df = proportions_df.pivot_table(
        index = ["sex", "emptype"],
        columns = "wfh_category",
        values = "proportion",
        fill_value = 0
    )
    
    #Reorders the columns of wfh_patterns_df to match category_order
    category_order = ["Never", "Occasional", "Frequent", "Always"]
    wfh_patterns_df = wfh_patterns_df[category_order]

    # Plot stacked bar chart
    barchart = wfh_patterns_df.plot(
        kind = "bar",
        figsize = (10, 6),
        colormap = "tab20"
    )

    #Set labels and title
    barchart.set_ylabel("Proportion")
    barchart.set_xlabel("Gender, Employment Type")
    barchart.set_title("Proportion of WFH Frequency by Gender and Employment Type")
    #create legend for the barchart, bbox_to_anchor is for the location(coordinates) of the legend box
    barchart.legend(title = "WFH Category", bbox_to_anchor = (1.05, 1), loc = "upper left")

    #Adjust layout, save figure to "task2_1.png" file and close
    plt.tight_layout()
    plt.savefig("task2_1.png")
    plt.close()
    
