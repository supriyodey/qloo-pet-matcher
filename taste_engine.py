import os
import re
import math
from typing import Dict, List, Any, Optional
import httpx
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

QLOO_API_KEY = os.getenv("QLOO_API_KEY", "")
QLOO_BASE_URL = os.getenv("QLOO_BASE_URL", "https://hackathon.api.qloo.com").rstrip("/")

# Built-in cultural correlation graph modeling Qloo's taste-to-lifestyle affinities
CULTURAL_TASTE_MODIFIERS: Dict[str, Dict[str, float]] = {
    # Outdoor / Active / Athletic
    "trail running": {"activity": 1.2, "space": 0.5, "noise": 0.2},
    "hiking": {"activity": 1.0, "space": 0.6, "noise": -0.2},
    "marathon": {"activity": 1.4, "space": 0.3},
    "crossfit": {"activity": 1.1, "social": 0.4},
    "surfing": {"activity": 1.0, "space": 0.4, "travel": -0.4},
    "camping": {"activity": 1.0, "space": 0.7, "social": -0.2},
    "national parks": {"activity": 0.9, "space": 0.6},
    "rock climbing": {"activity": 1.1, "space": 0.4},
    "cycling": {"activity": 0.9, "space": 0.3},
    "patagonia": {"activity": 0.8, "space": 0.5},
    "skiing": {"activity": 1.0, "travel": -0.4},
    "snowboarding": {"activity": 1.0, "travel": -0.4},

    # Nightlife / Social / Urban Excitement
    "electronic music": {"social": 0.7, "noise": 0.7, "activity": 0.4},
    "nightlife": {"social": 0.9, "noise": 0.8, "activity": 0.4},
    "cocktail bars": {"social": 0.7, "noise": 0.4, "space": -0.3},
    "raves": {"social": 0.8, "noise": 0.9},
    "hip hop": {"social": 0.5, "noise": 0.5},
    "house music": {"social": 0.6, "noise": 0.6},
    "techno": {"social": 0.6, "noise": 0.7},
    "festivals": {"social": 0.9, "noise": 0.8, "travel": -0.4},
    "pop music": {"social": 0.6, "noise": 0.5},
    "fashion week": {"social": 0.7, "space": -0.4},

    # Relaxed / Cozy / Introvert / Contemplative
    "reading": {"activity": -0.8, "noise": -0.8, "social": -0.5},
    "indie film": {"activity": -0.4, "noise": -0.5, "social": -0.3},
    "ambient music": {"activity": -0.7, "noise": -0.9, "social": -0.4},
    "lo-fi": {"activity": -0.6, "noise": -0.7, "social": -0.3},
    "gaming": {"activity": -0.7, "noise": 0.2, "social": -0.4, "space": -0.2},
    "board games": {"activity": -0.4, "social": 0.5, "noise": 0.2},
    "coffee shops": {"social": 0.3, "noise": -0.2, "activity": -0.2},
    "vinyl records": {"noise": -0.4, "social": -0.2, "activity": -0.3},
    "jazz": {"noise": -0.4, "social": 0.2, "activity": -0.3},
    "tea ceremony": {"activity": -0.6, "noise": -0.8, "social": -0.4},
    "cooking": {"space": 0.3, "activity": -0.2, "social": 0.4},
    "knitting": {"activity": -0.8, "noise": -0.7, "social": -0.5},
    "anime": {"activity": -0.5, "noise": -0.3, "social": -0.3},
    "studio ghibli": {"activity": -0.4, "noise": -0.6, "social": -0.2},
    "a24": {"activity": -0.3, "noise": -0.4, "social": -0.2},
    "indie rock": {"social": 0.2, "noise": 0.2},

    # Travel & Nomadic
    "travel": {"travel": -0.9, "activity": 0.5},
    "backpacking": {"travel": -1.0, "activity": 0.8},
    "boutique hotels": {"travel": -0.7, "social": 0.3},
    "frequent flyer": {"travel": -1.2, "activity": 0.3},
    "digital nomad": {"travel": -1.0, "space": -0.5},

    # Pets & Home
    "gardening": {"space": 0.8, "activity": 0.3, "noise": -0.4},
    "plant care": {"space": 0.4, "noise": -0.5, "activity": -0.3},
    "interior design": {"space": 0.3, "noise": -0.3}
}

LOCATION_CULTURAL_MODIFIERS: Dict[str, Dict[str, float]] = {
    "dense_urban": {"space": -0.8, "social": 0.5, "noise": 0.5},
    "urban": {"space": -0.4, "social": 0.3, "noise": 0.3},
    "suburban": {"space": 0.8, "social": -0.2, "activity": 0.2},
    "rural_nature": {"space": 1.2, "activity": 0.7, "noise": -0.6, "social": -0.5}
}

def detect_location_density(location: str) -> str:
    loc_lower = location.lower()
    dense_keywords = ["manhattan", "brooklyn", "new york", "nyc", "tokyo", "london", "paris", "downtown", "san francisco", "chicago", "seattle"]
    rural_keywords = ["mountains", "rural", "countryside", "farm", "vermont", "montana", "wyoming", "alaska", "cabin", "lake", "woods"]
    suburb_keywords = ["suburb", "suburbs", "county", "valleys", "heights", "estates", "orange county", "plano", "naperville"]

    for k in dense_keywords:
        if k in loc_lower:
            return "dense_urban"
    for k in rural_keywords:
        if k in loc_lower:
            return "rural_nature"
    for k in suburb_keywords:
        if k in loc_lower:
            return "suburban"
    return "urban"

async def fetch_qloo_cultural_insights(interests: List[str], location: str) -> Optional[Dict[str, Any]]:
    """
    Connects to the real Qloo API (/search and /v2/insights).
    Resolves user interests to entity IDs, queries correlated places & brands,
    and extracts cultural lifestyle context.
    """
    if not QLOO_API_KEY:
        return None

    headers = {
        "X-Api-Key": QLOO_API_KEY,
        "Accept": "application/json",
        "User-Agent": "PawVibe/1.0"
    }

    entity_ids = []
    matched_entities = []
    correlated_places = []
    correlated_brands = []
    detected_tags = []

    try:
        async with httpx.AsyncClient(timeout=6.0) as client:
            # 1. Resolve top user interests to Qloo entities
            for item in interests[:4]:
                try:
                    search_url = f"{QLOO_BASE_URL}/search"
                    resp = await client.get(search_url, params={"query": item}, headers=headers)
                    if resp.status_code == 200:
                        results = resp.json().get("results", [])
                        if results:
                            top_entity = results[0]
                            entity_id = top_entity.get("entity_id")
                            name = top_entity.get("name")
                            if entity_id:
                                entity_ids.append(entity_id)
                                matched_entities.append(name)
                except Exception as err:
                    print(f"Error querying Qloo search for '{item}': {err}")

            # 2. If entity IDs found, query Qloo Insights for correlated places & brands
            if entity_ids:
                ent_query = ",".join(entity_ids[:3])

                # Query Places
                try:
                    places_resp = await client.get(
                        f"{QLOO_BASE_URL}/v2/insights",
                        params={
                            "signal.interests.entities": ent_query,
                            "filter.type": "urn:entity:place"
                        },
                        headers=headers
                    )
                    if places_resp.status_code == 200:
                        entities = places_resp.json().get("results", {}).get("entities", [])
                        for p in entities[:4]:
                            place_name = p.get("name")
                            if place_name:
                                correlated_places.append(place_name)
                            for t in p.get("tags", []):
                                t_name = t.get("name")
                                if t_name and t_name not in detected_tags:
                                    detected_tags.append(t_name)
                except Exception as e:
                    print(f"Error fetching place insights: {e}")

                # Query Brands
                try:
                    brands_resp = await client.get(
                        f"{QLOO_BASE_URL}/v2/insights",
                        params={
                            "signal.interests.entities": ent_query,
                            "filter.type": "urn:entity:brand"
                        },
                        headers=headers
                    )
                    if brands_resp.status_code == 200:
                        entities = brands_resp.json().get("results", {}).get("entities", [])
                        for b in entities[:4]:
                            brand_name = b.get("name")
                            if brand_name:
                                correlated_brands.append(brand_name)
                            for t in b.get("tags", []):
                                t_name = t.get("name")
                                if t_name and t_name not in detected_tags:
                                    detected_tags.append(t_name)
                except Exception as e:
                    print(f"Error fetching brand insights: {e}")

            if matched_entities or correlated_places or correlated_brands:
                return {
                    "matched_entities": matched_entities,
                    "correlated_places": correlated_places,
                    "correlated_brands": correlated_brands,
                    "detected_tags": detected_tags[:8],
                    "live_connected": True
                }

    except Exception as e:
        print(f"Qloo API insights failed: {e}. Falling back to internal taste engine.")

    return None

def synthesize_lifestyle_vector(
    interests: List[str],
    location: str,
    routine: Dict[str, Any],
    qloo_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Computes a 5D Lifestyle Vector [1.0 to 5.0]:
    - activity: 1 (couch potato) to 5 (extreme endurance / trail runner)
    - space: 1 (studio) to 5 (spacious house with yard)
    - social: 1 (solitary sanctuary) to 5 (bustling host / party butterfly)
    - travel: 1 (always traveling / away often) to 5 (homebody / remote routine)
    - noise: 1 (pin-drop quiet) to 5 (vibrant / high noise tolerance)
    """

    # 1. Baseline from living setup & routine
    home_type = routine.get("home_type", "apartment")
    home_space_map = {
        "studio": 1.5,
        "apartment": 2.5,
        "townhouse": 3.5,
        "house_yard": 4.8
    }
    base_space = home_space_map.get(home_type, 2.5)

    work_style = routine.get("work_style", "hybrid")
    # Higher travel score = pet gets more at-home companionship (less user absence)
    work_travel_map = {
        "remote": 4.8,
        "hybrid": 3.6,
        "in_office": 2.4
    }
    base_travel = work_travel_map.get(work_style, 3.5)

    travel_frequency = routine.get("travel_frequency", "moderate")
    travel_penalty_map = {
        "rarely": 0.5,
        "moderate": 0.0,
        "frequent": -1.2
    }
    base_travel += travel_penalty_map.get(travel_frequency, 0.0)

    weekend_vibe = routine.get("weekend_vibe", "chill_creative")
    weekend_map = {
        "outdoors_active": {"activity": 4.2, "social": 3.6, "noise": 3.2},
        "social_nightlife": {"activity": 3.4, "social": 4.6, "noise": 4.3},
        "chill_creative": {"activity": 2.4, "social": 2.8, "noise": 2.4},
        "cozy_homebody": {"activity": 1.8, "social": 2.2, "noise": 1.8}
    }
    weekend_defaults = weekend_map.get(weekend_vibe, weekend_map["chill_creative"])
    base_activity = weekend_defaults["activity"]
    base_social = weekend_defaults["social"]
    base_noise = weekend_defaults["noise"]

    noise_pref = routine.get("noise_tolerance", "moderate")
    noise_pref_map = {
        "quiet": -0.8,
        "moderate": 0.0,
        "bustling": 0.8
    }
    base_noise += noise_pref_map.get(noise_pref, 0.0)

    # 2. Modulate with Location Density
    loc_density = detect_location_density(location)
    loc_mod = LOCATION_CULTURAL_MODIFIERS.get(loc_density, {})
    base_space += loc_mod.get("space", 0.0)
    base_social += loc_mod.get("social", 0.0)
    base_noise += loc_mod.get("noise", 0.0)
    base_activity += loc_mod.get("activity", 0.0)

    # 3. Modulate with Cultural Interests
    applied_affinities = []
    accumulated_mods = {"activity": 0.0, "space": 0.0, "social": 0.0, "travel": 0.0, "noise": 0.0}

    for item in interests:
        item_clean = item.lower().strip()
        matched = False
        for taste_key, mods in CULTURAL_TASTE_MODIFIERS.items():
            if taste_key in item_clean or item_clean in taste_key:
                matched = True
                applied_affinities.append(taste_key.title())
                for dim, delta in mods.items():
                    accumulated_mods[dim] += delta * 0.4
                break
        if not matched:
            # General keyword heuristics
            if any(w in item_clean for w in ["run", "gym", "climb", "hike", "bike", "sport", "fitness", "yoga"]):
                accumulated_mods["activity"] += 0.35
                applied_affinities.append("Athletic & Fitness")
            elif any(w in item_clean for w in ["art", "film", "book", "read", "indie", "museum", "write", "music"]):
                accumulated_mods["activity"] -= 0.2
                accumulated_mods["noise"] -= 0.25
                applied_affinities.append("Arts & Humanities")
            elif any(w in item_clean for w in ["club", "party", "drink", "cocktail", "bar", "rave", "dining"]):
                accumulated_mods["social"] += 0.4
                accumulated_mods["noise"] += 0.3
                applied_affinities.append("Nightlife & Dining")

    # Ingest Qloo Live API cultural data if available
    qloo_source = "qloo_live_api" if qloo_data else "qloo_cultural_taste_engine"
    correlated_notes = []

    if qloo_data:
        matched = qloo_data.get("matched_entities", [])
        places = qloo_data.get("correlated_places", [])
        brands = qloo_data.get("correlated_brands", [])
        tags = qloo_data.get("detected_tags", [])

        if matched:
            correlated_notes.append(f"Recognized: {', '.join(matched[:2])}")
        if brands:
            correlated_notes.append(f"Affinities: {', '.join(brands[:2])}")
        if places:
            correlated_notes.append(f"Places: {', '.join(places[:2])}")

        for t in tags:
            t_lower = t.lower()
            if any(k in t_lower for k in ["park", "nature", "outdoor", "adventure", "trail"]):
                accumulated_mods["activity"] += 0.3
                accumulated_mods["space"] += 0.2
                applied_affinities.append(t)
            elif any(k in t_lower for k in ["tranquil", "quiet", "relaxing", "historic", "museum", "art"]):
                accumulated_mods["noise"] -= 0.3
                accumulated_mods["activity"] -= 0.2
                applied_affinities.append(t)
            elif any(k in t_lower for k in ["lively", "nightlife", "bar", "cocktail", "trendy", "central"]):
                accumulated_mods["social"] += 0.35
                accumulated_mods["noise"] += 0.3
                applied_affinities.append(t)

    # Sum and clamp to [1.0, 5.0]
    final_activity = max(1.0, min(5.0, round(base_activity + accumulated_mods["activity"], 2)))
    final_space = max(1.0, min(5.0, round(base_space + accumulated_mods["space"], 2)))
    final_social = max(1.0, min(5.0, round(base_social + accumulated_mods["social"], 2)))
    final_travel = max(1.0, min(5.0, round(base_travel + accumulated_mods["travel"], 2)))
    final_noise = max(1.0, min(5.0, round(base_noise + accumulated_mods["noise"], 2)))

    # Cultural Archetype & Narrative Synthesizer
    archetype = "Balanced Explorer"
    if final_activity >= 4.2 and final_space >= 3.5:
        archetype = "High-Alpine Trail Warrior"
    elif final_activity <= 2.2 and final_social >= 3.8:
        archetype = "Urban Socialite & Cafe Connoisseur"
    elif final_activity <= 2.2 and final_noise <= 2.5:
        archetype = "Contemplative Sanctuary Creator"
    elif final_social >= 4.2 and final_noise >= 3.8:
        archetype = "Energetic Host & Culture Lover"
    elif final_space <= 2.2 and final_travel >= 4.0:
        archetype = "Devoted Urban Remote Companion"
    elif final_activity >= 3.8:
        archetype = "Dynamic Active Mover"

    qloo_note_str = f" [Qloo Live: {' | '.join(correlated_notes)}]" if correlated_notes else ""
    narrative = (
        f"Your affinity for {', '.join(interests[:3]) if interests else 'creative pursuits'} "
        f"paired with your {home_type.replace('_', ' ')} living in {location or 'your neighborhood'} "
        f"places you in the '{archetype}' profile. You register an activity rhythm of "
        f"{final_activity}/5 and a home-presence level of {final_travel}/5.{qloo_note_str}"
    )

    return {
        "lifestyle_vector": {
            "activity": final_activity,
            "space": final_space,
            "social": final_social,
            "travel": final_travel,
            "noise": final_noise
        },
        "cultural_profile": {
            "archetype": archetype,
            "location_density": loc_density,
            "affinities_detected": list(dict.fromkeys(applied_affinities))[:6],
            "correlated_context": correlated_notes,
            "narrative": narrative,
            "qloo_source": qloo_source
        }
    }
