import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from Data_Preprocessing import process_data  # your preprocessing function

# Load preprocessed data
df = process_data()

def plot_dataset_summary(df):
    sns.set(style="whitegrid")
    
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Household income as categorical range (robust for open-ended values)
    def get_lower_bound(val):
        if pd.isna(val) or not isinstance(val, str):
            return float('inf')  # push NaNs to the end
        val = val.strip()
        if '-' in val:
            return int(val.split('-')[0])
        else:
            # extract the first number in strings like "416000 or more"
            num = re.findall(r'\d+', val)
            return int(num[0]) if num else float('inf')

    income_ranges = [x for x in df['hhinc_group'].unique() if isinstance(x, str) and x.strip() != ""]
    income_ranges_sorted = sorted(income_ranges, key=get_lower_bound)

    sns.countplot(
        x='hhinc_group',
        data=df,
        ax=axs[0,0],
        color='skyblue',
        order=income_ranges_sorted
    )
    axs[0,0].set_title('Household Income Distribution', fontsize=14)
    axs[0,0].set_xlabel('Income Range ($)', fontsize=12)
    axs[0,0].set_ylabel('Count', fontsize=12)
    axs[0,0].tick_params(axis='x', rotation=45)

    # 2. Household size distribution
    sns.countplot(
        x='hhsize',
        data=df,
        ax=axs[0,1],
        palette='Set2',
        order=["Small", "Medium", "Large"]
    )
    axs[0,1].set_title('Household Size Categories', fontsize=14)
    axs[0,1].set_xlabel('Household Size', fontsize=12)
    axs[0,1].set_ylabel('Count', fontsize=12)

    # 3. Age group distribution
    sns.countplot(
        x='agegroup',
        data=df,
        ax=axs[1,0],
        palette='Set3',
        order=sorted(df['agegroup'].dropna().unique())
    )
    axs[1,0].set_title('Age Group Distribution', fontsize=14)
    axs[1,0].set_xlabel('Age Group (Decades)', fontsize=12)
    axs[1,0].set_ylabel('Count', fontsize=12)

    # 4. Main journey mode distribution
    sns.countplot(
        x='main_journey_mode',
        data=df,
        ax=axs[1,1],
        palette='Set1',
        order=df['main_journey_mode'].value_counts().index
    )
    axs[1,1].set_title('Main Journey Mode', fontsize=14)
    axs[1,1].set_xlabel('Mode of Transport', fontsize=12)
    axs[1,1].set_ylabel('Count', fontsize=12)

    plt.tight_layout()
    plt.savefig("dataset_summary.png", dpi=300)  # high-res for slides
    plt.show()  # optional: display the figure

# Call the function
plot_dataset_summary(df)

