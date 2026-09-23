# I acknowledge the use of ChatGPT [https://chat.openai.com/] to help do the coding for the assignment.
# I entered the following prompts: “How to count the frequency of each value for a column and show values on each bar” 
# I used the output as a starting point for writing the code to plot the distribution of the data. 


import matplotlib.pyplot as plt
import pandas as pd

# Load raw data
journey_to_work = pd.read_csv("journey_to_work_vista_2023_2024.csv")

# Count frequency of each category
counts = journey_to_work['main_journey_mode'].value_counts()

# Plot as vertical bar chart
plt.figure(figsize=(12, 8))  # wide figure for readability
ax = counts.plot(kind='bar', color='skyblue', edgecolor='black')

# Add labels and title
plt.xlabel("Main Journey Mode", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.title("Distribution of Main Journey Modes", fontsize=14, weight='bold')

# Rotate x-axis labels to prevent overlap
plt.xticks(rotation=90, ha='center')

# Show values above each bar
for i, val in enumerate(counts.values):
    ax.text(i, val + max(counts.values)*0.01, f"{val:,}", 
            ha='center', va='bottom', fontsize=10)

plt.tight_layout()

plt.savefig('raw_travel_mode_distribution.png', dpi=300)


