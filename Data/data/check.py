import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

# 读取两个CSV文件
df_grountruth = pd.read_csv('Data\license\\fixedresult.csv')
df_result = pd.read_csv('Data\license\liresolver\\tldr-licenses-forSpdx.csv')
all_columns = [
    "Distribute", "Modify", "Commercial Use", "Relicense", "Hold Liable",
    "Use Patent Claims", "Sublicense", "Statically Link", "Private Use",
    "Use Trademark", "Place Warranty","Include Copyright", "Include License", "Include Notice", "Disclose Source",
    "State Changes", "Include Original", "Give Credit", "Rename", "Contact Author",
    "Include Install Instructions", "Compensate for Damages", "Pay Above Use Threshold"
]
right_columns = [
    "Distribute", "Modify", "Commercial Use", "Relicense", "Hold Liable",
    "Use Patent Claims", "Sublicense", "Statically Link", "Private Use",
    "Use Trademark", "Place Warranty"
]

obligation_columns = [
    "Include Copyright", "Include License", "Include Notice", "Disclose Source",
    "State Changes", "Include Original", "Give Credit", "Rename", "Contact Author",
    "Include Install Instructions", "Compensate for Damages", "Pay Above Use Threshold"
]
columns = [
    (all_columns, "all "),
    (right_columns, "right "),
    (obligation_columns, "obligation ")
]


for column_group, group_name in columns:
    precision_scores = []
    recall_scores = []
    f1_scores = []

    for column in column_group:
        y_true = df_grountruth[column].fillna("").tolist()  
        y_pred = df_result[column].fillna("").tolist()  
        precision = precision_score(y_true, y_pred, average='macro', zero_division=0)
        recall = recall_score(y_true, y_pred, average='macro', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)
        precision_scores.append(precision)
        recall_scores.append(recall)
        f1_scores.append(f1)

    average_precision = sum(precision_scores) / len(precision_scores)
    average_recall = sum(recall_scores) / len(recall_scores)
    average_f1 = sum(f1_scores) / len(f1_scores)

    print(f"Precision of {group_name}: {average_precision:.4f}")
    print(f"Recall of {group_name}: {average_recall:.4f}")
    print(f"F1 Score of { group_name}: {average_f1:.4f}")
   
