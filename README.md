Overview

This project analyses demographic characteristics and mobility patterns using the 2023–2024 Victorian Integrated Survey of Travel and Activity (VISTA) dataset. The analysis investigates how demographic factors are associated with travel mode choice across Victoria, combining data cleaning, exploratory statistical analysis, classification, and clustering to identify patterns in travel behaviour. The project aims to provide insights into the relationship between demographic characteristics and mobility choices and demonstrate how data science techniques can be applied to real-world travel survey data.

#Data Preprocessing
- Merged 3 datasets: household, person and journey-to-work based on hhid and persid
- Filtered records to include working individuals only
- Selected columns: age, household_size, household_income, and main_journey_mode
- Cleaned missing or inconsistent values, and converted age, household_size and 
  main_journey_mode into categorical data

To run the code: 
- Place the dataset files in the same directory as the script
- run the command: python Data_Preprocessing.py all


#Correlation Analysis
Brief Details of the Implementation:
1. Preprocessed dataset is loaded using 'process_data()' from 'Data_Preprocessing.py'
2. Normalized Mutual Information (NMI)
 - Probabilities, Entropies and Conditional Entropies are computed manually to derive MI values for each feature 
 - Normalized to scale MI between 0 and 1
3. Visualization
 - Count plots showing travel mode distributions for each feature.
 - Heatmaps showing cross-tabulated counts.
 - Bar chart showing NMI values across features.
 - All generated images are saved automatically to '.png' in the working directory

To run the code:
Run the following command in your terminal or command prompt
python Correlation_Analysis.pys


#Supervised Machine Learning
Brief Details for the Implementation
1. Data Processing
- Loaded dataset using `process_data()` from `Data_Preprocessing.py`. 
- Removed identifier columns (`hhid`, `persid`) and label-encoded categorical features.  
- Split data into training and testing sets using stratified sampling

2. Model Training and Evaluation
- Implemented Decision Tree and K-Nearest Neighbours (KNN) classifiers using *scikit-learn*.  
- Tuned parameters: Decision Tree (criterion: gini, entropy; depth: 2–10) and KNN (k = 3–15).  
- Evaluated using accuracy, precision, recall, and F1-score.  
- Generated confusion matrices and class distribution plot as `.png` files.  

To run the code:
Run the following command in your terminal or command prompt
python Supervised_ML.py all

#Clustering Analysis
Brief Details of the Implementation:

1. Data Preprocessing
- Loaded dataset using `process_data()` from Data_Preprocessing.py.
- Converted income ranges to numeric midpoints and label-encoded demographics.
- Normalized selected features (`agegroup`, `hhinc_group`, `hhsize`) using MinMaxScaler.

2. Clustering
- Applied K-Means with optimal k = 3 via Elbow Method.
- Performed Hierarchical Clustering (Ward linkage) and generated dendrograms.

3. PCA & Visualization

- Conducted PCA on scaled data and visualized loadings via heatmap.
- Created visual outputs: Elbow Plot, Dendrogram, PCA Loadings Heatmap, and Mode Distribution Heatmap.

4. Cluster Interpretation
- Summarized clusters by demographic features and main travel mode.

 To run the code:
 Run the following command in your terminal or command prompt
 python Clustering_Analysis.py all

 #Data Distribution
 - Read in journey-to-work csv file
 - Counts the frequency for different travel modes
 - Plot the frequency of each travel mode to show the distribution of the data

 To run the code: 
 Run the following command in your terminal or command prompt
 python Data_Distribution.py all
