import os
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import taste_engine
import matcher

app = FastAPI(
    title="Qloo Pet Breed Matchmaker API",
    description="Cultural taste-to-lifestyle layer mapping interests and routine to Dog & Cat breed traits",
    version="1.0.0"
)

# Enable CORS for local dev / testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RoutineInput(BaseModel):
    work_style: str = Field(default="hybrid", description="remote, hybrid, or in_office")
    home_type: str = Field(default="apartment", description="studio, apartment, townhouse, or house_yard")
    travel_frequency: str = Field(default="moderate", description="rarely, moderate, or frequent")
    weekend_vibe: str = Field(default="chill_creative", description="outdoors_active, social_nightlife, chill_creative, or cozy_homebody")
    noise_tolerance: str = Field(default="moderate", description="quiet, moderate, or bustling")

class MatchRequest(BaseModel):
    interests: List[str] = Field(default_factory=list, description="Cultural interests, bands, films, hobbies, sports")
    location: str = Field(default="New York, NY", description="Neighborhood, city, or ZIP")
    routine: RoutineInput = Field(default_factory=RoutineInput)
    custom_vector_override: Optional[Dict[str, float]] = Field(default=None, description="Optional manual fine-tuning for 5D vector")

PRESETS = [
    {
        "id": "alpine-adventurer",
        "title": "The Alpine Trail Explorer",
        "badge": "Active & Outdoors",
        "location": "Boulder, CO",
        "interests": ["Trail Running", "National Parks", "Hiking", "Patagonia", "Camping", "Rock Climbing"],
        "routine": {
            "work_style": "hybrid",
            "home_type": "house_yard",
            "travel_frequency": "rarely",
            "weekend_vibe": "outdoors_active",
            "noise_tolerance": "moderate"
        }
    },
    {
        "id": "cozy-remote-creative",
        "title": "The Cozy Remote Creative",
        "badge": "Quiet & Contemplative",
        "location": "Portland, OR",
        "interests": ["Indie Film", "A24", "Lo-Fi", "Coffee Shops", "Reading", "Vinyl Records", "Plant Care"],
        "routine": {
            "work_style": "remote",
            "home_type": "apartment",
            "travel_frequency": "rarely",
            "weekend_vibe": "chill_creative",
            "noise_tolerance": "quiet"
        }
    },
    {
        "id": "urban-socialite",
        "title": "The Soho Loft Socialite",
        "badge": "Lively & Urban",
        "location": "SoHo, Manhattan",
        "interests": ["Electronic Music", "Cocktail Bars", "Fashion Week", "Nightlife", "Art Galleries"],
        "routine": {
            "work_style": "hybrid",
            "home_type": "studio",
            "travel_frequency": "moderate",
            "weekend_vibe": "social_nightlife",
            "noise_tolerance": "bustling"
        }
    },
    {
        "id": "suburban-zen-host",
        "title": "The Relaxed Garden Host",
        "badge": "Harmonious & Spacious",
        "location": "Austin, TX (Suburbs)",
        "interests": ["Gardening", "Cooking", "Jazz", "Board Games", "Cycling"],
        "routine": {
            "work_style": "hybrid",
            "home_type": "house_yard",
            "travel_frequency": "rarely",
            "weekend_vibe": "chill_creative",
            "noise_tolerance": "moderate"
        }
    }
]

@app.get("/api/health")
def health_check():
    breeds = matcher.load_breeds()
    dogs_count = sum(1 for b in breeds if b["species"] == "dog")
    cats_count = sum(1 for b in breeds if b["species"] == "cat")
    return {
        "status": "online",
        "qloo_api_configured": bool(taste_engine.QLOO_API_KEY),
        "total_breeds": len(breeds),
        "dogs_count": dogs_count,
        "cats_count": cats_count
    }

@app.get("/api/presets")
def get_presets():
    return PRESETS

@app.get("/api/breeds")
def get_all_breeds():
    return matcher.load_breeds()

@app.post("/api/match")
async def match_lifestyle(req: MatchRequest):
    # 1. Attempt Qloo API insights
    qloo_insights = await taste_engine.fetch_qloo_cultural_insights(req.interests, req.location)

    # 2. Synthesize 5D lifestyle vector
    synthesis = taste_engine.synthesize_lifestyle_vector(
        interests=req.interests,
        location=req.location,
        routine=req.routine.model_dump(),
        qloo_data=qloo_insights
    )

    lifestyle_vector = synthesis["lifestyle_vector"]

    # 3. Apply manual slider overrides if provided
    if req.custom_vector_override:
        for dim, val in req.custom_vector_override.items():
            if dim in lifestyle_vector and isinstance(val, (int, float)):
                lifestyle_vector[dim] = max(1.0, min(5.0, round(float(val), 2)))

    # 4. Rank dog and cat breeds
    ranked = matcher.rank_breeds(lifestyle_vector)

    return {
        "lifestyle_vector": lifestyle_vector,
        "cultural_profile": synthesis["cultural_profile"],
        "top_dogs": ranked["top_dogs"],
        "runner_up_dogs": ranked["runner_up_dogs"],
        "top_cats": ranked["top_cats"],
        "runner_up_cats": ranked["runner_up_cats"],
        "dimension_labels": matcher.DIMENSION_LABELS
    }

# Ensure frontend directory exists before static mount
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
