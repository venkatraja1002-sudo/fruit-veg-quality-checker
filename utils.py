from typing import Dict, Tuple

FRUITS = {
    "apple", "banana", "orange"
}

VEGETABLES = {
    "tomato", "capsicum", "bitter_gourd"
}

HEALTH_BENEFITS: Dict[str, str] = {
    "apple": "High fiber + vitamin C. Supports heart health and digestion.",
    "banana": "High potassium. Supports muscles, nerves, and energy.",
    "orange": "Vitamin C rich. Supports immunity and skin health.",
    "tomato": "Lycopene antioxidant. Supports heart and skin health.",
    "capsicum": "Vitamin C + antioxidants. Supports immunity and eye health.",
    "bitter_gourd": "Low calorie, rich in antioxidants; commonly used for blood sugar support (traditional use).",
}

# Nutrition values are approximate per 100g (common reference).
# These are general nutrition facts; they can vary by variety and ripeness.
NUTRITION_PER_100G: Dict[str, Dict[str, str]] = {
    "apple": {
        "Serving (reference)": "100 g",
        "Calories": "52 kcal",
        "Carbs": "13.8 g",
        "Fiber": "2.4 g",
        "Protein": "0.3 g",
        "Fat": "0.2 g",
        "Vitamin C": "~4.6 mg",
        "Potassium": "~107 mg",
    },
    "banana": {
        "Serving (reference)": "100 g",
        "Calories": "89 kcal",
        "Carbs": "22.8 g",
        "Fiber": "2.6 g",
        "Protein": "1.1 g",
        "Fat": "0.3 g",
        "Vitamin C": "~8.7 mg",
        "Potassium": "~358 mg",
    },
    "orange": {
        "Serving (reference)": "100 g",
        "Calories": "47 kcal",
        "Carbs": "11.8 g",
        "Fiber": "2.4 g",
        "Protein": "0.9 g",
        "Fat": "0.1 g",
        "Vitamin C": "~53.2 mg",
        "Potassium": "~181 mg",
    },
    "tomato": {
        "Serving (reference)": "100 g",
        "Calories": "18 kcal",
        "Carbs": "3.9 g",
        "Fiber": "1.2 g",
        "Protein": "0.9 g",
        "Fat": "0.2 g",
        "Vitamin C": "~13.7 mg",
        "Potassium": "~237 mg",
    },
    "capsicum": {
        "Serving (reference)": "100 g",
        "Calories": "31 kcal",
        "Carbs": "6.0 g",
        "Fiber": "2.1 g",
        "Protein": "1.0 g",
        "Fat": "0.3 g",
        "Vitamin C": "~127.7 mg",
        "Potassium": "~211 mg",
    },
    "bitter_gourd": {
        "Serving (reference)": "100 g",
        "Calories": "17 kcal",
        "Carbs": "3.7 g",
        "Fiber": "2.8 g",
        "Protein": "1.0 g",
        "Fat": "0.2 g",
        "Vitamin C": "~84 mg",
        "Potassium": "~296 mg",
    },
}

# For calorie counter calculations (kcal per 100g)
CALORIES_PER_100G: Dict[str, float] = {
    "apple": 52.0,
    "banana": 89.0,
    "orange": 47.0,
    "tomato": 18.0,
    "capsicum": 31.0,
    "bitter_gourd": 17.0,
}

def parse_label(label: str) -> Tuple[str, str]:
    parts = label.lower().split("_")
    if len(parts) >= 2:
        name = "_".join(parts[:-1])
        quality = parts[-1]
        return name, quality
    return label.lower(), "unknown"

def get_category(name: str) -> str:
    n = name.lower()
    if n in FRUITS:
        return "Fruit"
    if n in VEGETABLES:
        return "Vegetable"
    return "Food item"

def get_benefits(name: str) -> str:
    return HEALTH_BENEFITS.get(name.lower(), "Natural food. Contains useful vitamins/minerals depending on variety.")

def get_recommendation(quality: str) -> str:
    q = quality.lower()
    if q == "fresh":
        return "✅ Fresh: Safe to eat / sell."
    if q == "rotten":
        return "❌ Rotten/Stale: Discard and avoid consumption."
    if q == "unknown":
        return "ℹ️ Quality not available in this dataset."
    return "ℹ️ Inspect manually for best decision."

def get_nutrition_table(name: str) -> Dict[str, str] | None:
    return NUTRITION_PER_100G.get(name.lower())

def estimate_calories(name: str, grams: float) -> float | None:
    """Estimate calories for a given weight in grams based on kcal per 100g."""
    kcal100 = CALORIES_PER_100G.get(name.lower())
    if kcal100 is None:
        return None
    grams = max(0.0, float(grams))
    return (kcal100 / 100.0) * grams