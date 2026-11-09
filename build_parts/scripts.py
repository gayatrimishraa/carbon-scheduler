JS_SCRIPTS = """
// Embedded Data
const SUMMARY_DATA = __SUMMARY_JSON__;
const CARBON_REPLAY = __CARBON_REPLAY_JSON__;

const FUNCTION_URL = "https://r5ayxprhq2kwb6i6wdbar4o7m40fqrca.lambda-url.ap-south-1.on.aws/";

// State
let secretToken = "";
let selectedLivePolicy = "multi_objective";
let sessionRequests = [];

// Region Constants
const REGIONS = ["ap-south-1", "eu-north-1", "us-east-1"];
const HOME_REGION = "ap-south-1";
const COST_FACTORS = { "us-east-1": 1.00, "eu-north-1": 1.08, "ap-south-1": 1.10 };

// ==================== INITIALIZATION ====================
document.addEventListener("DOMContentLoaded", () => {
  initNavigation();
  initCounters();
  initLiveScheduler();
  initPolicyPlayground();
  initResultsTable();
  updateHourPreview(0);
});

// Navigation & Scroll Spy
function initNavigation() {
  const links = document.querySelectorAll(".nav-links a");
  const sections = document.querySelectorAll("main section");

  window.addEventListener("scroll", () => {
    let current = "";
    sections.forEach(section => {
      const sectionTop = section.offsetTop - 120;
      if (window.scrollY >= sectionTop) {
        current = section.getAttribute("id");
      }
    });

    links.forEach(link => {
      link.classList.remove("active");
      if (link.getAttribute("href") === `#${current}`) {
        link.classList.add("active");
      }
    });
  });
}

// Counter Animations
function initCounters() {
  const counters = document.querySelectorAll(".counter-val");
  counters.forEach(counter => {
    const target = parseFloat(counter.getAttribute("data-target"));
    const duration = 1200;
    const step = target / (duration / 16);
    let current = 0;
    const isFloat = target % 1 !== 0;

    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      counter.innerText = isFloat ? current.toFixed(4) : Math.round(current);
    }, 16);
  });
}

// ==================== LIVE SCHEDULER ====================
function initLiveScheduler() {
  const tokenInput = document.getElementById("secretTokenInput");
  const toggleBtn = document.getElementById("btnToggleToken");
  const policyPills = document.querySelectorAll(".policy-pill");
  const hourSlider = document.getElementById("liveSimHour");
  const executeBtn = document.getElementById("btnExecuteLive");
  const clearHistBtn = document.getElementById("btnClearHistory");

  // Secret token held ONLY in memory
  secretToken = tokenInput.value.trim();
  tokenInput.addEventListener("input", (e) => {
    secretToken = e.target.value.trim();
  });

  toggleBtn.addEventListener("click", () => {
    if (tokenInput.type === "password") {
      tokenInput.type = "text";
      toggleBtn.innerText = "Hide";
    } else {
      tokenInput.type = "password";
      toggleBtn.innerText = "Show";
    }
  });

  policyPills.forEach(pill => {
    pill.addEventListener("click", () => {
      policyPills.forEach(p => p.classList.remove("selected"));
      pill.classList.add("selected");
      selectedLivePolicy = pill.getAttribute("data-policy");
    });
  });

  hourSlider.addEventListener("input", (e) => {
    const h = parseInt(e.target.value);
    document.getElementById("liveHourVal").innerText = h;
    updateHourPreview(h);
  });

  executeBtn.addEventListener("click", handleLiveExecution);
  clearHistBtn.addEventListener("click", clearSessionHistory);
  
  const exportJsonBtn = document.getElementById("btnExportJson");
  if (exportJsonBtn) exportJsonBtn.addEventListener("click", exportHistoryJson);

  const exportCsvBtn = document.getElementById("btnExportCsv");
  if (exportCsvBtn) exportCsvBtn.addEventListener("click", exportHistoryCsv);
}

function updateHourPreview(hour) {
  const hData = CARBON_REPLAY[hour] || { "ap-south-1": 72.5, "eu-north-1": 19.0, "us-east-1": 325.0 };
  const preview = document.getElementById("liveHourCarbonPreview");
  if (preview) {
    preview.innerHTML = `
      <span>ap-south-1: <strong>${hData["ap-south-1"]}</strong> gCO2</span>
      <span>eu-north-1: <strong>${hData["eu-north-1"]}</strong> gCO2</span>
      <span>us-east-1: <strong>${hData["us-east-1"]}</strong> gCO2</span>
    `;
  }
}

async function handleLiveExecution() {
  const token = secretToken;
  const policy = selectedLivePolicy;
  const simHour = parseInt(document.getElementById("liveSimHour").value) || 0;
  const runId = document.getElementById("liveRunId").value.trim() || "web-eval-run";

  const btn = document.getElementById("btnExecuteLive");
  const statusBadge = document.getElementById("liveStatusBadge");
  const resultContainer = document.getElementById("liveResultDisplay");
  const emptyState = document.getElementById("liveEmptyState");
  const errorBox = document.getElementById("liveErrorBox");

  // Validate Token
  if (!token) {
    showError("Authentication Required: Please enter the X-Scheduler-Token before invoking the AWS Lambda Router.");
    return;
  }

  // Set In-Flight UI
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> Invoking AWS Worker...`;
  statusBadge.className = "badge-status running";
  statusBadge.innerHTML = `<span class="spinner" style="width:12px;height:12px;"></span> IN-FLIGHT`;
  errorBox.style.display = "none";

  const startTime = performance.now();

  try {
    const payload = {
      policy: policy,
      sim_hour: simHour,
      run_id: runId
    };

    const response = await fetch(FUNCTION_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-scheduler-token": token,
        "x-secret-token": token
      },
      body: JSON.stringify(payload)
    });

    const clientWallTime = (performance.now() - startTime).toFixed(1);

    if (!response.ok) {
      let errDetail = "";
      try {
        const errJson = await response.json();
        errDetail = errJson.error || JSON.stringify(errJson);
      } catch (e) {
        errDetail = response.statusText || `HTTP ${response.status}`;
      }

      if (response.status === 401) {
        throw new Error(`401 Unauthorized: Invalid secret token. Please verify your token (e.g. 'scheduler-secret-2024').`);
      } else {
        throw new Error(`AWS Lambda returned HTTP ${response.status}: ${errDetail}`);
      }
    }

    const data = await response.json();

    // Render Success
    statusBadge.className = "badge-status success";
    statusBadge.innerText = "200 OK (LIVE AWS RESPONSE)";
    emptyState.style.display = "none";
    resultContainer.style.display = "block";

    renderLiveResult(data, clientWallTime);
    recordSessionRequest(data, clientWallTime, "SUCCESS");

  } catch (err) {
    statusBadge.className = "badge-status error";
    statusBadge.innerText = "ERROR";
    showError(err.message);
    recordSessionRequest({
      request_id: "ERR-" + Date.now().toString(36),
      policy: policy,
      chosen_region: "N/A",
      latency_ms: "N/A",
      est_gco2: "N/A",
      cold_start: "N/A"
    }, (performance.now() - startTime).toFixed(1), "FAILED");
  } finally {
    btn.disabled = false;
    btn.innerHTML = `
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polygon points="5 3 19 12 5 21 5 3"></polygon>
      </svg>
      Invoke Lambda Worker
    `;
  }
}

function showError(msg) {
  const errorBox = document.getElementById("liveErrorBox");
  errorBox.style.display = "block";
  errorBox.innerHTML = `
    <div style="display:flex;align-items:flex-start;gap:0.75rem;">
      <span style="color:#ef4444;font-size:1.2rem;">⚠️</span>
      <div>
        <strong style="color:#f87171;display:block;margin-bottom:0.25rem;">Execution Failed</strong>
        <p style="font-size:0.85rem;color:#cbd5e1;">${msg}</p>
      </div>
    </div>
  `;
}

function renderLiveResult(data, clientWallMs) {
  document.getElementById("resRequestId").innerText = data.request_id || "N/A";
  
  const regEl = document.getElementById("resRegion");
  const regName = data.chosen_region || "N/A";
  let regFlag = "🇮🇳 Mumbai";
  if (regName === "eu-north-1") regFlag = "🇸🇪 Stockholm";
  if (regName === "us-east-1") regFlag = "🇺🇸 N. Virginia";
  regEl.innerHTML = `${regName} <span style="font-size:0.85rem;color:#94a3b8;font-weight:normal;">(${regFlag})</span>`;

  document.getElementById("resLatency").innerText = `${data.latency_ms} ms`;
  document.getElementById("resWallTime").innerText = `Client Wall: ${clientWallMs} ms`;
  document.getElementById("resCO2").innerText = `${data.est_gco2} g`;
  document.getElementById("resCarbonIntensity").innerText = `${data.carbon_intensity} gCO2/kWh`;

  const coldEl = document.getElementById("resColdStart");
  const isCold = String(data.cold_start).toLowerCase() === "true";
  if (isCold) {
    coldEl.className = "badge-pill";
    coldEl.style.background = "rgba(168, 85, 247, 0.2)";
    coldEl.style.color = "#c084fc";
    coldEl.innerText = "COLD START (True)";
  } else {
    coldEl.className = "badge-pill";
    coldEl.style.background = "rgba(16, 185, 129, 0.2)";
    coldEl.style.color = "#34d399";
    coldEl.innerText = "WARM CONTAINER (False)";
  }

  // Scores breakdown
  const scores = data.scores || {};
  renderLiveScores(scores, data.chosen_region);

  // Raw JSON
  document.getElementById("resRawJson").innerText = JSON.stringify(data, null, 2);
}

function renderLiveScores(scores, chosen) {
  const container = document.getElementById("liveScoresContainer");
  if (!scores || Object.keys(scores).length === 0) {
    container.innerHTML = `<p style="font-size:0.8rem;color:#64748b;">No composite score array returned for policy '${selectedLivePolicy}'.</p>`;
    return;
  }

  let html = `<div class="scores-title"><span>Regional Composite Scores</span><span>(Lower score = Preferred)</span></div>`;
  for (const reg of REGIONS) {
    const val = scores[reg] !== undefined ? Number(scores[reg]).toFixed(4) : "0.0000";
    const isChosen = reg === chosen;
    const barWidth = Math.min(100, Math.max(8, Number(val) * 100));
    const barColor = isChosen ? "#10b981" : (reg === "eu-north-1" ? "#38bdf8" : "#f59e0b");

    html += `
      <div class="region-score-row ${isChosen ? 'chosen' : ''}">
        <span style="width:90px;font-family:var(--font-mono);">${reg} ${isChosen ? '★' : ''}</span>
        <div class="score-bar-bg">
          <div class="score-bar-fill" style="width:${barWidth}%;background:${barColor};"></div>
        </div>
        <span style="width:60px;text-align:right;font-family:var(--font-mono);">${val}</span>
      </div>
    `;
  }
  container.innerHTML = html;
}

function recordSessionRequest(data, wallMs, status) {
  const record = {
    time: new Date().toLocaleTimeString(),
    id: data.request_id || "N/A",
    policy: data.policy || selectedLivePolicy,
    region: data.chosen_region || "N/A",
    latency: data.latency_ms || "N/A",
    wall: wallMs,
    co2: data.est_gco2 || "N/A",
    cold: String(data.cold_start),
    status: status
  };

  sessionRequests.unshift(record);
  renderHistoryTable();
}

function renderHistoryTable() {
  const tbody = document.querySelector("#liveHistoryTable tbody");
  const countEl = document.getElementById("histCount");
  const avgLatEl = document.getElementById("histAvgLat");
  const totalCO2El = document.getElementById("histTotalCO2");

  countEl.innerText = sessionRequests.length;

  const validRequests = sessionRequests.filter(r => r.status === "SUCCESS" && !isNaN(parseFloat(r.latency)));
  if (validRequests.length > 0) {
    const avgLat = validRequests.reduce((acc, r) => acc + parseFloat(r.latency), 0) / validRequests.length;
    const totCO2 = validRequests.reduce((acc, r) => acc + parseFloat(r.co2), 0);
    avgLatEl.innerText = `${avgLat.toFixed(1)} ms`;
    totalCO2El.innerText = `${totCO2.toFixed(5)} g`;
  } else {
    avgLatEl.innerText = "0 ms";
    totalCO2El.innerText = "0.0000 g";
  }

  if (sessionRequests.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" style="text-align:center;color:#64748b;padding:1.5rem;">No live requests in current browser session. Execute a request above to record session telemetry.</td></tr>`;
    return;
  }

  tbody.innerHTML = sessionRequests.map(r => `
    <tr>
      <td>${r.time}</td>
      <td style="font-size:0.75rem;color:#38bdf8;">${r.id.substring(0, 13)}...</td>
      <td><span class="policy-box-tag" style="padding:0.1rem 0.4rem;font-size:0.68rem;">${r.policy}</span></td>
      <td><strong>${r.region}</strong></td>
      <td>${r.latency} ms</td>
      <td>${r.co2}</td>
      <td>${r.cold === 'true' ? '<span style="color:#c084fc;">True</span>' : '<span style="color:#34d399;">False</span>'}</td>
      <td>
        <span class="badge-status ${r.status === 'SUCCESS' ? 'success' : 'error'}" style="font-size:0.65rem;padding:0.15rem 0.4rem;">
          ${r.status}
        </span>
      </td>
    </tr>
  `).join("");
}

function clearSessionHistory() {
  sessionRequests = [];
  renderHistoryTable();
}

function exportHistoryJson() {
  if (sessionRequests.length === 0) {
    alert("No session requests to export.");
    return;
  }
  const blob = new Blob([JSON.stringify(sessionRequests, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `carbonflow_session_${Date.now()}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

function exportHistoryCsv() {
  if (sessionRequests.length === 0) {
    alert("No session requests to export.");
    return;
  }
  const headers = ["time", "id", "policy", "region", "latency_ms", "wall_ms", "est_gco2", "cold_start", "status"];
  const rows = sessionRequests.map(r => [
    r.time, r.id, r.policy, r.region, r.latency, r.wall, r.co2, r.cold, r.status
  ]);
  const csvContent = [headers.join(","), ...rows.map(row => row.map(v => `"${v}"`).join(","))].join("\\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `carbonflow_session_${Date.now()}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

// ==================== POLICY PLAYGROUND ====================
let weights = { carbon: 0.40, latency: 0.30, cold: 0.20, cost: 0.10 };
let pgEwmaLatency = { "ap-south-1": 200, "eu-north-1": 650, "us-east-1": 950 };
let pgIdleMinutes = { "ap-south-1": 2, "eu-north-1": 12, "us-east-1": 35 };

function initPolicyPlayground() {
  const sliders = ["carbon", "latency", "cold", "cost"];
  sliders.forEach(s => {
    const el = document.getElementById(`pgW_${s}`);
    el.addEventListener("input", (e) => {
      handleWeightChange(s, parseFloat(e.target.value));
    });
  });

  const hourSlider = document.getElementById("pgHourSlider");
  hourSlider.addEventListener("input", (e) => {
    document.getElementById("pgHourVal").innerText = e.target.value;
    computePlaygroundScores();
  });

  // Region Latency Inputs
  REGIONS.forEach(r => {
    const latInput = document.getElementById(`pgLat_${r}`);
    if (latInput) {
      latInput.addEventListener("input", (e) => {
        pgEwmaLatency[r] = parseFloat(e.target.value) || 200;
        computePlaygroundScores();
      });
    }
    const idleInput = document.getElementById(`pgIdle_${r}`);
    if (idleInput) {
      idleInput.addEventListener("input", (e) => {
        pgIdleMinutes[r] = parseFloat(e.target.value) || 0;
        computePlaygroundScores();
      });
    }
  });

  // Presets
  document.querySelectorAll(".btn-preset").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".btn-preset").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      applyPreset(btn.getAttribute("data-preset"));
    });
  });

  computePlaygroundScores();
}

function handleWeightChange(changedKey, newVal) {
  weights[changedKey] = newVal;
  document.getElementById(`pgW_${changedKey}_val`).innerText = newVal.toFixed(2);

  // Normalize others to sum to 1.0
  const otherKeys = ["carbon", "latency", "cold", "cost"].filter(k => k !== changedKey);
  const remaining = Math.max(0, 1.0 - newVal);
  const currentOtherSum = otherKeys.reduce((acc, k) => acc + weights[k], 0);

  if (currentOtherSum > 0) {
    otherKeys.forEach(k => {
      weights[k] = (weights[k] / currentOtherSum) * remaining;
      document.getElementById(`pgW_${k}`).value = weights[k];
      document.getElementById(`pgW_${k}_val`).innerText = weights[k].toFixed(2);
    });
  } else {
    otherKeys.forEach(k => {
      weights[k] = remaining / 3;
      document.getElementById(`pgW_${k}`).value = weights[k];
      document.getElementById(`pgW_${k}_val`).innerText = weights[k].toFixed(2);
    });
  }

  updateTotalWeightDisplay();
  computePlaygroundScores();
}

function updateTotalWeightDisplay() {
  const sum = Object.values(weights).reduce((a, b) => a + b, 0);
  const el = document.getElementById("pgTotalWeight");
  if (el) {
    el.innerText = sum.toFixed(2);
    el.style.color = Math.abs(sum - 1.0) < 0.01 ? "#10b981" : "#f59e0b";
  }
}

function applyPreset(name) {
  if (name === "default") weights = { carbon: 0.40, latency: 0.30, cold: 0.20, cost: 0.10 };
  else if (name === "eco") weights = { carbon: 0.85, latency: 0.05, cold: 0.05, cost: 0.05 };
  else if (name === "latency") weights = { carbon: 0.05, latency: 0.85, cold: 0.05, cost: 0.05 };
  else if (name === "cold") weights = { carbon: 0.20, latency: 0.20, cold: 0.55, cost: 0.05 };
  else if (name === "cost") weights = { carbon: 0.10, latency: 0.10, cold: 0.10, cost: 0.70 };

  for (const k of ["carbon", "latency", "cold", "cost"]) {
    document.getElementById(`pgW_${k}`).value = weights[k];
    document.getElementById(`pgW_${k}_val`).innerText = weights[k].toFixed(2);
  }
  updateTotalWeightDisplay();
  computePlaygroundScores();
}

function coldPenalty(ageMin) {
  if (ageMin < 5) return 0.0;
  if (ageMin >= 30) return 1.0;
  return (ageMin - 5) / 25;
}

function normalize(values) {
  const vals = Object.values(values);
  const mn = Math.min(...vals);
  const mx = Math.max(...vals);
  if (mx === mn) {
    const res = {};
    for (const k of Object.keys(values)) res[k] = 0.0;
    return res;
  }
  const res = {};
  for (const [k, v] of Object.entries(values)) {
    res[k] = (v - mn) / (mx - mn);
  }
  return res;
}

function computePlaygroundScores() {
  const hour = parseInt(document.getElementById("pgHourSlider").value) || 0;
  const hCarbon = CARBON_REPLAY[hour] || { "ap-south-1": 72.5, "eu-north-1": 19.0, "us-east-1": 325.0 };

  const rawCarbon = { ...hCarbon };
  const rawLatency = { ...pgEwmaLatency };
  const rawCold = {};
  REGIONS.forEach(r => {
    rawCold[r] = coldPenalty(pgIdleMinutes[r] || 0);
  });
  const rawCost = { ...COST_FACTORS };

  const normC = normalize(rawCarbon);
  const normL = normalize(rawLatency);
  const normCost = normalize(rawCost);

  const scores = {};
  const breakdown = {};

  REGIONS.forEach(r => {
    const cPart = weights.carbon * normC[r];
    const lPart = weights.latency * normL[r];
    const sPart = weights.cold * rawCold[r];
    const mPart = weights.cost * normCost[r];

    scores[r] = cPart + lPart + sPart + mPart;
    breakdown[r] = { cPart, lPart, sPart, mPart, rawCarbon: rawCarbon[r], rawLat: rawLatency[r], coldPen: rawCold[r], costFactor: rawCost[r] };
  });

  // Rank regions (lower score is better)
  const ranked = [...REGIONS].sort((a, b) => scores[a] - scores[b]);
  renderPlaygroundRankings(ranked, scores, breakdown);
}

function renderPlaygroundRankings(ranked, scores, breakdown) {
  const container = document.getElementById("pgRankingsContainer");
  if (!container) return;

  const winner = ranked[0];

  container.innerHTML = ranked.map((r, idx) => {
    const isWinner = idx === 0;
    const b = breakdown[r];
    const scoreVal = scores[r].toFixed(4);

    const cWidth = (b.cPart / (scores[r] || 0.001)) * 100;
    const lWidth = (b.lPart / (scores[r] || 0.001)) * 100;
    const sWidth = (b.sPart / (scores[r] || 0.001)) * 100;
    const mWidth = (b.mPart / (scores[r] || 0.001)) * 100;

    let flag = "🇮🇳";
    let location = "Mumbai (Home)";
    if (r === "eu-north-1") { flag = "🇸🇪"; location = "Stockholm"; }
    if (r === "us-east-1") { flag = "🇺🇸"; location = "N. Virginia"; }

    return `
      <div class="rank-card ${isWinner ? 'winner' : ''}">
        <div class="rank-card-header">
          <div style="display:flex;align-items:center;gap:0.6rem;">
            <span class="rank-badge">${isWinner ? '🏆 #1 WINNER' : `#${idx + 1}`}</span>
            <strong style="font-size:1.05rem;">${r}</strong>
            <span style="font-size:0.8rem;color:#94a3b8;">${flag} ${location}</span>
          </div>
          <div class="rank-score">
            <span style="font-size:0.75rem;color:#94a3b8;font-weight:normal;">Score:</span> ${scoreVal}
          </div>
        </div>

        <div class="component-bar-container">
          <div class="component-bar">
            <div class="component-seg" style="width:${cWidth}%;background:#10b981;" title="Carbon: ${(b.cPart).toFixed(3)}"></div>
            <div class="component-seg" style="width:${lWidth}%;background:#3b82f6;" title="Latency: ${(b.lPart).toFixed(3)}"></div>
            <div class="component-seg" style="width:${sWidth}%;background:#a855f7;" title="Cold Start: ${(b.sPart).toFixed(3)}"></div>
            <div class="component-seg" style="width:${mWidth}%;background:#f59e0b;" title="Cost: ${(b.mPart).toFixed(3)}"></div>
          </div>
          <div class="component-legend">
            <span style="color:#34d399;">C: ${(b.cPart).toFixed(3)}</span>
            <span style="color:#60a5fa;">L: ${(b.lPart).toFixed(3)}</span>
            <span style="color:#c084fc;">Cold: ${(b.sPart).toFixed(3)}</span>
            <span style="color:#fbbf24;">Cost: ${(b.mPart).toFixed(3)}</span>
          </div>
        </div>

        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.5rem;font-size:0.72rem;color:#94a3b8;margin-top:0.6rem;padding-top:0.6rem;border-top:1px solid rgba(255,255,255,0.05);">
          <div>Grid: <strong style="color:#f8fafc;">${b.rawCarbon}</strong> gCO2</div>
          <div>EWMA Lat: <strong style="color:#f8fafc;">${b.rawLat}</strong> ms</div>
          <div>Cold Pen: <strong style="color:#f8fafc;">${b.coldPen.toFixed(2)}</strong></div>
          <div>Cost Factor: <strong style="color:#f8fafc;">${b.costFactor.toFixed(2)}x</strong></div>
        </div>
      </div>
    `;
  }).join("");
}

// ==================== RESULTS SUMMARY TABLE ====================
let resultsSortCol = "total_gco2";
let resultsSortAsc = true;

const POLICY_META = {
  "carbon_only": { name: "Carbon Only", tag: "Lowest Emissions", desc: "Selects region based exclusively on lowest carbon intensity (Stockholm eu-north-1)." },
  "multi_objective": { name: "Multi Objective", tag: "Optimal Balance", desc: "Dynamically weights carbon, latency, cold penalty, and cost. Achieves optimal balance." },
  "home": { name: "Home Region", tag: "Baseline Latency", desc: "Always invokes worker in local Mumbai ap-south-1 region. Zero cross-region network hop." },
  "round_robin": { name: "Round Robin", tag: "Naive Distribution", desc: "Disperses load cyclically across all 3 regions. Suffers 4x cold starts and higher emissions." }
};

function initResultsTable() {
  renderResultsTable();

  const searchInput = document.getElementById("resultsSearchInput");
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      renderResultsTable(searchInput.value.toLowerCase().trim());
    });
  }

  document.querySelectorAll("#summaryDataTable th[data-col]").forEach(th => {
    th.addEventListener("click", () => {
      const col = th.getAttribute("data-col");
      if (resultsSortCol === col) {
        resultsSortAsc = !resultsSortAsc;
      } else {
        resultsSortCol = col;
        resultsSortAsc = true;
      }
      renderResultsTable();
    });
  });
}

function renderResultsTable(filter = "") {
  const tbody = document.querySelector("#summaryDataTable tbody");
  if (!tbody) return;

  const rows = Object.entries(SUMMARY_DATA).map(([key, data]) => ({
    key: key,
    name: POLICY_META[key] ? POLICY_META[key].name : key,
    ...data
  }));

  const filtered = rows.filter(r => 
    r.name.toLowerCase().includes(filter) || r.key.toLowerCase().includes(filter)
  );

  filtered.sort((a, b) => {
    let vA = a[resultsSortCol];
    let vB = b[resultsSortCol];
    if (typeof vA === "string") return resultsSortAsc ? vA.localeCompare(vB) : vB.localeCompare(vA);
    return resultsSortAsc ? vA - vB : vB - vA;
  });

  tbody.innerHTML = filtered.map(r => {
    const meta = POLICY_META[r.key] || {};
    const isLowestCO2 = r.key === "carbon_only";
    const isOptimal = r.key === "multi_objective";

    return `
      <tr>
        <td>
          <div style="font-weight:700;color:#f8fafc;display:flex;align-items:center;gap:0.4rem;">
            ${r.name}
            ${isLowestCO2 ? '<span class="badge-pill" style="background:rgba(16,185,129,0.2);color:#34d399;">Eco Winner</span>' : ''}
            ${isOptimal ? '<span class="badge-pill" style="background:rgba(139,92,246,0.2);color:#c084fc;">Balanced Winner</span>' : ''}
          </div>
          <span style="font-size:0.72rem;color:#64748b;">${meta.desc || ''}</span>
        </td>
        <td><strong>${r.n}</strong></td>
        <td style="color:${isLowestCO2 ? '#34d399' : '#f8fafc'};font-weight:700;">${r.total_gco2.toFixed(4)} g</td>
        <td>${r.avg_gco2.toFixed(6)} g</td>
        <td style="color:${r.avg_latency_ms < 900 ? '#60a5fa' : '#f8fafc'};">${r.avg_latency_ms.toFixed(2)} ms</td>
        <td>${r.p95_latency_ms.toFixed(2)} ms</td>
        <td>${(r.cold_start_rate * 100).toFixed(1)}% <span style="font-size:0.72rem;color:#64748b;">(${r.cold_start_count})</span></td>
        <td style="font-size:0.75rem;">
          ${Object.entries(r.region_distribution).map(([reg, cnt]) => `${reg}: ${cnt}`).join(", ")}
        </td>
      </tr>
    `;
  }).join("");
}
"""

