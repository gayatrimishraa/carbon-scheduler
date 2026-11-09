CSS_STYLES = """
:root {
  --bg-primary: #0a0e17;
  --bg-secondary: #111827;
  --bg-tertiary: #1a2234;
  --bg-card: rgba(17, 24, 39, 0.75);
  --bg-card-hover: rgba(26, 36, 56, 0.85);
  --border-color: rgba(255, 255, 255, 0.08);
  --border-focus: #38bdf8;
  
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  
  --color-green: #10b981;
  --color-green-glow: rgba(16, 185, 129, 0.2);
  --color-blue: #3b82f6;
  --color-blue-glow: rgba(59, 130, 246, 0.2);
  --color-purple: #a855f7;
  --color-purple-glow: rgba(168, 85, 247, 0.2);
  --color-orange: #f59e0b;
  --color-orange-glow: rgba(245, 158, 11, 0.2);
  --color-cyan: #06b6d4;
  --color-red: #ef4444;

  --policy-home: #3b82f6;
  --policy-rr: #f97316;
  --policy-carbon: #10b981;
  --policy-multi: #8b5cf6;

  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: var(--font-sans);
  background-color: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.6;
  min-height: 100vh;
  overflow-x: hidden;
  background-image: 
    radial-gradient(circle at 15% 15%, rgba(16, 185, 129, 0.05) 0%, transparent 40%),
    radial-gradient(circle at 85% 25%, rgba(59, 130, 246, 0.05) 0%, transparent 40%),
    radial-gradient(circle at 50% 80%, rgba(168, 85, 247, 0.03) 0%, transparent 50%),
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 100% 100%, 100% 100%, 100% 100%, 40px 40px, 40px 40px;
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: var(--bg-primary);
}
::-webkit-scrollbar-thumb {
  background: #2a3447;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #3b4861;
}

/* Navigation Header */
header.top-nav {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(10, 14, 23, 0.88);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border-color);
  padding: 0.75rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand-wrapper {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-weight: 800;
  font-size: 1.3rem;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, #10b981 0%, #38bdf8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-logo svg {
  color: #10b981;
}

.brand-badge {
  font-size: 0.65rem;
  text-transform: uppercase;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
  background: rgba(56, 189, 248, 0.12);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.25);
}

.nav-links {
  display: flex;
  gap: 0.4rem;
  list-style: none;
}

.nav-links a {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 0.85rem;
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.nav-links a:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.05);
}

.nav-links a.active {
  color: #38bdf8;
  background: rgba(56, 189, 248, 0.1);
  border-color: rgba(56, 189, 248, 0.25);
}

.system-status {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.78rem;
  color: var(--text-secondary);
  background: rgba(16, 185, 129, 0.08);
  border: 1px solid rgba(16, 185, 129, 0.2);
  padding: 0.35rem 0.8rem;
  border-radius: 9999px;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--color-green);
  box-shadow: 0 0 10px var(--color-green);
  animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.2); }
}

/* Layout */
main {
  max-width: 1440px;
  margin: 0 auto;
  padding: 2.5rem 2rem 5rem 2rem;
}

section {
  margin-bottom: 5rem;
  scroll-margin-top: 5rem;
}

/* Section Header */
.section-header {
  margin-bottom: 2rem;
}

.section-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #38bdf8;
  margin-bottom: 0.5rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.section-subtitle {
  font-size: 1.05rem;
  color: var(--text-secondary);
  max-width: 850px;
}

/* Cards & Glassmorphism */
.card {
  background: var(--bg-card);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  border-color: rgba(255, 255, 255, 0.15);
}

.card-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Overview Metric Cards Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.25rem;
  margin-bottom: 2rem;
}

.metric-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, var(--accent-color, #38bdf8), transparent);
}

.metric-card.green { --accent-color: var(--color-green); }
.metric-card.blue { --accent-color: var(--color-blue); }
.metric-card.purple { --accent-color: var(--color-purple); }
.metric-card.orange { --accent-color: var(--color-orange); }

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.metric-label {
  font-size: 0.82rem;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.metric-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.04);
  color: var(--accent-color, #38bdf8);
}

.metric-value {
  font-size: 2.25rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  line-height: 1.1;
  margin-bottom: 0.4rem;
}

.metric-sub {
  font-size: 0.82rem;
  color: var(--text-secondary);
}

/* Policy Showcase Grid */
.policies-showcase {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
  margin-bottom: 2rem;
}

.policy-box {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  position: relative;
  transition: transform 0.2s, border-color 0.2s;
}

.policy-box:hover {
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.2);
}

.policy-box-tag {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
}

.policy-box.home .policy-box-tag { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
.policy-box.round_robin .policy-box-tag { background: rgba(249, 115, 22, 0.15); color: #fb923c; }
.policy-box.carbon_only .policy-box-tag { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.policy-box.multi_objective .policy-box-tag { background: rgba(139, 92, 246, 0.15); color: #c084fc; }

.policy-box h4 {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.4rem;
}

.policy-box p {
  font-size: 0.88rem;
  color: var(--text-secondary);
  line-height: 1.5;
  margin-bottom: 1rem;
}

.policy-box-meta {
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  padding-top: 0.75rem;
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
}

.policy-box-meta span {
  color: var(--text-muted);
}
.policy-box-meta strong {
  color: var(--text-primary);
}

/* Highlight Banner */
.highlight-banner {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(56, 189, 248, 0.08) 100%);
  border: 1px solid rgba(16, 185, 129, 0.25);
  border-radius: 12px;
  padding: 1.5rem 2rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.highlight-banner .icon-box {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.highlight-banner h4 {
  font-size: 1.05rem;
  font-weight: 700;
  color: #34d399;
  margin-bottom: 0.25rem;
}

.highlight-banner p {
  font-size: 0.95rem;
  color: var(--text-primary);
  line-height: 1.5;
}

/* Architecture SVG Container */
.arch-diagram-wrapper {
  background: #0d131f;
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
  margin-bottom: 2rem;
}

.arch-svg-container {
  width: 100%;
  overflow-x: auto;
}

.arch-svg {
  width: 100%;
  min-width: 960px;
  height: auto;
  display: block;
}

.arch-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-top: 1.25rem;
  padding-top: 1.25rem;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  font-size: 0.82rem;
  color: var(--text-secondary);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.legend-line {
  width: 24px;
  height: 3px;
  border-radius: 2px;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

/* Live Scheduler Section Styles */
.scheduler-panel {
  display: grid;
  grid-template-columns: 1fr 1.35fr;
  gap: 1.5rem;
}

@media (max-width: 1024px) {
  .scheduler-panel {
    grid-template-columns: 1fr;
  }
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.84rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 0.45rem;
}

.form-label span.badge-hint {
  font-size: 0.72rem;
  color: #38bdf8;
  background: rgba(56, 189, 248, 0.1);
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
}

.input-with-action {
  position: relative;
  display: flex;
}

.input-text, .select-input {
  width: 100%;
  background: rgba(10, 14, 23, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 8px;
  padding: 0.7rem 0.9rem;
  color: var(--text-primary);
  font-family: var(--font-mono);
  font-size: 0.88rem;
  transition: all 0.2s;
}

.input-text:focus, .select-input:focus {
  outline: none;
  border-color: #38bdf8;
  box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15);
}

.input-btn-toggle {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 4px 8px;
  font-size: 0.75rem;
  border-radius: 4px;
}

.input-btn-toggle:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.08);
}

/* Policy Selector Pills */
.policy-pills {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.policy-pill {
  background: rgba(10, 14, 23, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 0.65rem 0.8rem;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  transition: all 0.2s;
}

.policy-pill:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.2);
}

.policy-pill.selected {
  background: rgba(56, 189, 248, 0.12);
  border-color: #38bdf8;
}

.policy-pill .pill-name {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-primary);
}

.policy-pill .pill-desc {
  font-size: 0.72rem;
  color: var(--text-muted);
}

/* Hour Slider */
.slider-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.range-slider {
  width: 100%;
  height: 6px;
  background: #1e293b;
  border-radius: 3px;
  outline: none;
  -webkit-appearance: none;
}

.range-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #38bdf8;
  cursor: pointer;
  box-shadow: 0 0 8px rgba(56, 189, 248, 0.5);
  transition: transform 0.1s;
}

.range-slider::-webkit-slider-thumb:hover {
  transform: scale(1.15);
}

.hour-preview-box {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.hour-preview-box span strong {
  color: #38bdf8;
}

/* Execute Button */
.btn-execute {
  width: 100%;
  background: linear-gradient(135deg, #2563eb 0%, #10b981 100%);
  color: #ffffff;
  border: none;
  border-radius: 8px;
  padding: 0.9rem 1.5rem;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
  transition: all 0.2s;
}

.btn-execute:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

.btn-execute:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Spinner */
.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Live Execution Output Display */
.output-display {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.output-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.badge-status {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.3rem 0.65rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
}

.badge-status.idle {
  background: rgba(100, 116, 139, 0.15);
  color: #94a3b8;
  border: 1px solid rgba(100, 116, 139, 0.25);
}

.badge-status.running {
  background: rgba(56, 189, 248, 0.15);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.3);
}

.badge-status.success {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.badge-status.error {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.telemetry-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.telemetry-card {
  background: rgba(10, 14, 23, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  padding: 1rem;
}

.telemetry-card.highlight {
  border-color: rgba(56, 189, 248, 0.3);
  background: rgba(56, 189, 248, 0.04);
}

.telemetry-card .t-label {
  font-size: 0.72rem;
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: 600;
  margin-bottom: 0.35rem;
}

.telemetry-card .t-val {
  font-size: 1.45rem;
  font-weight: 800;
  color: var(--text-primary);
  font-family: var(--font-mono);
}

.telemetry-card .t-desc {
  font-size: 0.72rem;
  color: var(--text-secondary);
  margin-top: 0.2rem;
}

/* Scores Breakdown Bar */
.scores-container {
  background: rgba(10, 14, 23, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.scores-title {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
  display: flex;
  justify-content: space-between;
}

.region-score-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.82rem;
}

.region-score-row.chosen {
  font-weight: 700;
  color: #34d399;
}

.score-bar-bg {
  flex-grow: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 3px;
  margin: 0 0.75rem;
  overflow: hidden;
}

.score-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.4s ease;
}

/* Request History Table */
.history-section {
  margin-top: 2rem;
}

.table-container {
  overflow-x: auto;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  background: var(--bg-card);
}

table.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.84rem;
}

table.data-table th {
  background: rgba(10, 14, 23, 0.85);
  padding: 0.8rem 1rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  font-size: 0.72rem;
  letter-spacing: 0.05em;
  border-bottom: 1px solid var(--border-color);
  cursor: pointer;
  user-select: none;
}

table.data-table th:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.03);
}

table.data-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  color: var(--text-secondary);
  font-family: var(--font-mono);
  font-size: 0.82rem;
}

table.data-table tr:last-child td {
  border-bottom: none;
}

table.data-table tr:hover td {
  background: rgba(255, 255, 255, 0.02);
  color: var(--text-primary);
}

/* Policy Playground Slider Grid */
.playground-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.75rem;
}

@media (max-width: 1024px) {
  .playground-grid {
    grid-template-columns: 1fr;
  }
}

.slider-group-card {
  background: rgba(10, 14, 23, 0.6);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 1.25rem;
  margin-bottom: 1rem;
}

.slider-group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.slider-name {
  font-weight: 700;
  font-size: 0.9rem;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.slider-val-badge {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
}

.preset-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.btn-preset {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-secondary);
  font-size: 0.78rem;
  font-weight: 600;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-preset:hover {
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-primary);
  border-color: rgba(255, 255, 255, 0.2);
}

.btn-preset.active {
  background: rgba(56, 189, 248, 0.15);
  color: #38bdf8;
  border-color: #38bdf8;
}

/* Region Ranking Cards */
.ranking-cards {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.rank-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.25rem;
  position: relative;
  transition: all 0.3s;
}

.rank-card.winner {
  border-color: #10b981;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(10, 14, 23, 0.85) 100%);
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.15);
}

.rank-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.rank-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.75rem;
  font-weight: 800;
  padding: 0.2rem 0.6rem;
  border-radius: 9999px;
  text-transform: uppercase;
}

.rank-card.winner .rank-badge {
  background: #10b981;
  color: #042f2e;
}

.rank-card:not(.winner) .rank-badge {
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-muted);
}

.rank-score {
  font-family: var(--font-mono);
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--text-primary);
}

.component-bar-container {
  margin: 0.75rem 0;
}

.component-bar {
  display: flex;
  height: 10px;
  border-radius: 5px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.05);
}

.component-seg {
  height: 100%;
  transition: width 0.3s ease;
}

.component-legend {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
  color: var(--text-muted);
  margin-top: 0.35rem;
  font-family: var(--font-mono);
}

/* Charts Gallery Grid */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(460px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

@media (max-width: 640px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

.chart-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.chart-card.wide {
  grid-column: 1 / -1;
}

.chart-image-wrap {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  background: #ffffff;
  padding: 0.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.chart-image-wrap img {
  width: 100%;
  height: auto;
  display: block;
}

.chart-analysis {
  font-size: 0.88rem;
  color: var(--text-secondary);
  line-height: 1.55;
}

.chart-analysis strong {
  color: var(--text-primary);
}

.badge-pill {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
}

/* Math Equations Box */
.math-equation-card {
  background: #0d131f;
  border: 1px solid rgba(56, 189, 248, 0.2);
  border-left: 4px solid #38bdf8;
  border-radius: 8px;
  padding: 1.25rem 1.5rem;
  margin: 1.25rem 0;
  font-family: var(--font-mono);
  font-size: 0.95rem;
  color: #e2e8f0;
  line-height: 1.8;
  overflow-x: auto;
}

.variable-explainer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
}

.var-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 6px;
  padding: 0.75rem 1rem;
}

.var-item code {
  color: #38bdf8;
  font-weight: 700;
  font-size: 0.85rem;
}

.var-item p {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-top: 0.2rem;
}

/* Footer */
footer.site-footer {
  border-top: 1px solid var(--border-color);
  padding: 2.5rem 2rem;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.84rem;
  background: rgba(10, 14, 23, 0.95);
}

footer.site-footer p {
  margin-bottom: 0.4rem;
}

footer.site-footer .meta-links {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 0.8rem;
}

footer.site-footer a {
  color: #38bdf8;
  text-decoration: none;
}

footer.site-footer a:hover {
  text-decoration: underline;
}

/* Utility buttons */
.btn-sm {
  font-size: 0.75rem;
  padding: 0.3rem 0.65rem;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-sm:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
}

.raw-json-box {
  background: #070a10;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  padding: 0.75rem;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #a5f3fc;
  max-height: 200px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-all;
  margin-top: 0.5rem;
}
"""

