#I acknowledge the use of ChatGPT [https://chat.openai.com/] to help me with the coding part of this assignment.
#I entered the following prompts: “How do I compute normalized mutual information manually”
#                                 "How do I create a visualisation presenting the correlation"
#I used the output to help me writing the code.

import pandas as pd 
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from Data_Preprocessing import process_data
from sklearn.preprocessing import LabelEncoder

#Load preprocessed data
df = process_data()

#Step 1: Define functions to compute Normalized Mutual Information (NMI)

#Compute the probability distribution of values in a column
def compute_probability(col):
    return col.value_counts() / col.shape[0]

#Compute entropy H(X) = -Σ p(x) log2(p(x)) for a single variable.
def compute_entropy(col):
    probabilities = compute_probability(col)
    entropy = -sum(probabilities * np.log2(probabilities))
    return entropy

#Compute conditional entropy H(Y|X) using group-wise entropy of Y given X.
def compute_conditional_entropy(x, y):
    probability_x = compute_probability(x)
    temp_df = pd.DataFrame({'X': x, 'Y': y})

    #Compute entropy of Y for each value of X
    entropy_by_group = temp_df.groupby('X', observed=True)['Y'].aggregate(compute_entropy)

    #Weighted sum of entropies
    conditional_entropy = sum(probability_x * entropy_by_group)
    return conditional_entropy

def NMI(x, y):
    # Entropies of X and Y, H(X) and H(Y)
    entropy_x = compute_entropy(x)
    entropy_y = compute_entropy(y)
    
    # Conditional entropy H(Y|X)
    conditional_entropy = compute_conditional_entropy(x, y)
    
    # MI(X, Y)
    MI = entropy_y - conditional_entropy 
    
    #Normalization to scale MI between 0 and 1
    return MI / min(entropy_x, entropy_y)


#Step 2: Compute NMI for selected features against travel mode

features = ['agegroup', 'hhinc_group', 'hhsize']
target = 'main_journey_mode'

mi_result = {}
for col in features:
    mi = NMI(df[col], df[target])
    mi_result[col] = mi

# Step 3: Visualization of Travel Mode Distribution by features

# Define custom category orders for consistent visualisation
age_order = ['10-19','20-29','30-39','40-49','50-59','60-69','70-79','80-89','90-99']
income_order = [
    '1-7799', 
    '7800-15599', 
    '15600-20799', 
    '20800-25999', 
    '26000-31199', 
    '31200-41599', 
    '41600-51999', 
    '52000-64999', 
    '65000-77999', 
    '78000-90999', 
    '91000-103999', 
    '104000-129999', 
    '130000-155999', 
    '156000-181999', 
    '182000-207999', 
    '208000-233999', 
    '234000-259999', 
    '260000-311999', 
    '312000-415999', 
    '416000 or more'
]
hhsize_order = ['Small','Medium','Large']

order_modes = ['Active', 'Private', 'Public', 'Other']

#Create both count plots and heatmaps for each feature
#Choose appropriate sorting order for x-axis
for col in features:
    if col == 'agegroup':
        sorted_categories = age_order
    elif col == 'hhinc_group':
        sorted_categories = income_order
    elif col == 'hhsize':
        sorted_categories = hhsize_order
    else:
        sorted_categories = sorted(df[col].unique())  # fallback
    
    # Count plot
    plt.figure(figsize=(8, 5))
    sns.countplot(
        data=df,
        x=col,
        hue=target,
        hue_order=order_modes,
        order=sorted_categories
    )
    
    plt.title(f'Travel Mode Distribution by {col}')
    plt.xlabel(col)
    plt.ylabel('Number of People')
    plt.legend(title='Travel Mode')
    plt.xticks(rotation=90) 
    plt.tight_layout()
    plt.savefig(f'countplot_{col}.png')
    plt.close()

    # Heatmap
    ct = pd.crosstab(df[col], df[target])
    ct = ct.reindex(index=sorted_categories, columns=order_modes)
    plt.figure(figsize=(8, 5))
    sns.heatmap(ct.fillna(0), annot=True, fmt='.0f', cmap='YlGnBu')
    plt.title(f'Travel Mode Counts by {col}')
    plt.xlabel('Travel Mode')
    plt.ylabel(col)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"heatmap_{col}.png")
    plt.close()

#Step 4: Visualize NMI values for feature comparison

# Recompute NMI results as distionary
mi_result = {col: NMI(df[col], df[target]) for col in features}

# Convert to DataFrame for plotting
mi_df = pd.DataFrame(list(mi_result.items()), columns=['Feature', 'NMI'])

# Bar plot for NMI
plt.figure(figsize=(6,4))
sns.barplot(data=mi_df, x='Feature', y='NMI', palette='Blues_d')
plt.title('Normalized Mutual Information (NMI) with Travel Mode')
plt.ylabel('NMI')
plt.xlabel('Feature')
plt.tight_layout()
plt.savefig('NMI_barplot.png')
plt.show()

