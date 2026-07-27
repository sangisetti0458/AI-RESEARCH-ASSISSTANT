from datasets import load_dataset
import pandas as pd
import os

# Dataset labels mapped to readable categories
CATEGORY_MAPPING = {
    "cs.AI": "Artificial Intelligence",
    "cs.CV": "Computer Vision",
    "cs.SY": "Systems Engineering",
    "cs.CE": "Computer Engineering",
    "cs.PL": "Programming Languages",
    "cs.IT": "Information Theory",
    "cs.DS": "Data Structures",
    "cs.NE": "Neural Networks",
}

OUTPUT_DIR = "app/ml/dataset"


def prepare_dataset():
    print("Loading arXiv Classification Dataset...\n")

    dataset = load_dataset(
        "ccdv/arxiv-classification",
        "no_ref"
    )

    train = dataset["train"]

    label_names = train.features["label"].names

    rows = []

    for item in train:
        label_name = label_names[item["label"]]

        if label_name not in CATEGORY_MAPPING:
            continue

        rows.append(
            {
                "text": item["text"],
                "category": CATEGORY_MAPPING[label_name],
            }
        )

    df = pd.DataFrame(rows)

    print(f"Total Samples Selected: {len(df)}")

    print("\nCategory Distribution:\n")
    print(df["category"].value_counts())

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Shuffle dataset
    df = df.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    train_size = int(len(df) * 0.8)

    train_df = df.iloc[:train_size]
    test_df = df.iloc[train_size:]

    train_df.to_csv(
        os.path.join(OUTPUT_DIR, "train.csv"),
        index=False,
        encoding="utf-8",
    )

    test_df.to_csv(
        os.path.join(OUTPUT_DIR, "test.csv"),
        index=False,
        encoding="utf-8",
    )

    print("\n========================================")
    print("Dataset Created Successfully")
    print("========================================")
    print(f"Training Samples : {len(train_df)}")
    print(f"Testing Samples  : {len(test_df)}")
    print("Saved Files:")
    print("✓ train.csv")
    print("✓ test.csv")


if __name__ == "__main__":
    prepare_dataset()