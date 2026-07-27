from datasets import load_dataset

print("Loading dataset...")

dataset = load_dataset(
    "ccdv/arxiv-classification",
    "no_ref"
)

print(dataset)

print("\nFeatures:")
print(dataset["train"].features)

print("\nLabel Names:")
print(dataset["train"].features["label"].names)

print("\nFirst Sample:")
print(dataset["train"][0])