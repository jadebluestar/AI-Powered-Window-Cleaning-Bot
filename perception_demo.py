from PIL import Image, ImageDraw
import json, os
from controller_demo import score_detections  # Import your scoring logic

# Paths
test_dir = "data/test_images"
out_dir = "results"
os.makedirs(out_dir, exist_ok=True)

# Temporary simulated detections (replace with YOLOv8 later)
def simulate_detections(img_w, img_h):
    return [
        {"x1": 320, "y1": 220, "x2": 380, "y2": 280, "confidence": 0.92, "img_w": img_w, "img_h": img_h},
        {"x1": 700, "y1": 140, "x2": 760, "y2": 200, "confidence": 0.77, "img_w": img_w, "img_h": img_h},
        {"x1": 450, "y1": 430, "x2": 520, "y2": 500, "confidence": 0.58, "img_w": img_w, "img_h": img_h},
    ]

# Process every image
for fname in os.listdir(test_dir):
    if not fname.lower().endswith((".jpg", ".png", ".jpeg")):
        continue

    img_path = os.path.join(test_dir, fname)
    img = Image.open(img_path)
    img_w, img_h = img.size

    detections = simulate_detections(img_w, img_h)  # Later: use YOLO detections
    scored = score_detections(detections)

    print(f"\n--- Cleaning Plan for {fname} ---")
    print(json.dumps(scored, indent=2))

    # Draw boxes & labels
    vis = img.copy()
    draw = ImageDraw.Draw(vis)
    for d in scored:
        draw.rectangle([(d["x1"], d["y1"]), (d["x2"], d["y2"])], outline=(255, 0, 0), width=6)
        draw.text((d["x1"], d["y1"] - 18), f"{d['action']['strategy']} {d['score']}", fill=(255, 255, 255))

    out_path = os.path.join(out_dir, f"{os.path.splitext(fname)[0]}_output.jpg")
    if vis.mode == "RGBA":
        vis = vis.convert("RGB")
    vis.save(out_path)
    print(f"Saved visualization: {out_path}")
