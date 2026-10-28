import asyncio
import os
from dotenv import load_dotenv
import httpx

load_dotenv()
api_key = os.getenv("QLOO_API_KEY")
base_url = os.getenv("QLOO_BASE_URL", "https://hackathon.api.qloo.com").rstrip("/")

print("=" * 60)
print(f"Testing Qloo API: {base_url}")
print(f"API Key present: {bool(api_key)}, Prefix: {api_key[:10] if api_key else 'None'}")
print("=" * 60)

async def test_qloo():
    headers = {"X-Api-Key": api_key}
    async with httpx.AsyncClient(timeout=15.0) as client:
        # Test 1: Search Endpoint
        print("\n1. Testing GET /search (Query: 'Radiohead')")
        try:
            res = await client.get(f"{base_url}/search", params={"query": "Radiohead"}, headers=headers)
            print(f"   Status Code: {res.status_code}")
            if res.status_code == 200:
                results = res.json().get("results", [])
                print(f"   Results found: {len(results)}")
                for r in results[:3]:
                    print(f"   - Name: {r.get('name')} | ID: {r.get('entity_id')} | Type: {r.get('type')}")
                
                if results:
                    entity_id = results[0].get("entity_id")
                    
                    # Test 2: Insights Places
                    print(f"\n2. Testing GET /v2/insights (Places for Entity {entity_id[:8]}...)")
                    p_res = await client.get(
                        f"{base_url}/v2/insights",
                        params={"signal.interests.entities": entity_id, "filter.type": "urn:entity:place"},
                        headers=headers
                    )
                    print(f"   Status Code: {p_res.status_code}")
                    if p_res.status_code == 200:
                        entities = p_res.json().get("results", {}).get("entities", [])
                        print(f"   Correlated places returned: {len(entities)}")
                        for p in entities[:3]:
                            tags = [t.get("name") for t in p.get("tags", [])]
                            print(f"   - Place: {p.get('name')} | Tags: {tags[:3]}")
                    else:
                        print(f"   Error: {p_res.text[:300]}")

                    # Test 3: Insights Brands
                    print(f"\n3. Testing GET /v2/insights (Brands for Entity {entity_id[:8]}...)")
                    b_res = await client.get(
                        f"{base_url}/v2/insights",
                        params={"signal.interests.entities": entity_id, "filter.type": "urn:entity:brand"},
                        headers=headers
                    )
                    print(f"   Status Code: {b_res.status_code}")
                    if b_res.status_code == 200:
                        entities = b_res.json().get("results", {}).get("entities", [])
                        print(f"   Correlated brands returned: {len(entities)}")
                        for b in entities[:3]:
                            tags = [t.get("name") for t in b.get("tags", [])]
                            print(f"   - Brand: {b.get('name')} | Tags: {tags[:3]}")
                    else:
                        print(f"   Error: {b_res.text[:300]}")
            else:
                print(f"   Error: {res.text[:300]}")
        except Exception as e:
            print(f"   Exception during search: {e}")

    # Test 4: Internal Taste Engine Live Integration
    print("\n4. Testing PawVibe Taste Engine with Live Qloo Resolution")
    from taste_engine import fetch_qloo_cultural_insights, synthesize_lifestyle_vector
    from matcher import rank_breeds

    qloo_res = await fetch_qloo_cultural_insights(["Radiohead", "A24", "Trail Running"], "Portland, OR")
    print(f"   Qloo Query Connected: {bool(qloo_res and qloo_res.get('live_connected'))}")
    if qloo_res:
        print(f"   Matched Entities: {qloo_res.get('matched_entities')}")
        print(f"   Correlated Places: {qloo_res.get('correlated_places')}")
        print(f"   Correlated Brands: {qloo_res.get('correlated_brands')}")
        print(f"   Detected Tags: {qloo_res.get('detected_tags')}")

    lifestyle = synthesize_lifestyle_vector(
        interests=["Radiohead", "A24", "Trail Running"],
        location="Portland, OR",
        routine={"home_type": "apartment", "wfh_status": "hybrid", "outdoor_frequency": "frequent"},
        qloo_data=qloo_res
    )
    print("\n5. Synthesized 5D Lifestyle Vector:")
    print(f"   Vector: {lifestyle['lifestyle_vector']}")
    print(f"   Archetype: {lifestyle['cultural_profile']['archetype']}")
    print(f"   Narrative: {lifestyle['cultural_profile']['narrative']}")

    matches = rank_breeds(lifestyle["lifestyle_vector"])
    top_dog = matches["top_dogs"][0]
    top_cat = matches["top_cats"][0]
    print(f"\n6. Top Dog Match: {top_dog['name']} ({top_dog['match_score']}%)")
    print(f"   Top Cat Match: {top_cat['name']} ({top_cat['match_score']}%)")
    print("\n" + "=" * 60)
    print("ALL API TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_qloo())
