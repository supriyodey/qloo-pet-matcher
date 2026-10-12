import json
import math
import os
from typing import Dict, List, Any

BREEDS_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "breeds.json")

DIMENSION_LABELS = {
    "activity": "Activity Level",
    "space": "Living Space",
    "social": "Social Interaction",
    "travel": "Home Presence & Routine",
    "noise": "Noise & Lively Vibe"
}

# Dimension weights (space & activity weighted slightly higher as they most impact pet welfare)
WEIGHTS = {
    "activity": 1.25,
    "space": 1.20,
    "social": 1.00,
    "travel": 1.00,
    "noise": 0.90
}

def load_breeds() -> List[Dict[str, Any]]:
    with open(BREEDS_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_match(user_vector: Dict[str, float], breed_traits: Dict[str, float]) -> Dict[str, Any]:
    """
    Computes weighted Euclidean distance and match compatibility percentage.
    """
    sum_sq_diff = 0.0
    max_sq_diff = 0.0
    dim_diffs = {}

    for dim, weight in WEIGHTS.items():
        u_val = user_vector.get(dim, 3.0)
        b_val = breed_traits.get(dim, 3.0)
        diff = abs(u_val - b_val)
        dim_diffs[dim] = diff
        sum_sq_diff += weight * (diff ** 2)
        max_sq_diff += weight * (4.0 ** 2)  # max diff on scale 1 to 5 is 4

    distance = math.sqrt(sum_sq_diff)
    max_distance = math.sqrt(max_sq_diff)
    
    # Normalized score between 50% and 99%
    raw_fit = 1.0 - (distance / max_distance)
    # Rescale raw fit so good fits feel rewarding (typical close fit yields 88%-98%)
    match_pct = round(max(50.0, min(99.0, raw_fit * 100)), 1)

    return {
        "distance": round(distance, 3),
        "match_percentage": match_pct,
        "dim_diffs": dim_diffs
    }

def generate_why_it_fits(
    user_vector: Dict[str, float],
    breed: Dict[str, Any],
    dim_diffs: Dict[str, float]
) -> List[str]:
    """
    Synthesizes tailored explanation points based on closest trait alignments.
    """
    reasons = []
    sorted_dims = sorted(dim_diffs.items(), key=lambda x: x[1])
    best_dim_1 = sorted_dims[0][0]
    best_dim_2 = sorted_dims[1][0]

    b_name = breed["name"]
    species = breed["species"]

    # Trait 1 rationale
    if best_dim_1 == "activity":
        u_act = user_vector["activity"]
        if u_act >= 3.8:
            reasons.append(f"Athletic Harmony: Your high daily activity ({u_act}/5) complements the {b_name}'s craving for exercise and movement.")
        else:
            reasons.append(f"Relaxed Pace: Your peaceful energy ({u_act}/5) matches the {b_name}'s calm, low-demand daily rhythm.")
    elif best_dim_1 == "space":
        u_spc = user_vector["space"]
        if u_spc <= 2.5:
            reasons.append(f"Apartment Perfection: Highly comfortable with your cozy living footprint without feeling cramped.")
        else:
            reasons.append(f"Room to Flourish: Your generous living space gives the {b_name} the room it loves to explore.")
    elif best_dim_1 == "social":
        u_soc = user_vector["social"]
        if u_soc >= 4.0:
            reasons.append(f"Social Magnet: Matches your outgoing vibe and loves greeting visitors and joining gatherings.")
        else:
            reasons.append(f"Zen Companion: Respects personal boundaries and is content sharing quiet, unobtrusive company.")
    elif best_dim_1 == "travel":
        reasons.append(f"Schedule Sync: Perfectly fits your home presence rhythm and work-life balance.")
    elif best_dim_1 == "noise":
        reasons.append(f"Acoustic Fit: Seamlessly blends into your soundscape and household noise expectations.")

    # Trait 2 rationale
    if best_dim_2 == "space" and best_dim_1 != "space":
        reasons.append(f"Spatial Fit: Accommodates your habitat style with natural ease.")
    elif best_dim_2 == "social" and best_dim_1 != "social":
        reasons.append(f"Temperament Blend: {', '.join(breed.get('temperament', [])[:2])} nature harmonizes with your social circle.")
    elif best_dim_2 == "activity" and best_dim_1 != "activity":
        reasons.append(f"Energy Alignment: Daily play sessions will seamlessly match your schedule.")
    else:
        reasons.append(f"Lifestyle Bonus: {breed.get('tagline', '')}")

    # Unique species/trait perk
    if breed.get("hypoallergenic"):
        reasons.append("Hypoallergenic Advantage: Low dander makes this pet exceptionally gentle on indoor air quality.")
    elif breed.get("grooming") == "Low":
        reasons.append("Low Maintenance: Easy grooming routine that respects your busy daily calendar.")

    return reasons[:3]

def rank_breeds(user_vector: Dict[str, float]) -> Dict[str, Any]:
    breeds = load_breeds()
    ranked_dogs = []
    ranked_cats = []

    for b in breeds:
        match_info = calculate_match(user_vector, b["traits"])
        reasons = generate_why_it_fits(user_vector, b, match_info["dim_diffs"])
        
        item = {
            **b,
            "match_score": match_info["match_percentage"],
            "distance": match_info["distance"],
            "why_it_fits": reasons,
            "radar_data": {
                "labels": [DIMENSION_LABELS[k] for k in ["activity", "space", "social", "travel", "noise"]],
                "user_values": [user_vector[k] for k in ["activity", "space", "social", "travel", "noise"]],
                "breed_values": [b["traits"][k] for k in ["activity", "space", "social", "travel", "noise"]]
            }
        }

        if b["species"] == "dog":
            ranked_dogs.append(item)
        else:
            ranked_cats.append(item)

    ranked_dogs.sort(key=lambda x: x["distance"])
    ranked_cats.sort(key=lambda x: x["distance"])

    return {
        "top_dogs": ranked_dogs[:3],
        "runner_up_dogs": ranked_dogs[3:6],
        "top_cats": ranked_cats[:3],
        "runner_up_cats": ranked_cats[3:6],
        "all_ranked_dogs": ranked_dogs,
        "all_ranked_cats": ranked_cats
    }
