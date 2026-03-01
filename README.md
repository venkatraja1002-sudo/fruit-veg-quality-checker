# 🥗 Smart Fruit & Vegetable Name + Quality Checker

An AI-powered web application that detects **fruit/vegetable name**, checks **fresh vs stale/rotten quality**, and provides **nutrition facts + calorie estimation**.

Built using **TensorFlow (MobileNetV2 Transfer Learning) and Streamlit**.

---

## 🚀 Features

- ✅ Detects food name (Apple, Banana, Orange, Tomato, Capsicum, Bitter Gourd)
- ✅ Classifies **Fruit or Vegetable**
- ✅ Detects **Fresh vs Rotten/Stale**
- ✅ Shows **Prediction Confidence**
- ✅ Displays **Health Benefits**
- ✅ Shows **Nutrition Facts (per 100g)**
- ✅ Includes **Calorie Counter (portion-based estimation)**
- ✅ Clean and simple Streamlit UI

---

## 🧠 Model Information

- Model: MobileNetV2 (Transfer Learning)
- Framework: TensorFlow 2.15
- Image Size: 224 × 224
- Trained Classes:

```
apple_fresh
apple_rotten
banana_fresh
banana_rotten
orange_fresh
orange_rotten
tomato_fresh
tomato_rotten
capsicum_fresh
capsicum_rotten
bitter_gourd_fresh
bitter_gourd_rotten
```

> Note: "Stale" is treated as "Rotten" in the model output.

---

## 📊 Nutrition & Calorie Estimation

Nutrition values are based on approximate reference values per 100g.

Calorie formula:

Estimated Calories = (Calories per 100g / 100) × portion size in grams

Example:
Apple → 52 kcal per 100g  
200g Apple → 104 kcal  

---

## 📂 Project Structure

```
fruit-veg-quality-checker/
│
├── app.py
├── utils.py
├── train.py
├── prepare_dataset.py
├── requirements.txt
│
├── models/
│   ├── model.keras
│   └── labels.json
│
├── data/ (generated after prepare step)
└── data_raw/ (dataset folder)
```

---

## 🛠 Installation (Run Locally)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/fruit-veg-quality-checker.git
cd fruit-veg-quality-checker
```

---

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run the Application

```bash
streamlit run app.py
```

The app will open in your browser.

---

## 🏋️ Training the Model (Optional)

If you want to retrain the model:

```bash
python prepare_dataset.py
python train.py
```

This will generate:

```
models/model.keras
models/labels.json
```

---

## 🌍 Deployment

This project can be deployed using:

- Streamlit Community Cloud
- Render
- Railway
- Hugging Face Spaces

### Deploy on Streamlit Cloud

1. Push project to GitHub
2. Go to https://share.streamlit.io
3. Select repository
4. Choose `app.py`
5. Click Deploy

---

## ⚠ Limitations

- Model supports only trained fruits and vegetables.
- Nutrition values are approximate.
- Accuracy depends on dataset quality.

---

## 🧑‍💻 Tech Stack

- Python
- TensorFlow
- Keras
- Streamlit
- NumPy
- Pillow

---

## 📜 License

This project is created for educational and portfolio purposes.

---

## 🙌 Author

Venkat Raja C
