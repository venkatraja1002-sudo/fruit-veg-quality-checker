import json
import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image

from utils import (
    parse_label,
    get_category,
    get_benefits,
    get_recommendation,
    get_nutrition_table,
    estimate_calories,
)

IMG_SIZE = (224, 224)

st.set_page_config(page_title="Smart Food AI", page_icon="🥗", layout="centered")


@st.cache_resource
def load_model_and_labels():
    model = tf.keras.models.load_model("models/model.keras")
    with open("models/labels.json", "r", encoding="utf-8") as f:
        class_names = json.load(f)["class_names"]
    return model, class_names


def preprocess(pil_img: Image.Image):
    img = pil_img.convert("RGB").resize(IMG_SIZE)
    arr = np.array(img).astype(np.float32)
    arr = np.expand_dims(arr, axis=0)
    return arr


def topk_predictions(model, class_names, pil_img, k=3):
    x = preprocess(pil_img)
    probs = model.predict(x, verbose=0)[0]
    idx = probs.argsort()[::-1][:k]
    return [(class_names[i], float(probs[i])) for i in idx]


def main():
    st.title("🥗 fruit and vegitable qulity and name checker")
    st.write(
        "Upload an image to detect **food name**, **fruit/vegetable**, **fresh vs rotten/stale**, "
        "and get **health + nutrition info**."
    )

    # Load model
    try:
        model, class_names = load_model_and_labels()
    except Exception as e:
        st.error("Model not found. Make sure you trained the model first.")
        st.code(str(e))
        st.stop()

    file = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png", "webp"])

    if not file:
        st.info("👆 Upload an image to start.")
        st.stop()

    # Show image
    img = Image.open(file)
    st.image(img, caption="Uploaded image", use_column_width=True)

    # Predict
    preds = topk_predictions(model, class_names, img, k=3)
    best_label, best_prob = preds[0]

    # Parse outputs
    name, quality = parse_label(best_label)
    category = get_category(name)
    benefits = get_benefits(name)
    recommendation = get_recommendation(quality)

    # Main result UI
    st.subheader("🔎 Food Analysis Result")
    col1, col2, col3 = st.columns(3)
    col1.metric("Name", name.replace("_", " ").title())
    col2.metric("Type", category)
    col3.metric("Quality", quality.title(), f"{best_prob*100:.2f}%")

    st.success(recommendation)

    # Health benefits
    st.markdown("### 💊 Health Benefits")
    st.info(benefits)

    # Nutrition table
    st.markdown("### 🥗 Nutrition Facts (approx. per 100g)")
    nutrition = get_nutrition_table(name)
    if nutrition:
        st.table(nutrition)
    else:
        st.info("Nutrition facts not available for this item yet.")

    # Calorie counter
    st.markdown("### 🔥 Calorie Counter")
    grams = st.number_input(
        "Enter portion size (grams)",
        min_value=0.0,
        max_value=2000.0,
        value=100.0,
        step=10.0,
    )

    cal_est = estimate_calories(name, grams)
    if cal_est is None:
        st.info("Calorie estimate not available for this item yet.")
    else:
        st.metric("Estimated Calories", f"{cal_est:.1f} kcal", f"for {grams:.0f} g")

    # Top-3 predictions
    st.markdown("### 📌 Top-3 Predictions")
    for lbl, p in preds:
        n, q = parse_label(lbl)
        st.write(f"**{n.replace('_',' ').title()}** ({q}) — {p*100:.2f}%")
        st.progress(min(int(p * 100), 100))

    st.caption("Model: MobileNetV2 Transfer Learning • UI: Streamlit")


if __name__ == "__main__":
    main()