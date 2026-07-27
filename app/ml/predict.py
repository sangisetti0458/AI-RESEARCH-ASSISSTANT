import os
import pickle

import keras
import tensorflow as tf

MODEL_DIR = "app/ml/models"

VOCAB_SIZE = 30000
SEQUENCE_LENGTH = 500

# Load trained model using Keras 3
model = keras.models.load_model(
    os.path.join(MODEL_DIR, "tf_classifier.keras"),
    compile=False,
)

# Load label encoder
with open(
    os.path.join(MODEL_DIR, "label_encoder.pkl"),
    "rb",
) as f:
    label_encoder = pickle.load(f)

# Load vocabulary
with open(
    os.path.join(MODEL_DIR, "vocabulary.txt"),
    "r",
    encoding="utf-8",
) as f:
    vocabulary = [line.rstrip("\n") for line in f]

# Rebuild TextVectorization
vectorizer = keras.layers.TextVectorization(
    max_tokens=VOCAB_SIZE,
    output_mode="int",
    output_sequence_length=SEQUENCE_LENGTH,
)

vectorizer.set_vocabulary(vocabulary)


def predict_category(text: str):
    if not text or not text.strip():
        return {
            "category": "Unknown",
            "confidence": 0.0,
        }

    vectorized = vectorizer(tf.constant([text]))

    prediction = model.predict(vectorized, verbose=0)

    class_index = int(tf.argmax(prediction[0]))
    confidence = float(tf.reduce_max(prediction[0]))

    category = label_encoder.inverse_transform([class_index])[0]

    return {
        "category": category,
        "confidence": round(confidence, 4),
    }


if __name__ == "__main__":
    sample = """
    Deep learning models and convolutional neural networks
    are widely used for image recognition and object detection.
    """

    print(predict_category(sample))