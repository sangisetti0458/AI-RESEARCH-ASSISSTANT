import os
import pandas as pd
import arxiv

CATEGORIES = {
    "cs.AI": "Artificial Intelligence",
    "cs.CR": "Cyber Security",
    "cs.DC": "Cloud Computing",
    "cs.RO": "Robotics",
    "cs.LG": "Machine Learning",
    "cs.DB": "Data Science",
    "cs.IR": "Information Retrieval",
}

client = arxiv.Client()

rows = []

for category, label in CATEGORIES.items():

    print(f"Downloading {category}...")

    search = arxiv.Search(
        query=f"cat:{category}",
        max_results=200,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    for paper in client.results(search):

        rows.append(
            {
                "title": paper.title,
                "text": paper.summary.replace("\n", " "),
                "category": label,
            }
        )

os.makedirs("app/ml/dataset", exist_ok=True)

df = pd.DataFrame(rows)

df.to_csv(
    "app/ml/dataset/technology_dataset.csv",
    index=False,
    encoding="utf-8",
)

print(df.head())
print(f"\nTotal Papers: {len(df)}")