#I acknowledge the use of doubao [https://www.doubao.com/] to help me with the coding part of this assignment.
#I entered the following prompts: “How to categorically encode the values that i get from preprocessed data”
#                                 "How to load PCA and three demographic features in the way of heatmap visualization"
#I used the output to help me writing the code.
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram, linkage
from Data_Preprocessing import process_data


# ------------------------------------------------------------
# Helper: Convert household income ranges to numeric midpoints
# ------------------------------------------------------------
def convert_hhinc_group_to_numeric(df):
    def get_midpoint(income_str):
        if pd.isna(income_str):
            return None
        income_str = income_str.replace('$', '').replace(',', '')
        if " or more" in income_str:
            parts = income_str.split(" or more")
            return float(parts[0])
        parts = income_str.split('-')
        if len(parts) == 2:
            return (float(parts[0]) + float(parts[1])) / 2
        else:
            return float(parts[0])
    df["hhinc_group"] = df["hhinc_group"].apply(get_midpoint)
    return df


# =============================
# Step 1: Data Preprocessing
# =============================
final_df = process_data()

# Convert income group to numeric
final_df = convert_hhinc_group_to_numeric(final_df)

# Encode demographic categorical variables
cat_cols = ['agegroup', 'hhsize']  # exclude main_journey_mode
label_encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    final_df[col] = le.fit_transform(final_df[col])
    label_encoders[col] = le

# Travel mode kept for interpretation (not for clustering)
# final_df['main_journey_mode'] stays as original string/category

# Select demographic features only for clustering
features_for_clustering = ['agegroup', 'hhinc_group', 'hhsize']

# Normalize features
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(final_df[features_for_clustering])
final_df.to_csv("task1.csv", index=False)

# =============================
# Step 2: K-Means Clustering
# =============================
# Elbow Method to determine optimal k
distortions = []
k_range = range(1, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_data)
    distortions.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(k_range, distortions, 'bx-')
plt.title('Elbow Method Showing Optimal k')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Distortion (Inertia)')
plt.grid(True)
plt.savefig('elbow_optimal_k.png', dpi=300, bbox_inches='tight')
plt.show()

# Based on Elbow Method, choose k=3
k = 3
kmeans = KMeans(n_clusters=k, random_state=42).fit(scaled_data)
final_df['kmeans_cluster'] = kmeans.labels_


# =============================
# Step 3: Hierarchical Clustering
# =============================
hc = AgglomerativeClustering(n_clusters=k, linkage='ward')
hc.fit(scaled_data)
final_df['hc_cluster'] = hc.labels_

# Dendrogram (sample 100 points to avoid overcrowding)
sample_data = pd.DataFrame(scaled_data, columns=features_for_clustering).sample(100, random_state=26)
Z = linkage(sample_data, method='ward')

plt.figure(figsize=(10, 6))
dendrogram(Z)
plt.title('Hierarchical Clustering Dendrogram (Ward Linkage)')
plt.xlabel('Sample Index')
plt.ylabel('Linkage Distance')
plt.savefig('dendrogram.png', dpi=300, bbox_inches='tight')
plt.show()


# =============================
# Step 4: PCA Loadings Heatmap
# =============================
pca = PCA(n_components=2)  # Only 2 components
pca_result = pca.fit_transform(scaled_data)

print("Explained variance ratio per component:", pca.explained_variance_ratio_)
print("Total variance explained:", sum(pca.explained_variance_ratio_))

loadings = pd.DataFrame(
    pca.components_.T,  # now only 2 PCs
    columns=[f"PC{i+1}" for i in range(2)],
    index=features_for_clustering
)

plt.figure(figsize=(6, 4))
sns.heatmap(loadings, annot=True, cmap="coolwarm", center=0, fmt=".2f")
plt.title("PCA Loadings Heatmap (Demographic Variables)")
plt.ylabel("Features")
plt.xlabel("Principal Components")
plt.savefig('PCA_axes_heatmap_2D.png', dpi=300, bbox_inches='tight')
plt.show()


# =============================
# Step 5: Cluster Interpretation
# =============================
# Summarise demographics and mode distribution by cluster
cluster_summary = final_df.groupby('kmeans_cluster').agg({
    'agegroup': lambda x: x.mode()[0],
    'hhsize': lambda x: x.mode()[0],
    'hhinc_group': 'mean',
    'main_journey_mode': lambda x: x.mode()[0]
}).reset_index()

print("\nCluster Summary (K-Means):\n", cluster_summary)

# Mode choice distribution by cluster
mode_distribution = pd.crosstab(
    final_df['kmeans_cluster'],
    final_df['main_journey_mode'],
    normalize='index'
)

plt.figure(figsize=(8, 6))
sns.heatmap(mode_distribution, annot=True, cmap="Blues", fmt=".2f")
plt.title("Mode Choice Distribution by K-Means Cluster")
plt.xlabel("Travel Mode")
plt.ylabel("Cluster")
plt.savefig('cluster_mode_distribution.png', dpi=300, bbox_inches='tight')
plt.show()
