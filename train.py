import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

TRAIN_DIR = "data/train"
VAL_DIR = "data/val"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15
SEED = 42

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "model.keras")
LABELS_PATH = os.path.join(MODEL_DIR, "labels.json")

def main():
    tf.random.set_seed(SEED)
    np.random.seed(SEED)
    os.makedirs(MODEL_DIR, exist_ok=True)

    if not os.path.isdir(TRAIN_DIR) or not os.path.isdir(VAL_DIR):
        raise FileNotFoundError("Missing data/train or data/val. Run prepare_dataset.py first.")

    train_ds = tf.keras.utils.image_dataset_from_directory(
        TRAIN_DIR,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=True,
        seed=SEED
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        VAL_DIR,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    class_names = train_ds.class_names
    num_classes = len(class_names)
    print("Classes:", class_names)

    with open(LABELS_PATH, "w", encoding="utf-8") as f:
        json.dump({"class_names": class_names}, f, indent=2)

    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().prefetch(AUTOTUNE)
    val_ds = val_ds.cache().prefetch(AUTOTUNE)

    data_aug = tf.keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.08),
        layers.RandomZoom(0.12),
        layers.RandomContrast(0.1),
    ])

    preprocess = tf.keras.applications.mobilenet_v2.preprocess_input

    base = MobileNetV2(input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
                       include_top=False,
                       weights="imagenet")
    base.trainable = False

    inputs = layers.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    x = data_aug(inputs)
    x = preprocess(x)
    x = base(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)
    model = models.Model(inputs, outputs)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    cbs = [
        ModelCheckpoint(MODEL_PATH, monitor="val_accuracy", save_best_only=True),
        EarlyStopping(monitor="val_accuracy", patience=4, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.3, patience=2, min_lr=1e-6),
    ]

    print("\nTraining (frozen backbone)...")
    model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS, callbacks=cbs)

    print("\nFine-tuning...")
    base.trainable = True
    fine_tune_at = 120
    for layer in base.layers[:fine_tune_at]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-5),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    model.fit(train_ds, validation_data=val_ds, epochs=8, callbacks=cbs)

    print(f"\n✅ Saved model: {MODEL_PATH}")
    print(f"✅ Saved labels: {LABELS_PATH}")

if __name__ == "__main__":
    main()