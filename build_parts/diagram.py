SVG_DIAGRAM = """
<svg class="arch-svg" viewBox="0 0 1200 680" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Gradients -->
    <linearGradient id="bgHome" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0e172a" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#0b1329" stop-opacity="0.95"/>
    </linearGradient>
    <linearGradient id="bgRemote" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111827" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#0c121e" stop-opacity="0.9"/>
    </linearGradient>
    
    <linearGradient id="gradRouter" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f97316"/>
      <stop offset="100%" stop-color="#ea580c"/>
    </linearGradient>
    
    <linearGradient id="gradWorker" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#1d4ed8"/>
    </linearGradient>

    <linearGradient id="gradDDB" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#2563eb"/>
    </linearGradient>

    <linearGradient id="gradGreen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10b981"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>

    <!-- Filters -->
    <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="glow-green" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>

    <!-- Markers -->
    <marker id="arrow-cyan" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#38bdf8"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#10b981"/>
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#f97316"/>
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#a855f7"/>
    </marker>
  </defs>

  <!-- ==================== REGION BOUNDARIES ==================== -->
  
  <!-- HOME REGION: ap-south-1 -->
  <rect x="230" y="30" width="530" height="620" rx="16" fill="url(#bgHome)" stroke="#38bdf8" stroke-width="2" stroke-dasharray="8 4" opacity="0.95"/>
  <rect x="230" y="30" width="530" height="38" rx="16" fill="#1e293b" opacity="0.6"/>
  <text x="250" y="55" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="14" font-weight="800" letter-spacing="1">
    AWS REGION: ap-south-1 (Mumbai) [HOME REGION]
  </text>
  <rect x="620" y="40" width="125" height="20" rx="4" fill="rgba(56,189,248,0.15)" stroke="#38bdf8" stroke-width="1"/>
  <text x="632" y="54" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="11" font-weight="700">Single-Region DDB</text>

  <!-- REMOTE REGION 1: eu-north-1 -->
  <rect x="800" y="30" width="370" height="290" rx="16" fill="url(#bgRemote)" stroke="#10b981" stroke-width="1.5" stroke-dasharray="6 3" opacity="0.9"/>
  <rect x="800" y="30" width="370" height="36" rx="16" fill="#064e3b" opacity="0.4"/>
  <text x="820" y="54" fill="#34d399" font-family="system-ui, sans-serif" font-size="13" font-weight="700">
    AWS REGION: eu-north-1 (Stockholm)
  </text>
  <text x="1035" y="54" fill="#6ee7b7" font-family="monospace" font-size="10">Grid: ~19-28 gCO2</text>

  <!-- REMOTE REGION 2: us-east-1 -->
  <rect x="800" y="360" width="370" height="290" rx="16" fill="url(#bgRemote)" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="6 3" opacity="0.9"/>
  <rect x="800" y="360" width="370" height="36" rx="16" fill="#78350f" opacity="0.4"/>
  <text x="820" y="384" fill="#fbbf24" font-family="system-ui, sans-serif" font-size="13" font-weight="700">
    AWS REGION: us-east-1 (N. Virginia)
  </text>
  <text x="1035" y="384" fill="#fde68a" font-family="monospace" font-size="10">Grid: ~325-400 gCO2</text>


  <!-- ==================== CLIENT / BROWSER ==================== -->
  <g transform="translate(30, 240)">
    <rect width="150" height="130" rx="12" fill="#1e293b" stroke="#64748b" stroke-width="1.5"/>
    <rect width="150" height="28" rx="12" fill="#334155"/>
    <circle cx="15" cy="14" r="4" fill="#ef4444"/>
    <circle cx="28" cy="14" r="4" fill="#f59e0b"/>
    <circle cx="41" cy="14" r="4" fill="#10b981"/>
    <text x="75" y="18" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11" text-anchor="middle" font-weight="600">Client / Browser</text>
    
    <text x="75" y="60" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle" font-weight="700">Evaluation Client</text>
    <text x="75" y="78" fill="#94a3b8" font-family="monospace" font-size="10" text-anchor="middle">HTTPS POST</text>
    <rect x="15" y="90" width="120" height="24" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1"/>
    <text x="75" y="106" fill="#38bdf8" font-family="monospace" font-size="9" text-anchor="middle">x-scheduler-token</text>
  </g>


  <!-- ==================== HOME REGION COMPONENTS ==================== -->

  <!-- Function URL Endpoint -->
  <g transform="translate(255, 270)">
    <rect width="130" height="70" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="65" y="24" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="11" text-anchor="middle" font-weight="700">Lambda Function URL</text>
    <text x="65" y="42" fill="#94a3b8" font-family="monospace" font-size="9" text-anchor="middle">Auth: NONE</text>
    <text x="65" y="56" fill="#10b981" font-family="monospace" font-size="9" text-anchor="middle">CORS Enabled (300s)</text>
  </g>

  <!-- Router Lambda -->
  <g transform="translate(435, 240)">
    <rect width="165" height="130" rx="12" fill="#1c1917" stroke="#f97316" stroke-width="2"/>
    <rect x="0" y="0" width="165" height="28" rx="12" fill="url(#gradRouter)"/>
    <text x="82" y="19" fill="#ffffff" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle" font-weight="800">ROUTER LAMBDA</text>
    <text x="82" y="50" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="11" text-anchor="middle" font-weight="700">carbon-router</text>
    <text x="82" y="68" fill="#fdba74" font-family="monospace" font-size="9.5" text-anchor="middle">Python 3.11 | 128 MB</text>
    
    <line x1="10" y1="78" x2="155" y2="78" stroke="#44403c" stroke-width="1"/>
    
    <text x="82" y="93" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="9.5" text-anchor="middle">Multi-Objective Engine:</text>
    <text x="82" y="108" fill="#38bdf8" font-family="monospace" font-size="8.5" text-anchor="middle">Carbon (0.4) + Lat (0.3)</text>
    <text x="82" y="120" fill="#a855f7" font-family="monospace" font-size="8.5" text-anchor="middle">+ Cold (0.2) + Cost (0.1)</text>
  </g>

  <!-- Local Worker Lambda in ap-south-1 -->
  <g transform="translate(635, 120)">
    <rect width="110" height="65" rx="8" fill="#1e293b" stroke="#3b82f6" stroke-width="1.5"/>
    <rect x="0" y="0" width="110" height="20" rx="8" fill="#2563eb"/>
    <text x="55" y="14" fill="#ffffff" font-family="system-ui, sans-serif" font-size="9" text-anchor="middle" font-weight="700">WORKER (Local)</text>
    <text x="55" y="38" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="10" text-anchor="middle" font-weight="600">carbon-worker</text>
    <text x="55" y="52" fill="#93c5fd" font-family="monospace" font-size="8.5" text-anchor="middle">ap-south-1</text>
  </g>

  <!-- DynamoDB: region_state Table -->
  <g transform="translate(300, 95)">
    <rect width="130" height="75" rx="8" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
    <rect x="0" y="0" width="130" height="20" rx="8" fill="#0284c7"/>
    <text x="65" y="14" fill="#ffffff" font-family="system-ui, sans-serif" font-size="9.5" text-anchor="middle" font-weight="700">DynamoDB Table</text>
    <text x="65" y="38" fill="#38bdf8" font-family="monospace" font-size="10" text-anchor="middle" font-weight="700">region_state</text>
    <text x="65" y="52" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="8.5" text-anchor="middle">EWMA Latency (ms)</text>
    <text x="65" y="65" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="8.5" text-anchor="middle">Last Invoked Timestamp</text>
  </g>

  <!-- DynamoDB: requests Table -->
  <g transform="translate(465, 430)">
    <rect width="130" height="75" rx="8" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
    <rect x="0" y="0" width="130" height="20" rx="8" fill="#0284c7"/>
    <text x="65" y="14" fill="#ffffff" font-family="system-ui, sans-serif" font-size="9.5" text-anchor="middle" font-weight="700">DynamoDB Table</text>
    <text x="65" y="38" fill="#38bdf8" font-family="monospace" font-size="10" text-anchor="middle" font-weight="700">requests</text>
    <text x="65" y="52" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="8.5" text-anchor="middle">All 972 Records</text>
    <text x="65" y="65" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="8.5" text-anchor="middle">Latency, CO2, Cold, Run</text>
  </g>

  <!-- DynamoDB: carbon_live Table -->
  <g transform="translate(630, 430)">
    <rect width="115" height="75" rx="8" fill="#0f172a" stroke="#10b981" stroke-width="1.5"/>
    <rect x="0" y="0" width="115" height="20" rx="8" fill="#059669"/>
    <text x="57" y="14" fill="#ffffff" font-family="system-ui, sans-serif" font-size="9" text-anchor="middle" font-weight="700">DynamoDB Table</text>
    <text x="57" y="38" fill="#34d399" font-family="monospace" font-size="10" text-anchor="middle" font-weight="700">carbon_live</text>
    <text x="57" y="52" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="8.5" text-anchor="middle">gCO2/kWh per region</text>
    <text x="57" y="65" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="8.5" text-anchor="middle">TTL: 2 Hours</text>
  </g>

  <!-- Carbon Collector Lambda & EventBridge -->
  <g transform="translate(630, 530)">
    <rect width="115" height="60" rx="6" fill="#132e26" stroke="#10b981" stroke-width="1"/>
    <text x="57" y="18" fill="#34d399" font-family="system-ui, sans-serif" font-size="9" text-anchor="middle" font-weight="700">carbon-collector</text>
    <text x="57" y="33" fill="#a7f3d0" font-family="monospace" font-size="8" text-anchor="middle">EventBridge (1 hr)</text>
    <text x="57" y="47" fill="#6ee7b7" font-family="system-ui, sans-serif" font-size="8" text-anchor="middle">Live / Replay Sync</text>
  </g>

  <!-- CloudWatch Logs -->
  <g transform="translate(300, 440)">
    <rect width="130" height="65" rx="8" fill="#18181b" stroke="#ec4899" stroke-width="1.5"/>
    <rect x="0" y="0" width="130" height="20" rx="8" fill="#be185d"/>
    <text x="65" y="14" fill="#ffffff" font-family="system-ui, sans-serif" font-size="9" text-anchor="middle" font-weight="700">CloudWatch Logs</text>
    <text x="65" y="38" fill="#f472b6" font-family="monospace" font-size="8.5" text-anchor="middle">/aws/lambda/router</text>
    <text x="65" y="52" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="8" text-anchor="middle">Cold start init metrics</text>
  </g>


  <!-- ==================== REMOTE WORKERS ==================== -->

  <!-- Remote Worker 1: eu-north-1 (Stockholm) -->
  <g transform="translate(850, 95)">
    <rect width="270" height="180" rx="12" fill="#064e3b" fill-opacity="0.25" stroke="#10b981" stroke-width="2"/>
    <rect x="0" y="0" width="270" height="28" rx="12" fill="url(#gradGreen)"/>
    <text x="135" y="19" fill="#ffffff" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle" font-weight="800">
      WORKER LAMBDA (Stockholm)
    </text>
    <text x="135" y="55" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="13" text-anchor="middle" font-weight="700">carbon-worker</text>
    <text x="135" y="75" fill="#6ee7b7" font-family="monospace" font-size="10.5" text-anchor="middle">arn:aws:lambda:eu-north-1:...:carbon-worker</text>
    
    <rect x="20" y="90" width="230" height="70" rx="6" fill="#042f2e" stroke="#059669" stroke-width="1"/>
    <text x="135" y="110" fill="#a7f3d0" font-family="system-ui, sans-serif" font-size="10" text-anchor="middle" font-weight="600">Synthetic CPU Workload:</text>
    <text x="135" y="126" fill="#ffffff" font-family="monospace" font-size="9" text-anchor="middle">50,000 SHA-256 Iterations (~100ms)</text>
    <text x="135" y="145" fill="#34d399" font-family="monospace" font-size="9.5" text-anchor="middle">Cold container detection: was_cold</text>
  </g>

  <!-- Remote Worker 2: us-east-1 (N. Virginia) -->
  <g transform="translate(850, 425)">
    <rect width="270" height="180" rx="12" fill="#78350f" fill-opacity="0.25" stroke="#f59e0b" stroke-width="2"/>
    <rect x="0" y="0" width="270" height="28" rx="12" fill="url(#gradRouter)"/>
    <text x="135" y="19" fill="#ffffff" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle" font-weight="800">
      WORKER LAMBDA (N. Virginia)
    </text>
    <text x="135" y="55" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="13" text-anchor="middle" font-weight="700">carbon-worker</text>
    <text x="135" y="75" fill="#fde68a" font-family="monospace" font-size="10.5" text-anchor="middle">arn:aws:lambda:us-east-1:...:carbon-worker</text>
    
    <rect x="20" y="90" width="230" height="70" rx="6" fill="#451a03" stroke="#d97706" stroke-width="1"/>
    <text x="135" y="110" fill="#fde68a" font-family="system-ui, sans-serif" font-size="10" text-anchor="middle" font-weight="600">Synthetic CPU Workload:</text>
    <text x="135" y="126" fill="#ffffff" font-family="monospace" font-size="9" text-anchor="middle">50,000 SHA-256 Iterations (~100ms)</text>
    <text x="135" y="145" fill="#f59e0b" font-family="monospace" font-size="9.5" text-anchor="middle">Cold container detection: was_cold</text>
  </g>


  <!-- ==================== FLOW PATHS & ARROWS ==================== -->

  <!-- Path 1: Client -> Function URL -->
  <path id="path-client-furl" d="M 180 305 L 255 305" fill="none" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#arrow-cyan)"/>
  
  <!-- Path 2: Function URL -> Router -->
  <path id="path-furl-router" d="M 385 305 L 435 305" fill="none" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#arrow-cyan)"/>

  <!-- Path 3: Router <-> region_state (Read & Update) -->
  <path id="path-router-state" d="M 450 240 L 390 170" fill="none" stroke="#38bdf8" stroke-width="1.8" stroke-dasharray="4 2" marker-end="url(#arrow-cyan)"/>

  <!-- Path 4: Router -> requests (Persist telemetry) -->
  <path id="path-router-req" d="M 520 370 L 525 430" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow-cyan)"/>

  <!-- Path 5: Router -> CloudWatch -->
  <path id="path-router-cw" d="M 440 360 L 380 440" fill="none" stroke="#ec4899" stroke-width="1.5" stroke-dasharray="4 2" marker-end="url(#arrow-purple)"/>

  <!-- Path 6: Router -> Local Worker (ap-south-1) -->
  <path id="path-router-w-ap" d="M 570 240 Q 610 180 635 160" fill="none" stroke="#3b82f6" stroke-width="2" marker-end="url(#arrow-cyan)"/>

  <!-- Path 7: Router -> Remote Worker 1 (eu-north-1) -->
  <path id="path-router-w-eu" d="M 600 280 C 700 240, 750 180, 850 160" fill="none" stroke="#10b981" stroke-width="2.5" marker-end="url(#arrow-green)"/>

  <!-- Path 8: Router -> Remote Worker 2 (us-east-1) -->
  <path id="path-router-w-us" d="M 600 330 C 700 380, 750 460, 850 490" fill="none" stroke="#f59e0b" stroke-width="2.5" marker-end="url(#arrow-orange)"/>

  <!-- Path 9: Collector -> carbon_live -->
  <path d="M 687 530 L 687 505" fill="none" stroke="#10b981" stroke-width="1.5" marker-end="url(#arrow-green)"/>


  <!-- ==================== ANIMATED PACKETS ==================== -->

  <!-- Packet 1: Client to Function URL -->
  <circle r="4" fill="#38bdf8" filter="url(#glow-cyan)">
    <animateMotion dur="2s" repeatCount="indefinite" path="M 180 305 L 255 305" />
  </circle>

  <!-- Packet 2: Function URL to Router -->
  <circle r="4" fill="#38bdf8" filter="url(#glow-cyan)">
    <animateMotion dur="1.5s" repeatCount="indefinite" path="M 385 305 L 435 305" />
  </circle>

  <!-- Packet 3: Router to eu-north-1 Worker (Green path) -->
  <circle r="5" fill="#34d399" filter="url(#glow-green)">
    <animateMotion dur="3s" repeatCount="indefinite" path="M 600 280 C 700 240, 750 180, 850 160" />
  </circle>

  <!-- Packet 4: Router to us-east-1 Worker (Orange path) -->
  <circle r="5" fill="#fbbf24">
    <animateMotion dur="3.5s" repeatCount="indefinite" path="M 600 330 C 700 380, 750 460, 850 490" />
  </circle>

  <!-- Packet 5: Router to Local Worker (Blue path) -->
  <circle r="4" fill="#60a5fa">
    <animateMotion dur="2.2s" repeatCount="indefinite" path="M 570 240 Q 610 180 635 160" />
  </circle>
  
  <!-- Packet 6: Router to requests DynamoDB -->
  <circle r="4" fill="#38bdf8">
    <animateMotion dur="2s" repeatCount="indefinite" path="M 520 370 L 525 430" />
  </circle>

</svg>
"""

