import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Initialize Presentation in 16:9 Widescreen
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]  # Blank slide

# Color Palette: Luxury Atelier (Beige, White, Grey, Gold)
COLOR_BEIGE_BG = RGBColor(248, 245, 240)
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_GOLD = RGBColor(197, 160, 89)
COLOR_GOLD_LIGHT = RGBColor(223, 191, 119)
COLOR_GOLD_DEEP = RGBColor(167, 132, 61)
COLOR_CHARCOAL = RGBColor(33, 31, 29)
COLOR_GREY_BODY = RGBColor(84, 80, 74)
COLOR_GREY_MUTED = RGBColor(122, 116, 107)
COLOR_GREY_BORDER = RGBColor(231, 226, 216)
COLOR_CARD_BEIGE = RGBColor(243, 239, 232)

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BEIGE_BG

def add_header(slide, category_tag, title_text, subtitle_text=None):
    # Category tag
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.5), Inches(0.35))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = category_tag.upper()
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = COLOR_GOLD_DEEP

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.5), Inches(0.7))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_CHARCOAL

    if subtitle_text:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.5), Inches(0.45))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle_text
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = COLOR_GREY_BODY

def add_card(slide, left, top, width, height, bg_color=COLOR_WHITE, border_color=COLOR_GREY_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1)
    return shape

# ==============================================================================
# SLIDE 1: Title Slide (Cover)
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)

# Main Cover Card
add_card(s1, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5), COLOR_WHITE, COLOR_GOLD)

# Brand Logo
logo_img_path = os.path.join(os.path.dirname(__file__), "frontend", "logo.jpg")
if os.path.exists(logo_img_path):
    s1.shapes.add_picture(logo_img_path, Inches(8.8), Inches(1.8), Inches(2.7), Inches(2.7))

# Brand Badge
tag1 = s1.shapes.add_textbox(Inches(1.8), Inches(1.6), Inches(6.8), Inches(0.4))
tf1 = tag1.text_frame
p1 = tf1.paragraphs[0]
p1.text = "QLOO AGENTIC & CULTURAL AI HACKATHON 2026"
p1.font.size = Pt(11)
p1.font.bold = True
p1.font.color.rgb = COLOR_GOLD_DEEP

# Title
t1 = s1.shapes.add_textbox(Inches(1.8), Inches(2.0), Inches(6.8), Inches(1.2))
tf_t1 = t1.text_frame
p_t1 = tf_t1.paragraphs[0]
p_t1.text = "PawVibe"
p_t1.font.size = Pt(46)
p_t1.font.bold = True
p_t1.font.color.rgb = COLOR_CHARCOAL

# Subtitle
sub1 = s1.shapes.add_textbox(Inches(1.8), Inches(3.1), Inches(6.8), Inches(0.8))
tf_sub1 = sub1.text_frame
p_sub1 = tf_sub1.paragraphs[0]
p_sub1.text = "Bridging Cultural Taste Intelligence to Canine & Feline Compatibility"
p_sub1.font.size = Pt(17)
p_sub1.font.color.rgb = COLOR_GOLD_DEEP
p_sub1.font.bold = True

desc1 = s1.shapes.add_textbox(Inches(1.8), Inches(3.9), Inches(6.8), Inches(0.8))
tf_desc1 = desc1.text_frame
tf_desc1.word_wrap = True
p_desc1 = tf_desc1.paragraphs[0]
p_desc1.text = "“Your tastes define your routine. Your routine chooses your pet.”\nTurning music, cinema, dining, and neighborhood rhythms into predictive 5D pet lifestyle vectors."
p_desc1.font.size = Pt(12)
p_desc1.font.italic = True
p_desc1.font.color.rgb = COLOR_GREY_BODY

# Feature highlights bar at bottom of card
feat_box = s1.shapes.add_textbox(Inches(1.8), Inches(4.9), Inches(9.5), Inches(0.8))
tf_feat = feat_box.text_frame
p_feat = tf_feat.paragraphs[0]
p_feat.text = "• Live Qloo API (Entity Search & Cross-Domain Insights)   • 5D Euclidean Matching   • 24 Curated Dog & Cat Breeds"
p_feat.font.size = Pt(11)
p_feat.font.bold = True
p_feat.font.color.rgb = COLOR_GREY_MUTED

s1.notes_slide.notes_text_frame.text = (
    "SPEAKER SCRIPT (30s):\n"
    "Hello judges! Today, we are presenting PawVibe — an innovative application that solves a real-world multi-billion dollar problem "
    "using Qloo’s Taste Intelligence API. While Qloo models cultural taste correlations across music, film, fashion, and places, "
    "PawVibe uses Qloo as a predictive 'Taste-to-Lifestyle' translation layer to match people with the right dog and cat breeds."
)

# ==============================================================================
# SLIDE 2: The Problem (The Pet Mismatch Crisis)
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)
add_header(s2, "The Real-World Problem", "The Pet-Lifestyle Mismatch Crisis", "Why millions of animal adoptions fail despite good intentions")

# 3 Stat Cards
# Card 1: Surrenders
add_card(s2, Inches(0.8), Inches(2.0), Inches(3.6), Inches(4.8), COLOR_WHITE, COLOR_GREY_BORDER)
c1_box = s2.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(3.2), Inches(4.4))
tf_c1 = c1_box.text_frame
tf_c1.word_wrap = True
p = tf_c1.paragraphs[0]
p.text = "6.5 Million"
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = COLOR_GOLD_DEEP

p = tf_c1.add_paragraph()
p.text = "Pets in US Shelters Annually\n"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_CHARCOAL

p = tf_c1.add_paragraph()
p.text = "Over 6.5 million companion animals enter shelters each year. Up to 47% of rehoming decisions stem from lifestyle incompatibilities: energy mismatches, unexpected noise, space constraints, or travel frequency."
p.font.size = Pt(11)
p.font.color.rgb = COLOR_GREY_BODY

# Card 2: The Blindspot
add_card(s2, Inches(4.8), Inches(2.0), Inches(3.6), Inches(4.8), COLOR_WHITE, COLOR_GREY_BORDER)
c2_box = s2.shapes.add_textbox(Inches(5.0), Inches(2.2), Inches(3.2), Inches(4.4))
tf_c2 = c2_box.text_frame
tf_c2.word_wrap = True
p = tf_c2.paragraphs[0]
p.text = "The Flawed Choice"
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = COLOR_CHARCOAL

p = tf_c2.add_paragraph()
p.text = "Adoption by Aesthetics\n"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_GOLD_DEEP

p = tf_c2.add_paragraph()
p.text = "Owners typically adopt based on social media trends or cute looks (e.g. an apartment worker buying a working Australian Shepherd or Border Collie). People rarely quantify their daily energy, soundscape, and habitat until it's too late."
p.font.size = Pt(11)
p.font.color.rgb = COLOR_GREY_BODY

# Card 3: The Gap
add_card(s2, Inches(8.8), Inches(2.0), Inches(3.7), Inches(4.8), COLOR_WHITE, COLOR_GOLD)
c3_box = s2.shapes.add_textbox(Inches(9.0), Inches(2.2), Inches(3.3), Inches(4.4))
tf_c3 = c3_box.text_frame
tf_c3.word_wrap = True
p = tf_c3.paragraphs[0]
p.text = "The Opportunity"
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = COLOR_GOLD_DEEP

p = tf_c3.add_paragraph()
p.text = "Taste Predicts Lifestyle\n"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_CHARCOAL

p = tf_c3.add_paragraph()
p.text = "People struggle to evaluate their own physical routine in numbers. However, they easily know their favorite music artists, films, clothing brands, dining spots, and hobbies. These cultural tastes hold the hidden blueprint of how they live."
p.font.size = Pt(11)
p.font.color.rgb = COLOR_GREY_BODY

s2.notes_slide.notes_text_frame.text = (
    "SPEAKER SCRIPT (45s):\n"
    "Every year, 6.5 million companion animals enter shelters. Almost half of surrenders happen because owners pick pets based on looks "
    "rather than daily lifestyle compatibility. A remote worker in a studio adopts a high-drive working dog, or an endurance athlete adopts "
    "a sedentary cat. People cannot objectively calculate their lifestyle metrics in a boring questionnaire, but they know their favorite "
    "bands, films, and brands. That is where Qloo comes in."
)

# ==============================================================================
# SLIDE 3: The Solution: Qloo as a Taste-to-Lifestyle Layer
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)
add_header(s3, "The Core Breakthrough", "Qloo as a Taste-to-Lifestyle Translation Layer", "How cultural graph affinities map to biological breed traits")

# Left Column: The Problem Qloo Solves
add_card(s3, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8), COLOR_WHITE, COLOR_GREY_BORDER)
left_box = s3.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.0), Inches(4.4))
tf_l = left_box.text_frame
tf_l.word_wrap = True

p = tf_l.paragraphs[0]
p.text = "Why Traditional Methods Fail"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = COLOR_CHARCOAL

bullet_points_l = [
    ("No Biological Data in Qloo:", "Qloo doesn't index animal genetics or pet breeds directly."),
    ("Inaccurate Self-Reporting:", "Users in standard pet quizzes overstate their activity and understate their travel."),
    ("The Missing Link:", "There has never been a bridge connecting cultural consumer taste with physical pet breed temperaments.")
]

for title, desc in bullet_points_l:
    p = tf_l.add_paragraph()
    p.text = f"• {title} "
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD_DEEP
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = COLOR_GREY_BODY

# Right Column: The PawVibe Architecture
add_card(s3, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8), COLOR_CARD_BEIGE, COLOR_GOLD)
right_box = s3.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.1), Inches(4.4))
tf_r = right_box.text_frame
tf_r.word_wrap = True

p = tf_r.paragraphs[0]
p.text = "The PawVibe Translation Engine"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = COLOR_CHARCOAL

bullet_points_r = [
    ("1. Ingest Cultural Taste:", "Favorite bands (Radiohead), cinema (A24), fashion, outdoor brands (Patagonia), and neighborhood."),
    ("2. Cross-Domain Extraction:", "Qloo's Live Insights API outputs correlated places, brands, and venue tags (Tranquil, Historic, Parks, Nightlife)."),
    ("3. 5D Vector Synthesis:", "Transforms affinities into calibrated 1-5 vectors across: Activity, Space, Social, Routine, and Noise."),
    ("4. Mathematical Trait Distance:", "Computes weighted Euclidean distance against curated trait profiles for 24 Dog and Cat breeds.")
]

for title, desc in bullet_points_r:
    p = tf_r.add_paragraph()
    p.text = f"{title} "
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_CHARCOAL
    run = p.add_run()
    run.text = desc
    run.font.color.rgb = COLOR_GREY_BODY

s3.notes_slide.notes_text_frame.text = (
    "SPEAKER SCRIPT (45s):\n"
    "Qloo doesn't have a 'dog breeds' endpoint. But what Qloo DOES have is the world's most sophisticated cultural correlation graph. "
    "When a user likes Radiohead, A24 movies, and trail running, Qloo's Insights API tells us what places they visit and what brands they buy. "
    "PawVibe ingests these cultural correlations and synthesizes a calibrated 5D Lifestyle Vector, which we then mathematically match against "
    "canine and feline breed traits."
)

# ==============================================================================
# SLIDE 4: Live Qloo API Integration
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)
add_header(s4, "Technical Architecture", "Live Qloo Hackathon API Integration", "Real-time queries to https://hackathon.api.qloo.com via X-Api-Key")

# Left Column: Code / Endpoint Details
add_card(s4, Inches(0.8), Inches(2.0), Inches(5.5), Inches(4.8), COLOR_WHITE, COLOR_GREY_BORDER)
api_box = s4.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.1), Inches(4.4))
tf_api = api_box.text_frame
tf_api.word_wrap = True

p = tf_api.paragraphs[0]
p.text = "Two-Tier Qloo Query Engine"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = COLOR_CHARCOAL

steps = [
    ("Step 1: Entity Resolution (/search)",
     "User signals (e.g. 'Radiohead', 'Patagonia') are queried via GET /search?query={item}.\n"
     "Returns verified Qloo URN entity IDs (e.g. 70CAE5BF-2F4C... type: urn:entity:artist)."),
    ("Step 2: Places Insights (/v2/insights)",
     "Queries GET /v2/insights with signal.interests.entities={entity_ids}&filter.type=urn:entity:place.\n"
     "Extracts place archetypes & tags: Tranquil, Historic, Nature conservation, Park."),
    ("Step 3: Brands Insights (/v2/insights)",
     "Queries filter.type=urn:entity:brand to retrieve correlated lifestyle brands (e.g. Blinkist, Patagonia, Albion Fit).")
]

for title, desc in steps:
    p = tf_api.add_paragraph()
    p.text = title
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD_DEEP
    p = tf_api.add_paragraph()
    p.text = desc
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_GREY_BODY

# Right Column: Screenshot of Live API Results
screenshot_path_live = r'C:\Users\devsu\.gemini\antigravity-ide\brain\2c16193e-1849-4439-b486-f2c89587f49a\qloo_pet_results_1791987968196.png'
if os.path.exists(screenshot_path_live):
    add_card(s4, Inches(6.6), Inches(2.0), Inches(5.9), Inches(4.8), COLOR_WHITE, COLOR_GOLD)
    s4.shapes.add_picture(screenshot_path_live, Inches(6.8), Inches(2.2), Inches(5.5), Inches(4.4))
else:
    add_card(s4, Inches(6.6), Inches(2.0), Inches(5.9), Inches(4.8), COLOR_CARD_BEIGE, COLOR_GOLD)

s4.notes_slide.notes_text_frame.text = (
    "SPEAKER SCRIPT (40s):\n"
    "Let's look under the hood. PawVibe is not a static prototype — it connects in real time to hackathon.api.qloo.com. "
    "First, we resolve cultural terms into Qloo entity IDs. Then, we query the Insights API for correlated places and brands. "
    "You can see in the screenshot right here: when the user enters creative tastes, Qloo extracts affinities like Blinkist and TED Talks, "
    "and places tagged as 'Tranquil' and 'Historic'. That live cultural context is directly injected into our matching vector."
)

# ==============================================================================
# SLIDE 5: The Mathematical Model & 5D Vector Matching
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)
add_header(s5, "The Science Behind The Match", "Weighted Euclidean Trait Distance Modeling", "How the 5D Lifestyle Vector matches canine and feline profiles")

# Left Column: The 5 Dimensions
add_card(s5, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8), COLOR_WHITE, COLOR_GREY_BORDER)
dim_box = s5.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.0), Inches(4.4))
tf_d = dim_box.text_frame
tf_d.word_wrap = True

p = tf_d.paragraphs[0]
p.text = "The 5 Lifestyle Dimensions (Scale: 1.0 - 5.0)"
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = COLOR_CHARCOAL

dims = [
    ("🏃 Activity Level (Weight: 1.25):", "Couch & book relaxation (1.0) vs. marathon trail running (5.0)."),
    ("🏡 Living Space (Weight: 1.20):", "Micro-studio loft (1.0) vs. multi-acre fenced suburban house (5.0)."),
    ("🤝 Social Exposure (Weight: 1.00):", "Solitary home sanctuary (1.0) vs. vibrant party host / busy venues (5.0)."),
    ("⏱️ Home Routine (Weight: 1.00):", "Frequent flyer / long commutes (1.0) vs. 100% remote homebody (5.0)."),
    ("🔊 Noise & Vibe (Weight: 0.90):", "Pin-drop quiet required (1.0) vs. bustling, vocal household (5.0).")
]

for title, desc in dims:
    p = tf_d.add_paragraph()
    p.text = title + " "
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD_DEEP
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = COLOR_GREY_BODY

# Right Column: Formula & Algorithm
add_card(s5, Inches(6.7), Inches(2.0), Inches(5.8), Inches(4.8), COLOR_WHITE, COLOR_GOLD)
math_box = s5.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.2), Inches(4.4))
tf_m = math_box.text_frame
tf_m.word_wrap = True

p = tf_m.paragraphs[0]
p.text = "The Matching Equation"
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = COLOR_CHARCOAL

p = tf_m.add_paragraph()
p.text = "1. Weighted Euclidean Distance:"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = COLOR_GOLD_DEEP

p = tf_m.add_paragraph()
p.text = "D(b) = √ [ Σ w_i · ( Lifestyle_i  -  Breed_Traits_b,i )² ]"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_CHARCOAL

p = tf_m.add_paragraph()
p.text = "2. Normalized Match Compatibility:"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = COLOR_GOLD_DEEP

p = tf_m.add_paragraph()
p.text = "Match % = max( 50, (1 - D(b) / D_max) × 100 )"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_CHARCOAL

p = tf_m.add_paragraph()
p.text = "3. Explainable AI Divergence Analysis:"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = COLOR_GOLD_DEEP

p = tf_m.add_paragraph()
p.text = "The engine compares the user's vector to the breed's traits, isolates the closest alignments, and generates personalized 'Why It Fits Your Vibe' explanations (e.g., 'Matches your peaceful schedule while accommodating your studio space')."
p.font.size = Pt(10)
p.font.color.rgb = COLOR_GREY_BODY

s5.notes_slide.notes_text_frame.text = (
    "SPEAKER SCRIPT (40s):\n"
    "We don't use arbitrary keyword matching. We use a formal mathematical distance model. "
    "We weight Activity and Living Space slightly higher because animal welfare is most at risk when an active pet is confined in a small space. "
    "The engine computes weighted Euclidean distance across the 5 dimensions, calculates a normalized compatibility score, "
    "and isolates the exact trait overlaps to provide clear, explainable AI justifications."
)

# ==============================================================================
# SLIDE 6: Product Showcase (Visual Design & Radar Charts)
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)
add_header(s6, "Product Showcase", "Luxury Atelier UI & Real-Time Visualization", "Designed with warm beige, white, grey, gold, and HTML5 Canvas radar charts")

# Screenshot 1: Dog Cards with Real Photos & Radar Charts
screenshot_dogs = r'C:\Users\devsu\.gemini\antigravity-ide\brain\2c16193e-1849-4439-b486-f2c89587f49a\dog_suggestions_with_photos_1791361452373.png'
if os.path.exists(screenshot_dogs):
    add_card(s6, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.8), COLOR_WHITE, COLOR_GREY_BORDER)
    s6.shapes.add_picture(screenshot_dogs, Inches(0.95), Inches(2.15), Inches(5.4), Inches(4.5))

# Screenshot 2: Landing Page & Presets
screenshot_landing = r'C:\Users\devsu\.gemini\antigravity-ide\brain\2c16193e-1849-4439-b486-f2c89587f49a\landing_page_1791361371332.png'
if os.path.exists(screenshot_landing):
    add_card(s6, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8), COLOR_WHITE, COLOR_GOLD)
    s6.shapes.add_picture(screenshot_landing, Inches(6.95), Inches(2.15), Inches(5.4), Inches(4.5))

s6.notes_slide.notes_text_frame.text = (
    "SPEAKER SCRIPT (35s):\n"
    "Here is the user experience. We designed PawVibe with an editorial, high-end aesthetic inspired by luxury lifestyle magazines. "
    "Notice the flat SVG icons, warm beige canvas, and verified high-resolution photography. "
    "Each recommendation box features an interactive HTML5 Canvas radar chart overlaying the user's lifestyle vector in gold "
    "against the breed's required traits in charcoal grey, giving prospective owners an instant visual comparison."
)

# ==============================================================================
# SLIDE 7: Market Opportunity & Business Model
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7)
add_header(s7, "Business & Market Opportunity", "$150 Billion Industry Meets Cultural AI", "How PawVibe drives revenue while improving animal welfare")

# 3 Market & Revenue Columns
add_card(s7, Inches(0.8), Inches(2.0), Inches(3.6), Inches(4.8), COLOR_WHITE, COLOR_GREY_BORDER)
m1_box = s7.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(3.2), Inches(4.4))
tf_m1 = m1_box.text_frame
tf_m1.word_wrap = True
p = tf_m1.paragraphs[0]
p.text = "$150B+"
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = COLOR_GOLD_DEEP

p = tf_m1.add_paragraph()
p.text = "Global Pet Market\n"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_CHARCOAL

p = tf_m1.add_paragraph()
p.text = "Over 86 million US households own pets. Pet parents spend more on premium nutrition, ethical adoptions, and lifestyle gear than ever before. PawVibe enters as an indispensable discovery gateway at the exact moment of adoption decision."
p.font.size = Pt(11)
p.font.color.rgb = COLOR_GREY_BODY

# Column 2: Revenue Streams
add_card(s7, Inches(4.8), Inches(2.0), Inches(3.6), Inches(4.8), COLOR_WHITE, COLOR_GREY_BORDER)
m2_box = s7.shapes.add_textbox(Inches(5.0), Inches(2.2), Inches(3.2), Inches(4.4))
tf_m2 = m2_box.text_frame
tf_m2.word_wrap = True
p = tf_m2.paragraphs[0]
p.text = "Monetization"
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = COLOR_CHARCOAL

p = tf_m2.add_paragraph()
p.text = "High-Margin Channels\n"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_GOLD_DEEP

bullets_monet = [
    "Adoption & Rescue Referral Fees with verified ethical breeders and shelter networks.",
    "Targeted Affiliate Commerce: Qloo brand affinities recommend tailored gear (e.g. Patagonia owner → Ruffwear outdoor harness).",
    "Pet Insurance & Vet Plans integrated at the point of match."
]
for b in bullets_monet:
    p = tf_m2.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_GREY_BODY

# Column 3: Impact & ESG
add_card(s7, Inches(8.8), Inches(2.0), Inches(3.7), Inches(4.8), COLOR_CARD_BEIGE, COLOR_GOLD)
m3_box = s7.shapes.add_textbox(Inches(9.0), Inches(2.2), Inches(3.3), Inches(4.4))
tf_m3 = m3_box.text_frame
tf_m3.word_wrap = True
p = tf_m3.paragraphs[0]
p.text = "Social Impact"
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = COLOR_GOLD_DEEP

p = tf_m3.add_paragraph()
p.text = "Preventing Surrenders\n"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_CHARCOAL

p = tf_m3.add_paragraph()
p.text = "By steering adopters away from mismatched breeds and towards pets whose energy and space needs fit their real lives, PawVibe directly targets the root cause of shelter rehoming. Measurable ESG impact combined with venture-scale economics."
p.font.size = Pt(11)
p.font.color.rgb = COLOR_GREY_BODY

s7.notes_slide.notes_text_frame.text = (
    "SPEAKER SCRIPT (40s):\n"
    "The pet economy is a $150 billion dollar market. But beyond the commercial opportunity, PawVibe has immense social impact. "
    "Because we ingest Qloo brand affinities, we can also recommend personalized gear, food subscriptions, and pet insurance. "
    "And by preventing incompatible adoptions before they happen, we keep animals in loving homes and out of shelters."
)

# ==============================================================================
# SLIDE 8: Why PawVibe Wins & Conclusion
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8)
add_header(s8, "Summary & Vision", "Why PawVibe Wins This Hackathon", "The intersection of cultural AI, animal welfare, and live execution")

# 4 Key Pillars Card
add_card(s8, Inches(0.8), Inches(2.0), Inches(11.733), Inches(4.8), COLOR_WHITE, COLOR_GOLD)
summary_box = s8.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(11.0), Inches(4.4))
tf_s = summary_box.text_frame
tf_s.word_wrap = True

p = tf_s.paragraphs[0]
p.text = "Key Takeaways"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = COLOR_CHARCOAL

takeaways = [
    ("1. Novel & Untapped Application of Qloo:",
     "Most hackathon projects use Qloo for playlist or restaurant recommendations. PawVibe proves that cultural affinities can solve critical behavioral problems in animal welfare and consumer lifestyle."),
    ("2. Fully Built & Tested with Live API:",
     "Not a mock-up. Authenticated against https://hackathon.api.qloo.com, executing live /search and /v2/insights requests, backed by FastAPI and modern HTML5 Canvas visualization."),
    ("3. Luxury Atelier User Experience:",
     "Tailored with a refined Beige, White, Grey, and Gold palette, flat vector iconography, and verified breed photography that wows users at first glance."),
    ("4. Scalable Roadmap:",
     "Expanding from 24 breeds to regional shelter integrations, adoptable pet pet-matching APIs, and multi-pet household dynamics.")
]

for title, desc in takeaways:
    p = tf_s.add_paragraph()
    p.text = title + " "
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD_DEEP
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = COLOR_GREY_BODY

p = tf_s.add_paragraph()
p.text = "\n🐾 Try the live app at: http://localhost:8080   |   Thank You!"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_CHARCOAL

s8.notes_slide.notes_text_frame.text = (
    "SPEAKER SCRIPT (30s):\n"
    "To wrap up: PawVibe stands out because it takes Qloo into a completely fresh, high-impact vertical. "
    "It is fully functional, beautifully designed, and connected to the live Qloo Hackathon API. "
    "Thank you so much, and we'd love to take any questions or show you a live demo!"
)

# Save the presentation
output_pptx_path = r"C:\Users\devsu\.gemini\antigravity-ide\scratch\qloo-pet-matcher\PawVibe_Hackathon_Pitch_Deck.pptx"
try:
    prs.save(output_pptx_path)
    print(f"Presentation saved successfully to: {output_pptx_path}")
except PermissionError:
    alt_path = r"C:\Users\devsu\.gemini\antigravity-ide\scratch\qloo-pet-matcher\PawVibe_Hackathon_Pitch_Deck_v2.pptx"
    prs.save(alt_path)
    print(f"Original file was open in PowerPoint. Saved updated deck with logo to: {alt_path}")
