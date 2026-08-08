---
name: wifi-csi-sensing
description: Deploy, run, and honestly evaluate WiFi CSI (Channel State Information) human-sensing stacks — especially the RuView / wifi-densepose project. Covers hardware requirements (ESP32-S3/C6 for true CSI, macOS CoreWLAN for coarse RSSI), Docker deployment gotchas (entrypoint security guard issue #864, the RUVIEW_BIND_ADDR loopback trap), and the real REST/UI endpoints to probe. Use when the user wants to test or build WiFi-based presence / pose / vitals sensing, with or without ESP32 hardware.
---

# WiFi CSI Sensing (RuView / wifi-densepose)

Turn commodity WiFi signals into spatial intelligence — presence, motion, vitals,
through-wall sensing — without cameras. The reference open-source stack is
`ruvnet/RuView` (the repo `ruvnet/wifi-densepose` now **redirects** to it).

## When to use
- User wants to test/evaluate WiFi sensing but isn't sure about hardware needs.
- User has only a Mac + phone and asks "can I try this without an ESP32?".
- Deploying the RuView Docker image or building the native Rust/Python stack.
- Interpreting the project's accuracy/vitals claims (many are retracted — see below).
- **Assessing whether a WiFi-sensing product is lawful / sellable / brand-safe**
  (GDPR, BIPA, CPRA, landlord-tenant, Airbnb policy, FDA/MDR) — see the
  Legal & go-to-market section below.

## Hardware reality (be honest with the user)
- **True CSI sensing (through-wall pose, contactless vitals):** requires an
  **ESP32-S3 or ESP32-C6** (~$9–10) flashed with the project's CSI firmware.
  **Not supported:** original ESP32 and ESP32-C3 (single-core, too weak for CSI DSP).
  Optional add-on: Cognitum Seed ($131) for persistent memory + witness chain.
- **No hardware at all:** the software runs in **simulated CSI** mode (proves the
  pipeline works, does NOT validate sensing accuracy). See references/ruview-docker-runbook.md.
- **Real but coarse, no ESP32:** build the **native Rust stack** — it has a
  **macOS CoreWLAN adapter** that gives RSSI-grade presence/motion from the Mac's
  own WiFi. Not CSI-grade; an iPhone can only act as a moving RF target (iOS doesn't
  expose CSI), never as a sensor.
- **iPhone (any model):** cannot capture CSI. Useful only as a walking signal source.

## Honesty caveats (this user values precise, non-fabricated claims)
The project's published numbers have been retracted/stubbed — state this before the
user trusts any metric:
- "100% presence" was a single-class recording artifact — retracted (#882).
- "92.9% PCK@20" pose was retracted (2026-06-10): a mean-pose predictor scored 100%
  under a bad protocol; real torso-normalized PCK@20 on holdout ≈19%.
- Live pose cog currently runs as a `confidence=0` stub; the "82.69% pose" is a
  *separate* MM-Fi benchmark, not the live model.
- Honest remaining metric: **82.3% held-out temporal-triplet** (label-free embedding quality).

## Quick test without hardware (Docker, simulated)
Full working recipe + endpoint probes: **references/ruview-docker-runbook.md**.
Key points:
- Image `ruvnet/wifi-densepose:latest` is multi-arch (amd64 + arm64) — runs on Apple Silicon.
- Entrypoint has a security guard (issue #864): it refuses to expose live sensing
  frames on a non-loopback bind without a token.
- TRAP: `RUVIEW_BIND_ADDR=127.0.0.1` binds *inside the container* to loopback,
  making `-p 3000:3000` useless. Bind `0.0.0.0` + set a token, publish the port as
  `127.0.0.1:3000` (host-side loopback only) so it's reachable but not LAN-exposed.
- Real endpoints: `/health`, `/api/v1/sensing/latest`, `/api/v1/vital-signs`,
  `/api/v1/model/info`, UI at `/ui/index.html`. REST requires `Authorization: Bearer <token>`.
- No RVF model loaded → `/api/v1/model/info` returns `no_model` (pose head needs a model).
- Simulated mode auto-promotes to live CSI the instant a real frame hits UDP :5005.

## Native macOS RSSI sensing (no ESP32) — the real recipe
Full working build + code: **references/macos-corewlan-rssi-sensing.md** and the
re-runnable helper **scripts/mac_wifi.swift**. Summary:
- The repo's `archive/v1/src/sensing/mac_wifi.swift` is a Swift CoreWLAN helper
  that prints JSON per line at ~10 Hz:
  `{"timestamp","rssi","noise","tx_rate","ssid","bssid","channel"}`.
  Compile: `swiftc -O mac_wifi.swift -o mac_wifi` (Swift ships with Xcode CLT on
  macOS). It reads `CWWiFiClient.shared().interface().rssiValue()` of the
  **active** link — so if the Mac is tethered to an iPhone hotspot, the iPhone is
  the **transmitter** and the Mac is the **receiver**; moving the iPhone perturbs
  the link RSSI.
- **macOS Sonoma+ redacts BSSID/SSID to blank** without the `com.apple.wifi.scan`
  entitlement, but `rssiValue()` on the active interface needs no entitlement — so
  you still get real RSSI. Confirm the link via `channel` (e.g. ch 6 = 2.4 GHz hotspot).
- **Drift trap (critical):** raw RSSI slowly wanders (thermal/distance), so a naive
  `stddev` over a window false-triggers MOTION on calm data. Fix: compute the
  **stddev of consecutive-sample deltas** (`delta_stddev`) — a walking body causes
  rapid up/down jitter (large alternating deltas); slow drift gives small deltas.
  Thresholds that worked live: `motion_db=1.5`, `quiet_std=0.4` (dB).
- A Rust consumer spawns the helper, parses the JSON, keeps a rolling window of
  deltas, and prints `STILL / PRESENT` vs `MOTION`. RSSI-grade only: presence +
  motion, NOT person-count / through-wall / pose / vitals (those need ESP32 CSI).
  For the full build, delta-stddev latency table, live unicode **sparkline**
  display, the checkpoint-before-change ritual, and the **non-technical-user
  communication rules** (the Hermes verification-reminder summary must never
  overwrite the running explanation), see the dedicated
  `macos-wifi-rssi-sensing` skill.
- **Reactivity / latency tuning:** the window was historically clamped to a
  **minimum of 8 samples** (`let cap = (window_secs * hz).max(8.0)`), flooring
  `--window` to 0.8s and *silently ignoring* `--window 0.3`. **That floor was
  lowered to `2.0`** (commit `feabbbb`), so `--window 0.3` is now genuinely
  honored (~0.3s) — but with only 3 samples `d_std` is noisy/twitchy, so it is NOT
  actually "faster" in practice. True measured latencies (onset→MOTION, via a
  synchronized onset-marker — see `macos-wifi-rssi-sensing` skill):
  `--window 0.3` ≈0.04s (instant, noisy), `--window 1` ≈0.49s (stable,
  **recommended**), `--window 3` ≈1.5s (smooth, sluggish). True hard floor
  ≈0.1s because CoreWLAN only updates RSSI at ~10 Hz. To react faster without code
  change: `--window 1 --motion-db 0.8` (~0.5s, stable). Lower `motion-db`
  (1.5→1.0→0.8) = more sensitive to small motion but more false triggers on calm
  jitter.
- **RSSI detection range (honest envelope, no ESP32):** no fixed radius.
  Same room / indirect path: ~5–10 m. Thin wall (drywall/wood): ~3–7 m, weaker.
  Concrete / multiple walls / different floor: unreliable–none. Detection is
  **directional toward the Mac↔iPhone (hotspot) path** — a body *between* them
  blocks the direct path; off-axis only adds a weak reflection, so it's not
  radial. Phone hotspot TX power is low (~10–20 dBm), limiting range. RSSI cannot
  distinguish "a person" from "the phone moving" — both just perturb the link.
- **Verification pattern that worked:** (a) feed a *shaped* fake helper (calm →
  jitter → calm) and assert the classifier flips STILL→MOTION→STILL; (b) capture a
  few seconds of the *live* helper and confirm real RSSI samples. Then do a real
  body-motion run by hand (agent can't move the hardware).

## Legal & go-to-market risk (hotels, rentals, tenants)
Full sourced knowledge bank: **references/legal-privacy-gtm-risk.md**. Headlines:
- **"No camera" is NOT a legal exemption.** GDPR is technology-neutral; CPRA's
  biometric definition names "gait patterns… and sleep, health, or exercise data";
  CA Penal Code 647(j)(1) says "electronic device" and enumerates bedrooms.
- **Breathing is the pivot.** Presence/motion is comparatively benign; vital signs
  trigger GDPR Art. 9 health data, EU MDR / FDA device classification, and
  failure-to-detect liability all at once. Always offer a presence-only tier.
- **Illinois BIPA is the one safe harbour** — its definition is a closed list that
  CSI doesn't hit. CPRA is the opposite and catches you squarely.
- **Airbnb (eff. 30 Apr 2024)** bans indoor recording devices and bars even decibel
  monitors from bedrooms/sleeping areas → treat short-term rental as closed.
- **Least-friction segment:** hotel/commercial occupancy+motion, non-sleeping
  spaces, disclosed, zero vital-sign claims.
- Contactless vitals is an already-cleared FDA category (Sleepiz K223163, Circadia
  K200445) — "nobody regulates this" is false.
- Always label output **research, not legal advice**, and recommend counsel.

## Pitfalls
- **Working-style — ask, then wait:** This user wants concise answers to clarifying
  questions, then an explicit stop and wait for a "build it" / go-ahead before
  executing long builds or multi-step tasks. Do NOT start building right after a
  Q&A round — confirm first, then proceed.
- **Checkpoint before changes (this user, repeated, explicit):** before any code
  edit the user wants a *restorable checkpoint first*. From a clean local repo:
  `git add -A && git commit -m "..."` then `git tag checkpoint-working`. Exclude
  big clones (e.g. `RuView/`, 225 MB) and secrets (`.ruview_token`) via
  `.gitignore` *before* the first commit. This lets them step back from an error
  loop with `git checkout <tag> -- .` or `git reset --hard <tag>`. Do the
  checkpoint, confirm it's clean, THEN make the change — not after.
- **Push the checkpoint to GitHub from a clean local repo** (no `gh` preinstalled
  on this Mac): `brew install gh && gh auth login` (choose HTTPS + browser code),
  then `gh repo create <name> --private --source=. --remote=origin --push`. Swap
  `--private`→`--public` to open it. This pushes only tracked files (RuView/ and
  the token stay excluded). Future changes: `git add -A && git commit -m "..." &&
  git push`.
- **macOS Docker daemon not running:** `docker pull` fails with "Cannot connect to
  the Docker daemon". Fix: `open -a Docker`, then poll `docker info` until it returns 0.
- **Port 3001 conflict:** the live-CSI WebSocket uses 3001; another container (e.g.
  `flowise`) may already own it. Drop the 3001 publish for a simulated-only demo.
- **WS port doc inconsistency:** root HTML says `ws://localhost:8765/ws/sensing` but
  the server actually binds `0.0.0.0:3001`. Trust the logs, not the landing page.

## Verification
After starting, confirm the pipeline is live with:
```
T=$(cat .ruview_token)
curl -s -H "Authorization: Bearer $T" http://localhost:3000/health
# expect {"status":"ok","source":"simulated",...}
curl -s -H "Authorization: Bearer $T" http://localhost:3000/api/v1/vital-signs
```
A 200 with JSON = the pipeline is running. Remember: simulated ≠ measured.
