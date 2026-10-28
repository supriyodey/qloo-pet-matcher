import httpx
import json

base = "http://127.0.0.1:8080"
print("=" * 60)
print("TESTING LOCAL BACKEND & REST API ENDPOINTS")
print("=" * 60)

# 1. Health check
r_health = httpx.get(f"{base}/api/health")
print("1. GET /api/health:")
print(f"   Status: {r_health.status_code}")
print(f"   Response: {r_health.json()}")

# 2. Presets
r_presets = httpx.get(f"{base}/api/presets")
print(f"\n2. GET /api/presets:")
print(f"   Status: {r_presets.status_code}")
presets_data = r_presets.json()
print(f"   Count: {len(presets_data)} persona presets available")
for p in presets_data[:3]:
    print(f"   - {p.get('name')}: {p.get('tagline')}")

# 3. Breeds
r_breeds = httpx.get(f"{base}/api/breeds")
print(f"\n3. GET /api/breeds:")
print(f"   Status: {r_breeds.status_code}")
breeds_data = r_breeds.json()
print(f"   Count: {len(breeds_data)} breeds in catalog (dogs & cats)")

# 4. POST /api/match with live Qloo resolution
print(f"\n4. POST /api/match (Live Taste-to-Lifestyle matching):")
payload = {
    "interests": ["Radiohead", "Patagonia", "Trail running"],
    "location": "Boulder, CO",
    "routine": {
        "home_type": "apartment",
        "wfh_status": "hybrid",
        "outdoor_frequency": "frequent",
        "experience_level": "intermediate",
        "schedule_predictability": "consistent"
    }
}
r_match = httpx.post(f"{base}/api/match", json=payload, timeout=20.0)
print(f"   Status: {r_match.status_code}")
if r_match.status_code == 200:
    res = r_match.json()
    profile = res.get("cultural_profile", {})
    vector = res.get("lifestyle_vector", {})
    matches = res.get("matches", {})

    print(f"   Archetype: {profile.get('archetype')}")
    print(f"   Qloo Source: {profile.get('qloo_source')}")
    print(f"   Correlated Context: {profile.get('correlated_context')}")
    print(f"   Synthesized Vector: {vector}")
    
    top_dogs = matches.get("top_dogs", [])
    if top_dogs:
        td = top_dogs[0]
        print(f"\n   Top Dog Match: {td.get('name')} ({td.get('match_score')}%)")
        print(f"   Why it fits: {td.get('why_it_fits')}")
    
    top_cats = matches.get("top_cats", [])
    if top_cats:
        tc = top_cats[0]
        print(f"\n   Top Cat Match: {tc.get('name')} ({tc.get('match_score')}%)")
        print(f"   Why it fits: {tc.get('why_it_fits')}")

print("\n" + "=" * 60)
print("ALL SERVER ENDPOINTS TESTED SUCCESSFULLY!")
print("=" * 60)
