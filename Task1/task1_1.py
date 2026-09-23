# Declaration
# I acknowledge the use of ChatGPT [https://chat.openai.com/] in preparing this assessment.
# I used the following prompt: “How should I handle missing values and recode 5-year age groups into decades using Pandas?”
# I used the output only as a reference to confirm my own approach for Task 1.1.



import pandas as pd
import re

HOUSEHOLD_PATH = "/course/household.csv"

def task1_1():
    df = pd.read_csv(HOUSEHOLD_PATH, low_memory=False)

    def parse_income(val):
        if pd.isna(val): 
            return None
        s = str(val)

        # grab all digit groups, remove commas
        nums = re.findall(r"\d+", s.replace(",", ""))
        nums = [int(n) for n in nums]

        if len(nums) >= 2:
            return (nums[0] + nums[1]) / 2  # midpoint of range
        if len(nums) == 1:
            return nums[0]
        return None


    df["hhinc_group"] = df["hhinc_group"].apply(parse_income)
    #find the mean value of hhinc_group, skipna = True: skipping all NaN value
    mean_val = df["hhinc_group"].mean(skipna=True)
    #fill NaN with mean
    df["hhinc_group"] = df["hhinc_group"].fillna(mean_val)

    age_cols = [c for c in df.columns if "age" in c.lower() and "5" in c]
    if age_cols:
        age5 = age_cols[0]

        def recode_age(label):
            if pd.isna(label):
                return label
            s = str(label)
            nums = re.findall(r"\d+", s)
            if nums:
                start = int(nums[0])
                decade = (start // 10) * 10
                #range for a decade, e.g. 10->20
                return f"{decade}->{decade+10}"
            return label

        df["agegroup_10"] = df[age5].apply(recode_age)

    #save df to the csv file of name "task1.csv" without writing the row indices
    df.to_csv("task1.csv", index=False)

if __name__ == "__main__":
    task1_1()

