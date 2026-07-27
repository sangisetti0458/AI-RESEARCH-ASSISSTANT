from datasets import load_dataset

print("Loading dataset...")

dataset = load_dataset(
    "CShorten/ML-ArXiv-Papers"
)

print(dataset)

print(dataset["train"][0])