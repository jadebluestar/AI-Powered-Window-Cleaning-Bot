

## Glass Stain Detection Model (YOLO)

This repository was made for the sole purpose of training a **computer vision model (YOLO)** that can identify and classify stains on glass for the ASME BrainBolt Hackathon.

### Stains Covered

* rain\_streaks
* bird\_droppings
* dust\_spots
* water\_spots
* grime\_buildup
* fingerprints
* insect\_remains
* pollen\_residue
* construction\_debris
* salt\_stains

## Model Limitations and Justification for Use

### Current Model Performance

This model is **not perfect** and has several limitations:

* May misclassify similar-looking stains (e.g., water spots vs. dust spots)
* Performance varies with lighting conditions and image quality
* Limited training data may affect detection accuracy for rare stain types
* False positives/negatives occur, especially with overlapping stain types

---

## Model Evaluation & Accuracy

Evaluating accuracy is essential to understand the model’s strengths and weaknesses.

### 1. **During Training**

* Training logs show evolving accuracy with metrics like:

  * **Precision (P):** Of the detections made, how many were correct
  * **Recall (R):** Of all actual objects, how many were found
  * **mAP50:** Mean Average Precision at IoU = 0.5 (looser threshold)
  * **mAP50-95:** mAP across IoU thresholds 0.5 → 0.95 (stricter, standard metric)

Example log entry:

```
Class     Images  Instances      Box(P)      R      mAP50   mAP50-95
all        162       461        0.00549   0.495   0.0909    0.0625
```

### 2. **Validation / Test Evaluation**

After training, evaluate performance on validation/test data:

```python
from ultralytics import YOLO

model = YOLO("runs/detect/train6/weights/best.pt")
metrics = model.val()  # returns precision, recall, mAP scores
print(metrics)
```

### 3. **Visual Testing on New Images**

To manually check predictions:

```python
results = model.predict(source="path/to/test/images", save=True, conf=0.25)
```

* Saves images with bounding boxes
* `conf` sets minimum confidence threshold

 A good mAP for practical use depends on context:

* **>0.5 (50%)** = usable for initial screening
* **0.7–0.8 (70–80%)** = strong for most industrial/commercial tasks
* **0.9+ (90%)** = typically needed for safety-critical applications

---

## Why Use This Model Despite Imperfections?

### 1. **Automation Over Manual Inspection**

* Even 70–80% accuracy is better than manual inspection at scale
* Reduces human error and fatigue in repetitive tasks
* Provides consistent detection across different operators

### 2. **Foundation for Improvement**

* Baseline model that can be improved iteratively
* Easy to retrain with more data
* Provides immediate value while working toward higher accuracy

### 3. **Practical Applications**

* **Quality Control:** Flag potentially dirty glass for review
* **Maintenance Scheduling:** Identify cleaning priorities
* **Research Tool:** Analyze stain patterns and frequency
* **Training Data:** Generate labeled examples for future models

### 4. **Real-World Context**

* Perfect accuracy isn’t always necessary
* Cost-effective vs. alternatives (sensors, manual checks)
* Enables faster decision-making

### 5. **Transparent Limitations**

* Users understand constraints and can act accordingly
* Combine with human oversight for critical applications
* Confidence scores help assess reliability

---

## Recommended Usage Guidelines

 **Good Use Cases:**

* Initial screening/filtering of glass surfaces
* Trend analysis and pattern recognition
* Automated alerts for excessive contamination
* Training tool for human inspectors

⚠**Use with Caution:**

* Critical safety applications without oversight
* Final QC decisions without verification
* Applications needing 95%+ accuracy

**Not Recommended:**

* Medical/safety-critical environments
* Legal/regulatory compliance without validation
* Fully autonomous cleaning systems without fail-safes

---

## Future Improvements

* [ ] Expand training dataset with edge cases
* [ ] Implement confidence thresholding
* [ ] Add ensemble methods for better accuracy
* [ ] Collect user feedback for refinement
* [ ] Integrate active learning pipeline

