# ==============================
# I acknowledge the use of ChatGPT [https://chat.openai.com/] to assist with the coding part of this assignment.
# I entered the following prompts: “How to implement Decision Tree and KNN for travel mode prediction using scikit-learn”
#                                  “How to tune hyperparameters and evaluate models with confusion matrices”
# I used the output to assist in writing the supervised machine learning code.

# ==============================

import os
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    classification_report, accuracy_score, f1_score,
    confusion_matrix, ConfusionMatrixDisplay
)

from Data_Preprocessing import process_data


# =============================
# Step 1: Load and preprocess data
# =============================
df = process_data()

# Drop identifiers
X = df.drop(columns=['hhid', 'persid', 'main_journey_mode'])
y = df['main_journey_mode']

# Encode categorical features
for col in X.columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])

y_le = LabelEncoder()
y = y_le.fit_transform(y)

# Create output folder for visuals
output_dir = "Supervised_ML_Visual"
os.makedirs(output_dir, exist_ok=True)

# =============================
# Step 2: Stratified train-test split
# =============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# =============================
# Step 3: Decision Tree - Hyperparameter Tuning
# =============================
print("=== Decision Tree Classifier (Hyperparameter Tuning) ===")

depths = range(2, 11)
criteria = ["gini", "entropy"]
dt_results = []

for criterion in criteria:
    for depth in depths:
        dtree = DecisionTreeClassifier(criterion=criterion, max_depth=depth, random_state=42)
        dtree.fit(X_train, y_train)
        y_pred = dtree.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")
        dt_results.append((criterion, depth, acc, f1))

# Convert results to DataFrame
dt_df = pd.DataFrame(dt_results, columns=["Criterion", "Max Depth", "Accuracy", "F1"])
print("\nDecision Tree tuning results:\n", dt_df)

# Pick best model
best_dt = dt_df.sort_values(by="F1", ascending=False).iloc[0]
print("\nBest Decision Tree -> Criterion:", best_dt["Criterion"],
      "Max Depth:", best_dt["Max Depth"],
      "Accuracy:", best_dt["Accuracy"],
      "F1:", best_dt["F1"])

# Train final best model
dtree = DecisionTreeClassifier(
    criterion=best_dt["Criterion"],
    max_depth=int(best_dt["Max Depth"]),
    random_state=42
)
dtree.fit(X_train, y_train)
y_pred_dt = dtree.predict(X_test)

print("\nClassification Report (Decision Tree):")
print(classification_report(y_test, y_pred_dt, target_names=y_le.classes_))

# Save confusion matrix as PNG
ConfusionMatrixDisplay.from_estimator(dtree, X_test, y_test, display_labels=y_le.classes_)
plt.title("Decision Tree Confusion Matrix")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "decision_tree_confusion_matrix.png"))
plt.close()


# =============================
# Step 4: KNN - Hyperparameter Tuning
# =============================
print("\n=== KNN Classifier (Hyperparameter Tuning) ===")

k_values = range(3, 16, 2)  # try odd k from 3 to 15
knn_results = []

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="weighted")
    knn_results.append((k, acc, f1))

# Convert to DataFrame
knn_df = pd.DataFrame(knn_results, columns=["k", "Accuracy", "F1"])
print("\nKNN tuning results:\n", knn_df)

# Pick best model
best_knn = knn_df.sort_values(by="F1", ascending=False).iloc[0]
print("\nBest KNN -> k:", best_knn["k"],
      "Accuracy:", best_knn["Accuracy"],
      "F1:", best_knn["F1"])

# Train final best KNN
knn = KNeighborsClassifier(n_neighbors=int(best_knn["k"]))
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)

print("\nClassification Report (KNN):")
print(classification_report(y_test, y_pred_knn, target_names=y_le.classes_))

# Save confusion matrix as PNG
ConfusionMatrixDisplay.from_estimator(knn, X_test, y_test, display_labels=y_le.classes_)
plt.title(f"KNN Confusion Matrix (k={best_knn['k']})")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, f"knn_confusion_matrix_k{best_knn['k']}.png"))
plt.close()


# =============================
# Step 5: Class Distribution Plot
# =============================
sns.countplot(x=y_le.inverse_transform(y), order=y_le.classes_)
plt.title("Distribution of Travel Modes (Class Balance)")
plt.xlabel("Travel Mode")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "travel_mode_distribution.png"))
plt.close()

print(f"\nAll visuals saved in folder: {output_dir}/")

