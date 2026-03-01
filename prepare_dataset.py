import shutil
import random
from pathlib import Path

random.seed(42)

RAW_DIR = Path("data_raw")
TRAIN_DIR = Path("data/train")
VAL_DIR = Path("data/val")

IMG_EXT = (".jpg", ".jpeg", ".png", ".webp")

def reset_output():
    if Path("data").exists():
        shutil.rmtree("data")
    TRAIN_DIR.mkdir(parents=True, exist_ok=True)
    VAL_DIR.mkdir(parents=True, exist_ok=True)

def parse_label_from_parent(folder_name: str):
    # Your folders are like: fresh_apple, stale_banana, etc.
    folder = folder_name.strip().lower()

    if folder.startswith("fresh_"):
        name = folder.replace("fresh_", "", 1)
        quality = "fresh"
        return f"{name}_{quality}"

    if folder.startswith("stale_"):
        name = folder.replace("stale_", "", 1)
        quality = "rotten"   # map stale -> rotten (or change to "stale" if you want)
        return f"{name}_{quality}"

    return None

def copy_split(label_to_imgs):
    for label, imgs in label_to_imgs.items():
        random.shuffle(imgs)
        split = max(1, int(len(imgs) * 0.8))
        train_imgs = imgs[:split]
        val_imgs = imgs[split:] if len(imgs) > split else imgs[:1]

        for img in train_imgs:
            dst = TRAIN_DIR / label
            dst.mkdir(parents=True, exist_ok=True)
            shutil.copy2(img, dst / img.name)

        for img in val_imgs:
            dst = VAL_DIR / label
            dst.mkdir(parents=True, exist_ok=True)
            shutil.copy2(img, dst / img.name)

def main():
    if not RAW_DIR.exists():
        print("❌ data_raw not found")
        return

    reset_output()

    label_to_imgs = {}
    total = 0
    used = 0

    for folder in RAW_DIR.iterdir():
        if not folder.is_dir():
            continue

        label = parse_label_from_parent(folder.name)
        if not label:
            continue

        for img in folder.rglob("*"):
            if img.is_file() and img.suffix.lower() in IMG_EXT:
                total += 1
                label_to_imgs.setdefault(label, []).append(img)
                used += 1

    if not label_to_imgs:
        print("❌ No labeled images found. Check folder names inside data_raw.")
        return

    copy_split(label_to_imgs)

    print("✅ Dataset prepared successfully!")
    print(f"Images used: {used}")
    print("Labels:", sorted(label_to_imgs.keys()))

if __name__ == "__main__":
    main()