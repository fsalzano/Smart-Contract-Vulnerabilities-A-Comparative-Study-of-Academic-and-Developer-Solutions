import pandas as pd

# Load dataset
df = pd.read_csv("random_commit_sample.csv")
print(df.shape)

# Ensure boolean types
df["has_to_be_caught"] = df["has_to_be_caught"].astype(bool)
df["caught"] = df["caught"].astype(bool)

# Confusion matrix components
tp = ((df["has_to_be_caught"] == True) & (df["caught"] == True)).sum()
fn = ((df["has_to_be_caught"] == True) & (df["caught"] == False)).sum()
tn = ((df["has_to_be_caught"] == False) & (df["caught"] == False)).sum()
fp = ((df["has_to_be_caught"] == False) & (df["caught"] == True)).sum()

# Metrics
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
specificity = tn / (tn + fp) if (tn + fp) > 0 else 0

# Output
print(f"✅ True Positives:  {tp}")
print(f"❌ False Negatives: {fn}")
print(f"✅ True Negatives:  {tn}")
print(f"❌ False Positives: {fp}")
print(f"🎯 Recall:     {recall:.4f}")
print(f"🛡️ Specificity: {specificity:.4f}")
