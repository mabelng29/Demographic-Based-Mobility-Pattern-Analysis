# Declaration
# I acknowledge the use of ChatGPT [https://chat.openai.com/] in preparing this assessment.
# I used the following prompt: “How can I create a heatmap and pie charts with Pandas and Matplotlib for Task 1.2?”
# I used the output only as a reference to confirm my own approach for Task 1.2.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

HOUSEHOLD_PATH = "/course/household.csv"

#change non numeric income to numeric
def _parse_income_to_numeric(s):
    """Return a single number for hhinc_group (mean if range), NaN if none."""
    if pd.isna(s):
        return np.nan
    nums = re.findall(r"\d[\d,]*", str(s))
    nums = [int(x.replace(",", "")) for x in nums]
    if len(nums) >= 2:
        return (nums[0] + nums[1]) / 2
    if len(nums) == 1:
        return float(nums[0])
    return np.nan

#change labels to become more pretty (pretty label) for intervals
def _fmt(iv):
    """Pretty label for pandas Interval."""
    #if lower bound is finite, cast to int, set to None if not
    L = None if not np.isfinite(iv.left)  else int(iv.left)
    #if upper bound is finite, cast to int,set to None if not
    R = None if not np.isfinite(iv.right) else int(iv.right)

    #if no lower bound, the interval becomes <= $x
    if L is None: return f"≤ ${R:,}"
    #if no upper bound, the interval becomes >= $x
    if R is None: return f"≥ ${L:,}"
    #if both finite, have upper bound and lower bound interval $x - $y
    return f"${L:,}–${R:,}"

def task1_2():
    # 1) Read
    df = pd.read_csv(HOUSEHOLD_PATH, low_memory=False)

    # 2) Ensure income is numeric for binning
    if "hhinc_group" not in df.columns:
        raise ValueError("household.csv missing 'hhinc_group'")
    inc_num = df["hhinc_group"]

    #check if num in inc_num is numeric subtype (e.g. int, float)
    #if not, change to numeric
    if not np.issubdtype(inc_num.dtype, np.number):
        inc_num = df["hhinc_group"].map(_parse_income_to_numeric)

    # 3) Find the 5-year age column 
    age5_names = ("aveagegroup_5", "averagegroup_5", "agegroup_5", "age_group_5")
    age5_cols = [c for c in df.columns if c.lower() in age5_names]
    if not age5_cols:
        raise ValueError("5-year age band column not found")

    age5 = age5_cols[0]

    # Keep rows with income; make 6 quantile bins (balanced counts)
    df = df.copy() #make a copy of df so the original isn't modified
    df["__inc_num"] = inc_num
    df = df[df["__inc_num"].notna()] #drop rows where "__inc_num" is NaN

    #bin the numeric incomes into 6-quantile based groups
    #split into 6 bins of roughly equal counts
    #remove duplicates value - reduces number of bins to avoid errors
    df["__inc_bin"] = pd.qcut(df["__inc_num"], q=6, duplicates="drop")

    # 4) Heatmap: agegroup_5 × income-bin
    pivot = pd.crosstab(df[age5], df["__inc_bin"])
    xlabels = [_fmt(iv) for iv in pivot.columns]

    plt.figure(figsize=(11, 6))
    plt.imshow(pivot.values, aspect="auto")
    plt.colorbar(label="Count")
    plt.xticks(range(len(xlabels)), xlabels, rotation=40, ha="right")
    plt.yticks(range(len(pivot.index)), [str(i) for i in pivot.index])
    plt.xlabel("Household income (binned)")
    plt.ylabel("Age group (5-year)")
    plt.title("Age vs Household Income")
    plt.tight_layout()
    plt.savefig("task1_heatmap.png")
    plt.close()

    # 5) Pies: Cities (C) vs Shires (S) income distributions
    if "homelga" not in df.columns:
        raise ValueError("household.csv missing 'homelga'")
    
    #classify "homelga" to city if contains C and shire if contains S
    is_city  = df["homelga"].astype(str).str.contains(r"\(C\)", na=False)
    is_shire = df["homelga"].astype(str).str.contains(r"\(S\)", na=False)


    def pie_counts(mask):
        # Select the subset of "__inc_num" values where the mask is True
        sub = df.loc[mask, "__inc_num"]

        # If the subset is empty (no rows selected), return empty labels and values
        if sub.empty:
            return [], np.array([])

        # Bin the income values into 6 quantile-based groups
        # "duplicates='drop'" avoids errors if some quantiles are identical
        bins = pd.qcut(sub, q=6, duplicates="drop")

        # Count how many fall into each bin, and sort by interval order
        counts = bins.value_counts().sort_index()

        # Format interval labels nicely using the _fmt function
        labels = [_fmt(iv) for iv in counts.index]

        # Return the formatted labels and the counts as numpy array
        return labels, counts.values


    # Apply the function separately to "city" and "shire" subsets (Boolean masks)
    labels_c, values_c = pie_counts(is_city)
    labels_s, values_s = pie_counts(is_shire)

    # Create a figure with 1 row, 2 columns of subplots for side-by-side pies
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))


    if len(values_c):
        # Plot a pie chart on the first subplot (cities) if there is data
        wedges, _, _ = axes[0].pie(
            values_c,               # values for each slice
            autopct="%1.1f%%",      # show percentage on each slice with 1 decimal
            startangle=90,           # start pie from 12 o'clock position
            textprops={"fontsize": 8} # font size for labels on slices
        )
        axes[0].axis("equal")       # make the pie a circle (not oval)
        axes[0].set_title("Income distribution — Cities (C)")  # subplot title
        axes[0].legend(
            wedges,                 # the pie slices
            labels_c,               # corresponding income bin labels
            title="Income bins",    
            loc="center left",      # legend position
            bbox_to_anchor=(1, 0.5),# place legend outside the plot on right
            fontsize=8
        )

    if len(values_s):
        # Plot a pie chart on the second subplot (shires) if there is data
        wedges, _, _ = axes[1].pie(
            values_s,
            autopct="%1.1f%%",
            startangle=90,
            textprops={"fontsize": 8}
        )
        axes[1].axis("equal")
        axes[1].set_title("Income distribution — Shires (S)")
        axes[1].legend(
            wedges,
            labels_s,
            title="Income bins",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize=8
        )

    plt.tight_layout()            # adjust spacing so titles/legends don’t overlap
    plt.savefig("task1_pie.png") # save the figure as PNG
    plt.close()                   # close the figure to free memory

if __name__ == "__main__":
    task1_2()

