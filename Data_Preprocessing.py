# I acknowledge the use of ChatGPT [https://chat.openai.com/] to help do the coding for the assignment.
# I entered the following prompts: “How to extract the values in bracket and remove $sign. How to drop a row. How to check for duplicate rows” 
# I used the output as a starting point for writing the code to categorise data and remove duplicated rows. 

import pandas as pd
import numpy as np
import re
import math

# -----------------------------
# Helper functions
# -----------------------------

# Convert 5-year age ranges into 10-year ranges
def agegroup_to_decade(age_str):
    if pd.isna(age_str):
        return None
    nums = [int(s) for s in re.findall(r"\d+", age_str)]
    if not nums:
        return age_str
    lower = (nums[0] // 10) * 10
    upper = lower + 9
    return f"{lower}-{upper}"

# Categorise travel mode into Public, Private, Active, or Other
def map_mode(mode):
    if mode in ["Bus", "Train", "Tram"]:
        return "Public"
    elif mode in ["Vehicle Driver", "Vehicle Passenger", "Taxi"]:
        return "Private"
    elif mode in ["Bicycle", "Walking"]:
        return "Active"
    else:
        return "Other"

# -----------------------------
# Data processing functions
# -----------------------------

# Load CSVs and merge into a single dataframe of working people
def load_and_merge(): 
    # Read CSV files into dataframes
    household = pd.read_csv("household_vista_2023_2024.csv")
    person = pd.read_csv("person_vista_2023_2024.csv")
    journey_to_work = pd.read_csv("journey_to_work_vista_2023_2024.csv")

    # Select relevant columns
    household = household[["hhid", "hhinc_group", "hhsize"]]
    person = person[["hhid", "persid", "agegroup", "anywork"]]
    journey_to_work = journey_to_work[["hhid", "persid", "main_journey_mode"]]

    # Select working persons
    working_person = person[person["anywork"] == "Yes"].drop(columns = ["anywork"])

    # Merge
    df = pd.merge(working_person, household, on="hhid", how="inner")
    df = pd.merge(df, journey_to_work, on=["hhid", "persid"], how="inner")

    return df

# Clean household income and household size columns
def clean_household(df): 
    # Extract numeric yearly income range
    df["hhinc_group"] = (
        df["hhinc_group"]
        .str.extract(r"\((.*?)\)")[0]        
        .str.replace("[$,]", "", regex=True)
    )

    # Detect any outlier and cap household size to 10
    # Handle missing hhsize by filling with the mean of the column, round up to the nearest integer
    df["hhsize"] = pd.to_numeric(df["hhsize"], errors='coerce')
    df["hhsize"] = df["hhsize"].clip(upper=10)
    mean_hhsize = math.ceil(df["hhsize"].mean())
    df["hhsize"] = df["hhsize"].fillna(mean_hhsize)

    # Categorise household size
    df["hhsize"] = pd.cut(
        df["hhsize"],
        bins=[0, 2, 4, float("inf")],
        labels=["Small", "Medium", "Large"],
        right=True
    )

    return df

# Clean age group values into decades
def clean_person(df): 
    df["agegroup"] = df["agegroup"].apply(agegroup_to_decade)
    return df

# Categorise journey modes and handle missing values using the mode across the 4 modes
def clean_journey(df): 
    df["main_journey_mode"] = df["main_journey_mode"].apply(map_mode)
    most_freq_mode = df["main_journey_mode"].mode()[0]
    df["main_journey_mode"] = df["main_journey_mode"].fillna(most_freq_mode)
    return df

# Drop rows with missing household income or age
def handle_missing(df): 
    df = df.dropna(subset=['hhinc_group', 'agegroup']).reset_index(drop=True)
    return df

# Remove any duplicate rows, keep the first occurrence
def remove_duplicates(df): 
    df = df.drop_duplicates().reset_index(drop = True)
    return df

# -----------------------------
# Overall preprocessing
# -----------------------------

def process_data(): 
    df = load_and_merge()
    df = handle_missing(df)
    df = clean_household(df)
    df = clean_person(df)
    df = clean_journey(df)
    df = remove_duplicates(df)

    return df

if __name__ == "__main__": 
    final_df = process_data()
    print(final_df)
    final_df.to_csv("task.csv", index=False)
    


