// PawVibe - Luxury Atelier Client Logic
// Strictly Beige, White, Grey, and Gold Palette with Flat Icons & Real Breed Photography

const state = {
  currentStep: 1,
  selectedInterests: new Set(["Indie Film", "Reading", "Coffee Shops", "Plant Care", "Lo-Fi"]),
  customTags: [],
  location: "Brooklyn, NY",
  routine: {
    home_type: "apartment",
    work_style: "remote",
    weekend_vibe: "chill_creative",
    noise_tolerance: "quiet",
    travel_frequency: "rarely"
  },
  activeTab: "dogs",
  currentResults: null,
  presets: []
};

// Flat SVG icons helpers
const SVG_ICONS = {
  dog: `<svg viewBox="0 0 24 24"><path d="M4.5 10.5C3.67 10.5 3 9.83 3 9s.67-1.5 1.5-1.5S6 8.17 6 9s-.67 1.5-1.5 1.5zm15 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm-7.5-6C8.91 4.5 6.75 6.66 6.75 9.75c0 3.86 3.75 8.25 5.25 9.75 1.5-1.5 5.25-5.89 5.25-9.75C17.25 6.66 15.09 4.5 12 4.5z"/></svg>`,
  cat: `<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-4 7c.83 0 1.5.67 1.5 1.5S8.83 12 8 12s-1.5-.67-1.5-1.5S7.17 9 8 9zm8 0c.83 0 1.5.67 1.5 1.5S16.83 12 16 12s-1.5-.67-1.5-1.5.67-1.5 1.5-1.5zm-4 8c-2.33 0-4.31-1.46-5.11-3.5h10.22c-.8 2.04-2.78 3.5-5.11 3.5z"/></svg>`,
  spark: `<svg viewBox="0 0 24 24"><path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/></svg>`,
  tag: `<svg viewBox="0 0 24 24"><path d="M21.41 11.58l-9-9C12.05 2.22 11.55 2 11 2H4c-1.1 0-2 .9-2 2v7c0 .55.22 1.05.59 1.42l9 9c.36.36.86.58 1.41.58.55 0 1.05-.22 1.41-.59l7-7c.37-.36.59-.86.59-1.41 0-.55-.23-1.06-.59-1.42zM5.5 7C4.67 7 4 6.33 4 5.5S4.67 4 5.5 4 7 4.67 7 5.5 6.33 7 5.5 7z"/></svg>`,
  check: `<svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>`
};

document.addEventListener("DOMContentLoaded", () => {
  initApiStatus();
  initPresets();
  initTagToggles();
  initCustomTagInput();
  initRadioCards();
  initStepNavigation();
  initSynthesisTrigger();
  initTunerModal();
  initResultsTabs();
});

// Check API health & update status badge
async function initApiStatus() {
  const badgeText = document.getElementById("api-status-text");
  try {
    const res = await fetch("/api/health");
    if (res.ok) {
      const data = await res.json();
      if (data.qloo_api_configured) {
        badgeText.textContent = "Qloo Live API Connected";
      } else {
        badgeText.textContent = "Qloo Cultural Engine Active";
      }
    }
  } catch (e) {
    badgeText.textContent = "Offline Cultural Engine";
  }
}

// Fetch and render presets
async function initPresets() {
  const grid = document.getElementById("preset-grid");
  try {
    const res = await fetch("/api/presets");
    if (res.ok) {
      state.presets = await res.json();
      renderPresets();
    }
  } catch (e) {
    console.warn("Could not load presets from server", e);
  }
}

function renderPresets() {
  const grid = document.getElementById("preset-grid");
  if (!grid || !state.presets.length) return;

  grid.innerHTML = state.presets.map((p, idx) => `
    <div class="preset-card ${idx === 1 ? 'active' : ''}" data-preset-id="${p.id}">
      <span class="preset-badge">${p.badge}</span>
      <h4>${p.title}</h4>
      <p>${p.location} • ${p.interests.slice(0, 3).join(", ")}</p>
    </div>
  `).join("");

  grid.querySelectorAll(".preset-card").forEach(card => {
    card.addEventListener("click", () => {
      grid.querySelectorAll(".preset-card").forEach(c => c.classList.remove("active"));
      card.classList.add("active");
      const presetId = card.getAttribute("data-preset-id");
      applyPreset(presetId);
    });
  });
}

function applyPreset(presetId) {
  const preset = state.presets.find(p => p.id === presetId);
  if (!preset) return;

  state.location = preset.location;
  const locInput = document.getElementById("input-location");
  if (locInput) locInput.value = preset.location;

  state.selectedInterests.clear();
  preset.interests.forEach(i => state.selectedInterests.add(i));

  document.querySelectorAll(".tag-pill").forEach(pill => {
    const val = pill.getAttribute("data-val");
    if (state.selectedInterests.has(val)) {
      pill.classList.add("selected");
    } else {
      pill.classList.remove("selected");
    }
  });

  state.routine = { ...preset.routine };
  syncRadioCardsWithState();
}

// Tag toggling
function initTagToggles() {
  document.querySelectorAll(".tag-pill").forEach(pill => {
    const val = pill.getAttribute("data-val");
    if (state.selectedInterests.has(val)) {
      pill.classList.add("selected");
    }
    pill.addEventListener("click", () => {
      if (state.selectedInterests.has(val)) {
        state.selectedInterests.delete(val);
        pill.classList.remove("selected");
      } else {
        state.selectedInterests.add(val);
        pill.classList.add("selected");
      }
    });
  });
}

// Custom Tag Input
function initCustomTagInput() {
  const input = document.getElementById("custom-tag-input");
  const btn = document.getElementById("btn-add-tag");
  const container = document.getElementById("custom-tags-container");

  function addTag() {
    const val = input.value.trim();
    if (!val) return;
    if (!state.selectedInterests.has(val)) {
      state.selectedInterests.add(val);
      const pill = document.createElement("span");
      pill.className = "tag-pill selected";
      pill.setAttribute("data-val", val);
      pill.innerHTML = `
        <svg viewBox="0 0 24 24"><path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/></svg>
        ${val}
        <span style="font-size:0.75rem; margin-left:4px; opacity:0.6;">✕</span>
      `;
      pill.addEventListener("click", () => {
        state.selectedInterests.delete(val);
        pill.remove();
      });
      container.appendChild(pill);
      input.value = "";
    }
  }

  btn.addEventListener("click", addTag);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      addTag();
    }
  });
}

// Radio Card Selector
function initRadioCards() {
  document.querySelectorAll(".radio-card").forEach(card => {
    card.addEventListener("click", () => {
      const groupName = card.getAttribute("data-group");
      const input = card.querySelector("input");
      if (!groupName || !input) return;

      document.querySelectorAll(`.radio-card[data-group="${groupName}"]`).forEach(c => {
        c.classList.remove("selected");
      });
      card.classList.add("selected");
      input.checked = true;

      state.routine[groupName] = input.value;
    });
  });
}

function syncRadioCardsWithState() {
  for (const [group, val] of Object.entries(state.routine)) {
    document.querySelectorAll(`.radio-card[data-group="${group}"]`).forEach(card => {
      const input = card.querySelector("input");
      if (input && input.value === val) {
        card.classList.add("selected");
        input.checked = true;
      } else {
        card.classList.remove("selected");
      }
    });
  }
}

// Multi-step Wizard Navigation
function initStepNavigation() {
  const steps = [1, 2, 3];
  
  function goToStep(num) {
    state.currentStep = num;
    steps.forEach(s => {
      const stepEl = document.getElementById(`step-${s}`);
      const tabEl = document.getElementById(`tab-step-${s}`);
      if (s === num) {
        stepEl.classList.add("active");
        tabEl.classList.add("active");
      } else {
        stepEl.classList.remove("active");
        tabEl.classList.remove("active");
        if (s < num) tabEl.classList.add("completed");
      }
    });
    window.scrollTo({ top: document.getElementById("quiz-card").offsetTop - 20, behavior: "smooth" });
  }

  document.getElementById("btn-next-1")?.addEventListener("click", () => goToStep(2));
  document.getElementById("btn-back-2")?.addEventListener("click", () => goToStep(1));
  document.getElementById("btn-next-2")?.addEventListener("click", () => goToStep(3));
  document.getElementById("btn-back-3")?.addEventListener("click", () => goToStep(2));

  document.getElementById("tab-step-1")?.addEventListener("click", () => goToStep(1));
  document.getElementById("tab-step-2")?.addEventListener("click", () => goToStep(2));
  document.getElementById("tab-step-3")?.addEventListener("click", () => goToStep(3));
}

// Synthesis Trigger & Animation
function initSynthesisTrigger() {
  const btn = document.getElementById("btn-synthesize");
  const loader = document.getElementById("loader-box");
  const loaderText = document.getElementById("loader-text");
  const resultsContainer = document.getElementById("results-container");
  const quizCard = document.getElementById("quiz-card");

  btn.addEventListener("click", async () => {
    const locInput = document.getElementById("input-location");
    if (locInput) state.location = locInput.value.trim() || "New York, NY";

    quizCard.style.display = "none";
    loader.style.display = "block";
    resultsContainer.style.display = "none";

    const messages = [
      "Analyzing cultural signals with Qloo Taste Intelligence...",
      "Synthesizing 5D Lifestyle Vector (Energy, Habitat, Routine)...",
      "Calculating Weighted Euclidean Trait Distances across 24 Breeds...",
      "Fetching breed imagery and ranking top compatibility profiles..."
    ];

    let msgIdx = 0;
    const interval = setInterval(() => {
      msgIdx = (msgIdx + 1) % messages.length;
      loaderText.textContent = messages[msgIdx];
    }, 450);

    try {
      const payload = {
        interests: Array.from(state.selectedInterests),
        location: state.location,
        routine: state.routine
      };

      const res = await fetch("/api/match", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      clearInterval(interval);

      if (!res.ok) throw new Error("Match computation failed");
      const data = await res.json();
      state.currentResults = data;

      setTimeout(() => {
        loader.style.display = "none";
        renderResults(data);
        resultsContainer.style.display = "block";
        window.scrollTo({ top: resultsContainer.offsetTop - 30, behavior: "smooth" });
      }, 500);

    } catch (err) {
      clearInterval(interval);
      loader.style.display = "none";
      quizCard.style.display = "block";
      alert("Error calculating matches: " + err.message);
    }
  });

  document.getElementById("btn-restart")?.addEventListener("click", () => {
    resultsContainer.style.display = "none";
    quizCard.style.display = "block";
    window.scrollTo({ top: quizCard.offsetTop - 20, behavior: "smooth" });
  });
}

// Render Results Dashboard
function renderResults(data) {
  const { cultural_profile, lifestyle_vector } = data;

  // Profile Header
  document.getElementById("res-archetype").textContent = cultural_profile.archetype;
  document.getElementById("res-narrative").textContent = cultural_profile.narrative;

  // Affinities & Qloo Live Signals
  const affWrap = document.getElementById("res-affinities");
  const liveChips = (cultural_profile.correlated_context || []).map(c => 
    `<span class="affinity-chip" style="border-color:var(--gold-primary); color:var(--gold-deep); font-weight:600;">✦ ${c}</span>`
  );
  const detectedChips = (cultural_profile.affinities_detected || []).map(a => 
    `<span class="affinity-chip">${a}</span>`
  );
  affWrap.innerHTML = [...liveChips, ...detectedChips].join("");

  // 5D Lifestyle Vector Bars
  const barsContainer = document.getElementById("vector-metric-bars");
  const dimDefs = [
    { key: "activity", label: "Activity Level", val: lifestyle_vector.activity },
    { key: "space", label: "Living Space", val: lifestyle_vector.space },
    { key: "social", label: "Social Exposure", val: lifestyle_vector.social },
    { key: "travel", label: "Home Presence", val: lifestyle_vector.travel },
    { key: "noise", label: "Vibe / Noise", val: lifestyle_vector.noise }
  ];

  barsContainer.innerHTML = dimDefs.map(d => `
    <div class="metric-row">
      <span style="font-size:0.8rem; min-width:90px; color:var(--text-secondary);">${d.label}</span>
      <div class="metric-bar-wrap">
        <div class="metric-bar-fill" style="width: ${(d.val / 5.0) * 100}%"></div>
      </div>
      <span style="font-weight:700; font-size:0.8rem; min-width:32px; text-align:right; color:var(--gold-deep);">${d.val.toFixed(1)}</span>
    </div>
  `).join("");

  // Sync Tuner Sliders
  dimDefs.forEach(d => {
    const range = document.getElementById(`range-${d.key}`);
    const valText = document.getElementById(`val-${d.key}`);
    if (range && valText) {
      range.value = d.val;
      valText.textContent = d.val.toFixed(1);
    }
  });

  renderActiveBreeds();
}

// Render Breeds based on active tab
function renderActiveBreeds() {
  if (!state.currentResults) return;
  const grid = document.getElementById("breeds-card-grid");
  const runnerGrid = document.getElementById("runner-grid");
  const { top_dogs, top_cats, runner_up_dogs, runner_up_cats } = state.currentResults;

  let breedsToShow = [];
  let runnersToShow = [];

  if (state.activeTab === "dogs") {
    breedsToShow = top_dogs;
    runnersToShow = runner_up_dogs;
  } else if (state.activeTab === "cats") {
    breedsToShow = top_cats;
    runnersToShow = runner_up_cats;
  } else {
    // Both combined
    breedsToShow = [top_dogs[0], top_cats[0], top_dogs[1], top_cats[1]];
    runnersToShow = [...runner_up_dogs.slice(0, 2), ...runner_up_cats.slice(0, 2)];
  }

  // Render cards with REAL PHOTOGRAPHY in suggestion box
  grid.innerHTML = breedsToShow.map((b, idx) => `
    <article class="breed-card ${idx === 0 ? 'top-pick' : ''}">
      <!-- Real Breed Photo in Suggestion Box -->
      <div class="breed-image-box">
        <img 
          src="${b.image_url || 'https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=800&q=80'}" 
          alt="${b.name}" 
          class="breed-img" 
          loading="lazy"
          onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=800&q=80';"
        >
        <span class="species-tag-badge">
          ${b.species === 'dog' ? SVG_ICONS.dog : SVG_ICONS.cat}
          ${b.species === 'dog' ? 'Canine' : 'Feline'}
        </span>
      </div>

      <div class="card-top">
        <div class="breed-header">
          <span class="breed-badge">${b.badge || (b.species === 'dog' ? 'Canine Pick' : 'Feline Pick')}</span>
          <h3>${b.name}</h3>
        </div>
        <div class="match-score-badge">
          <span class="score-num">${b.match_score}%</span>
          <span class="score-label">Lifestyle Fit</span>
        </div>
      </div>

      <!-- Trait Radar Visualizer -->
      <div class="radar-container">
        <canvas class="radar-canvas" id="radar-${b.id}"></canvas>
        <div class="radar-legend">
          <div class="legend-item"><span class="dot-user"></span> Your Profile</div>
          <div class="legend-item"><span class="dot-breed"></span> ${b.name} Traits</div>
        </div>
      </div>

      <div class="card-content">
        <p class="tagline">“${b.tagline}”</p>
        
        <div class="why-fits-box">
          <div class="why-title">
            ${SVG_ICONS.spark}
            Why It Fits Your Vibe
          </div>
          <ul class="why-list">
            ${b.why_it_fits.map(r => `<li>${r}</li>`).join("")}
          </ul>
        </div>

        <div class="card-specs">
          <div class="spec-item">
            <span class="spec-k">Size</span>
            <span class="spec-v">${b.size || 'Medium'}</span>
          </div>
          <div class="spec-item">
            <span class="spec-k">Grooming</span>
            <span class="spec-v">${b.grooming || 'Moderate'}</span>
          </div>
          <div class="spec-item">
            <span class="spec-k">Hypoallergenic</span>
            <span class="spec-v">${b.hypoallergenic ? 'Yes' : 'No'}</span>
          </div>
        </div>
      </div>
    </article>
  `).join("");

  // Draw Radar Charts
  breedsToShow.forEach(b => {
    drawRadarChart(`radar-${b.id}`, b.radar_data.user_values, b.radar_data.breed_values);
  });

  // Runner Ups (with thumbnail images)
  runnerGrid.innerHTML = runnersToShow.map(r => `
    <div class="runner-card">
      <img 
        src="${r.image_url || 'https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=400&q=80'}" 
        alt="${r.name}" 
        class="runner-thumb" 
        loading="lazy"
        onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=400&q=80';"
      >
      <div class="runner-info">
        <h4>${r.name}</h4>
        <p>${r.badge || r.tagline}</p>
      </div>
      <div class="runner-score">${r.match_score}%</div>
    </div>
  `).join("");
}

// Draw HTML5 Canvas Radar Chart (Beige, White, Grey, Gold)
function drawRadarChart(canvasId, userValues, breedValues) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();

  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;
  ctx.scale(dpr, dpr);

  const width = rect.width;
  const height = rect.height;
  const centerX = width / 2;
  const centerY = height / 2;
  const radius = Math.min(centerX, centerY) - 28;
  const labels = ["Activity", "Space", "Social", "Routine", "Vibe"];
  const numAxes = labels.length;

  ctx.clearRect(0, 0, width, height);

  // Background Web Grid (Concentric polygons in subtle grey)
  const rings = [0.33, 0.66, 1.0];
  ctx.strokeStyle = "#E7E2D8";
  ctx.lineWidth = 1;

  rings.forEach(ringScale => {
    ctx.beginPath();
    for (let i = 0; i < numAxes; i++) {
      const angle = (Math.PI * 2 / numAxes) * i - Math.PI / 2;
      const x = centerX + Math.cos(angle) * (radius * ringScale);
      const y = centerY + Math.sin(angle) * (radius * ringScale);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.stroke();
  });

  // Axis Lines & Text Labels
  ctx.font = "500 10px 'Plus Jakarta Sans', sans-serif";
  ctx.fillStyle = "#7A746B";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";

  for (let i = 0; i < numAxes; i++) {
    const angle = (Math.PI * 2 / numAxes) * i - Math.PI / 2;
    const x = centerX + Math.cos(angle) * radius;
    const y = centerY + Math.sin(angle) * radius;

    // Line
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(x, y);
    ctx.stroke();

    // Text Label slightly pushed outwards
    const labelX = centerX + Math.cos(angle) * (radius + 18);
    const labelY = centerY + Math.sin(angle) * (radius + 18);
    ctx.fillText(labels[i], labelX, labelY);
  }

  // Draw Polygon Helper
  function drawPolygon(values, strokeColor, fillColor, dotColor) {
    ctx.beginPath();
    for (let i = 0; i < numAxes; i++) {
      const val = Math.max(1, Math.min(5, values[i] || 3));
      const valNorm = (val - 1) / 4;
      const currentRadius = radius * (0.2 + valNorm * 0.8);
      const angle = (Math.PI * 2 / numAxes) * i - Math.PI / 2;
      const x = centerX + Math.cos(angle) * currentRadius;
      const y = centerY + Math.sin(angle) * currentRadius;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.fillStyle = fillColor;
    ctx.fill();
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = 2;
    ctx.stroke();

    // Draw vertex dots
    for (let i = 0; i < numAxes; i++) {
      const val = Math.max(1, Math.min(5, values[i] || 3));
      const valNorm = (val - 1) / 4;
      const currentRadius = radius * (0.2 + valNorm * 0.8);
      const angle = (Math.PI * 2 / numAxes) * i - Math.PI / 2;
      const x = centerX + Math.cos(angle) * currentRadius;
      const y = centerY + Math.sin(angle) * currentRadius;
      ctx.beginPath();
      ctx.arc(x, y, 3, 0, Math.PI * 2);
      ctx.fillStyle = dotColor;
      ctx.fill();
    }
  }

  // Draw Breed Traits Polygon (Charcoal Grey)
  drawPolygon(breedValues, "#54504A", "rgba(84, 80, 74, 0.16)", "#54504A");

  // Draw User Lifestyle Polygon (Warm Metallic Gold)
  drawPolygon(userValues, "#C5A059", "rgba(197, 160, 89, 0.24)", "#A7843D");
}

// Results Tabs Switching (Dogs / Cats / Both)
function initResultsTabs() {
  const tabs = ["dogs", "cats", "both"];
  tabs.forEach(tab => {
    document.getElementById(`tab-${tab}`)?.addEventListener("click", () => {
      tabs.forEach(t => document.getElementById(`tab-${t}`)?.classList.remove("active"));
      document.getElementById(`tab-${tab}`)?.classList.add("active");
      state.activeTab = tab;
      renderActiveBreeds();
    });
  });
}

// 5D Vector Tuner Modal
function initTunerModal() {
  const modal = document.getElementById("tuner-modal");
  const openBtn = document.getElementById("btn-open-tuner");
  const closeBtn = document.getElementById("btn-close-tuner");
  const applyBtn = document.getElementById("btn-apply-tuning");

  openBtn?.addEventListener("click", () => modal.classList.add("active"));
  closeBtn?.addEventListener("click", () => modal.classList.remove("active"));
  modal?.addEventListener("click", (e) => {
    if (e.target === modal) modal.classList.remove("active");
  });

  ["activity", "space", "social", "travel", "noise"].forEach(dim => {
    const range = document.getElementById(`range-${dim}`);
    const valText = document.getElementById(`val-${dim}`);
    range?.addEventListener("input", () => {
      valText.textContent = parseFloat(range.value).toFixed(1);
    });
  });

  applyBtn?.addEventListener("click", async () => {
    const customOverride = {
      activity: parseFloat(document.getElementById("range-activity").value),
      space: parseFloat(document.getElementById("range-space").value),
      social: parseFloat(document.getElementById("range-social").value),
      travel: parseFloat(document.getElementById("range-travel").value),
      noise: parseFloat(document.getElementById("range-noise").value)
    };

    modal.classList.remove("active");

    const payload = {
      interests: Array.from(state.selectedInterests),
      location: state.location,
      routine: state.routine,
      custom_vector_override: customOverride
    };

    try {
      const res = await fetch("/api/match", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        const data = await res.json();
        state.currentResults = data;
        renderResults(data);
      }
    } catch (e) {
      alert("Error applying custom vector: " + e.message);
    }
  });
}
