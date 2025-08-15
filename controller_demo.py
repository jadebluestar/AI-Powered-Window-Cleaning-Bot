# Priority scoring functions (copy this into controller_demo.py if you want)
def _area(det):
    return max(0, (det["x2"] - det["x1"]) * (det["y2"] - det["y1"]))

def score_detection(det, w_conf=0.6, w_area=0.4):
    """Score in [0,1] using confidence and normalized area."""
    conf = det.get("confidence", 0)
    ar = _area(det)
    img_w = det.get("img_w", 1)
    img_h = det.get("img_h", 1)
    img_area = img_w * img_h
    norm_area = ar / img_area
    # area contribution scaled up so that reasonably sized blobs matter
    s = max(0.0, min(1.0, w_conf * conf + w_area * (norm_area * 10.0)))
    return s

def decide_action_from_score(score):
    """Map a scalar score to a discrete strategy and actuation parameters."""
    if score >= 0.80:
        return {
            "strategy": "HIGH_INTENSITY",
            "brush_speed_rpm": 120,
            "pressure_psi": 30,
            "spray_duration_s": 5
        }
    elif score >= 0.55:
        return {
            "strategy": "MEDIUM",
            "brush_speed_rpm": 80,
            "pressure_psi": 18,
            "spray_duration_s": 3
        }
    else:
        return {
            "strategy": "QUICK_PASS",
            "brush_speed_rpm": 40,
            "pressure_psi": 8,
            "spray_duration_s": 1
        }

def score_detections(detections):
    """Annotate list of detections with score and action, and sort by score desc."""
    for d in detections:
        s = score_detection(d)
        d["score"] = round(s, 3)
        d["action"] = decide_action_from_score(s)
    return sorted(detections, key=lambda x: x["score"], reverse=True)
