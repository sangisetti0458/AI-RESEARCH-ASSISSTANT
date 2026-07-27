import os
import pickle
import pandas as pd
import tensorflow as tf

from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.layers import (
    TextVectorization,
    Embedding,
    GlobalAveragePooling1D,
    Dense,
    Dropout,
)
from tensorflow.keras.models import Sequential

DATASET_DIR = "app/ml/dataset"
MODEL_DIR = "app/ml/models"

os.makedirs(MODEL_DIR, exist_ok=True)

print("Loading datasets...")

train_df = pd.read_csv(os.path.join(DATASET_DIR, "train.csv"))
test_df = pd.read_csv(os.path.join(DATASET_DIR, "test.csv"))

train_df = train_df.dropna()
test_df = test_df.dropna()

train_text = train_df["text"].astype(str).values
test_text = test_df["text"].astype(str).values

label_encoder = LabelEncoder()

train_labels = label_encoder.fit_transform(train_df["category"])
test_labels = label_encoder.transform(test_df["category"])

print("\nClasses:")
print(label_encoder.classes_)

# Save Label Encoder
with open(os.path.join(MODEL_DIR, "label_encoder.pkl"), "wb") as f:
    pickle.dump(label_encoder, f)

VOCAB_SIZE = 30000
SEQUENCE_LENGTH = 500
BATCH_SIZE = 32

vectorizer = TextVectorization(
    max_tokens=VOCAB_SIZE,
    output_mode="int",
    output_sequence_length=SEQUENCE_LENGTH,
)

print("\nBuilding vocabulary...")
vectorizer.adapt(train_text)

# Save vocabulary as UTF-8 (Windows-safe)
vocabulary = vectorizer.get_vocabulary()

with open(
    os.path.join(MODEL_DIR, "vocabulary.txt"),
    "w",
    encoding="utf-8",
) as f:
    for word in vocabulary:
        f.write(word + "\n")

# Build datasets
train_ds = (
    tf.data.Dataset.from_tensor_slices((train_text, train_labels))
    .shuffle(len(train_text))
    .batch(BATCH_SIZE)
    .prefetch(tf.data.AUTOTUNE)
)

test_ds = (
    tf.data.Dataset.from_tensor_slices((test_text, test_labels))
    .batch(BATCH_SIZE)
    .prefetch(tf.data.AUTOTUNE)
)

model = Sequential(
    [
        vectorizer,
        Embedding(VOCAB_SIZE, 128),
        GlobalAveragePooling1D(),
        Dense(128, activation="relu"),
        Dropout(0.3),
        Dense(len(label_encoder.classes_), activation="softmax"),
    ]
)

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

print("\nModel Summary")
model.summary()

print("\nTraining model...\n")

history = model.fit(
    train_ds,
    validation_data=test_ds,
    epochs=5,
)

loss, accuracy = model.evaluate(test_ds)

print(f"\nTest Accuracy: {accuracy:.4f}")

# Save model in Keras format
model.save(
    os.path.join(MODEL_DIR, "tf_classifier.keras")
)

print("\nFiles Saved:")

print("✓ tf_classifier.keras")
print("✓ label_encoder.pkl")
print("✓ vocabulary.txt")

print("\nModel Saved Successfully!")