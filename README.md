# PawVibe — Qloo Taste & Lifestyle Pet Breed Matchmaker 🐾

> **Bridging Cultural Taste to Canine & Feline Compatibility** using Qloo's Taste-to-Lifestyle correlation intelligence and 5D Euclidean vector matching.

---

## 🌟 Overview & Concept

Qloo models correlations across cultural affinities (music, film, dining, travel, fashion, books, and hobbies) and real-world behavioral routines. While Qloo does not natively catalog animal genetics, **PawVibe uses Qloo as a cultural-to-lifestyle translation engine**:

1. **Cultural Signal Ingestion**: Collects non-PII lifestyle cues (favorite entertainment, fitness habits, neighborhood density, and work schedule).
2. **5D Lifestyle Vector Synthesis**: Synthesizes a calibrated vector across 5 normalized dimensions:
   - **Activity Level** (1.0 = relaxed/reading $\rightarrow$ 5.0 = marathon/trail running)
   - **Living Space** (1.0 = compact studio $\rightarrow$ 5.0 = spacious house with fenced acreage)
   - **Social Exposure** (1.0 = quiet sanctuary $\rightarrow$ 5.0 = lively host / dinner parties)
   - **Home Presence / Routine** (1.0 = frequent travel / long shifts $\rightarrow$ 5.0 = 100% remote / rarely away)
   - **Noise & Vibe Tolerance** (1.0 = pin-drop quiet $\rightarrow$ 5.0 = bustling urban liveliness)
3. **Trait Matching Engine**: Calculates weighted Euclidean distance against a curated trait matrix of **24 distinct Dog and Cat breeds**:
   $$D(b) = \sqrt{\sum_{i=1}^5 w_i \cdot (L_i - T_{b,i})^2}$$
   $$\text{Match \%} = \max\left(50, \left(1 - \frac{D(b)}{D_{\max}}\right) \times 100\right)$$
4. **Interactive Visual Dashboard**: Renders dynamic Canvas radar charts comparing the user's lifestyle profile against breed trait requirements, accompanied by custom "Why It Fits Your Vibe" narratives.

---

## 🚀 Running the Application

### 1. Requirements
- Python 3.10+
- Installed packages: `fastapi`, `uvicorn`, `httpx` (all included)

### 2. Start the Server
```bash
python run.py
```
Open **`http://localhost:8080`** in any web browser.

---

## 🔑 Connecting Your Live Qloo API Key

The application works **100% out-of-the-box** using its internal cultural correlation engine modeling Qloo's taste-graph correlations.

To connect your live Qloo developer account:
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Insert your Qloo API key:
   ```ini
   QLOO_API_KEY=your_actual_qloo_key_here
   QLOO_BASE_URL=https://api.qloo.com/v2
   ```
3. Restart the server. The header badge will dynamically illuminate as **"Qloo Live API Connected"**!

---

## 🐕 Curated Breeds Supported
- **Dogs**: Labrador Retriever, French Bulldog, Border Collie, Shiba Inu, Cavalier King Charles Spaniel, Golden Retriever, Italian Greyhound, Australian Shepherd, Pembroke Welsh Corgi, Standard Poodle, Dachshund, Basset Hound, Samoyed, Whippet.
- **Cats**: Bengal, Ragdoll, Siamese, British Shorthair, Sphynx, Maine Coon, Russian Blue, Scottish Fold, Abyssinian, Persian.
