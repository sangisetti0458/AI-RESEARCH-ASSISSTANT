import tensorflow as tf

model = tf.keras.models.load_model("app/ml/models/tf_classifier.keras")

print("=" * 60)
print("MODEL SUMMARY")
print("=" * 60)

model.summary()

print("\nFIRST LAYER:")
print(type(model.layers[0]))
print(model.layers[0])

print("\nALL LAYERS:")
for i, layer in enumerate(model.layers):
    print(i, type(layer), layer.name)