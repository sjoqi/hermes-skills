# macOS CoreWLAN RSSI sensing — no ESP32 required

Real, live WiFi **presence / motion** sensing on a Mac using only its own WiFi
radio (e.g. tethered to an iPhone hotspot). This is RSSI-grade, NOT CSI — it
proves the `ruvnet/RuView` macOS CoreWLAN path works on Apple Silicon and gives
genuine (non-simulated) presence/motion, but no person-count / through-wall /
pose / vitals.

## Why this works without ESP32
macOS exposes the active WiFi interface's RSSI via the **CoreWLAN** framework.
The repo's `archive/v1/src/sensing/mac_wifi.swift` shells out from Rust and prints
one JSON object per line at ~10 Hz. When a body (or the iPhone itself) moves in
the RF path between the Mac and its AP, the RSSI fluctuates — that fluctuation is
the signal.

## The helper (compiled once)
File: `scripts/mac_wifi.swift` (copy beside this md). Compile:
```bash
swiftc -O mac_wifi.swift -o mac_wifi
```
Emits:
```json
{"timestamp":1785746415.9,"rssi":-33,"noise":-93,"tx_rate":144.0,"ssid":"","bssid":"","channel":6}
```
- Reads `CWWiFiClient.shared().interface().rssiValue()` — no special entitlement
  needed for the *active* interface.
- `ssid`/`bssid` come back **blank on macOS Sonoma+** (Apple redacts them without
  the `com.apple.wifi.scan` entitlement). That's fine — `rssi` and `channel` are
  still real. Use `channel` to confirm which link you're on (ch 6 = 2.4 GHz =
  typical iPhone hotspot).

## Hotspot topology (if Mac is tethered to the iPhone)
- **iPhone = transmitter** (it's the AP you're connected to).
- **Mac = receiver** running the detector.
- Moving the iPhone → link RSSI changes → detector sees it (device presence).
- A person walking between Mac and iPhone → body shadows the link → detector sees
  it (human presence). A person standing still outside the Mac↔iPhone path → NOT
  detected (no effect on that specific link).
- From RSSI alone you **cannot distinguish "person" from "phone moving"** — both
  are just RSSI changes. CSI is needed for that.

## The drift trap (the one thing that breaks naive detectors)
Raw RSSI wanders slowly (thermal, tiny distance changes) even when nobody moves.
A detector that thresholds the raw `stddev` over a window will false-trigger
MOTION on calm data. The fix that worked live:

> Track **consecutive-sample deltas** `d = rssi[i] - rssi[i-1]`, keep a rolling
> window of them, and threshold the **stddev of those deltas** (`delta_stddev`).

Rationale: a walking body produces rapid up/down jitter (large, alternating
deltas → high `delta_stddev`); slow drift produces smooth, small deltas → low
`delta_stddev`. Tuned live on an M1 Air: `motion_db = 1.5` dB, `quiet_std = 0.4` dB.
Calm hotspot data sat at `delta_stddev` 0.6–0.9 (no false MOTION); a shaped
jitter signal pushed it to 1.7–2.1 (clean MOTION).

Minimal Rust loop (pseudo):
```rust
let mut last = f64::NAN;
let mut deltas: Vec<f64> = vec![];
for each sample v {
    if !last.is_nan() { deltas.push(v - last); /* cap window */ }
    last = v;
}
let d_std = stddev(&deltas);
let state = if d_std >= 1.5 { "MOTION" }
            else if d_std <= 0.4 { "STILL / PRESENT" }
            else { "IDLE" };
```

## Verification (do this before claiming it works)
1. **Classifier on shaped data** — write a fake helper that emits calm RSSI for
   5 s, then rapid `±6 dB` sinusoidal jitter for 5 s, then calm. Pipe it to the
   detector and assert: `STILL / PRESENT` during calm, `MOTION` during jitter.
   (This isolates the classifier from hardware noise.)
2. **Live capture** — run the real `mac_wifi` for a few seconds and confirm ≥1
   sample with a real `rssi` value off your actual link.
3. **Real body-motion run** — the agent cannot move hardware; the user waves a
   hand / moves the phone and watches the detector flip to MOTION. This last 1%
   is a manual confirmation.
- Ad-hoc verification can be done with a `hermes-verify-*.sh` temp script
  (OS temp dir, cleaned up after). Watch a quoting bug: Python `dict` repr uses
  **single** quotes, so `grep '"rssi"'` misses it — check for both `'rssi'` and
  `"rssi"`.

## Honesty boundary
- ✅ Real presence/motion on hardware you own.
- ❌ Not CSI: no through-wall, pose, vitals, or person-count.
- ❌ Cannot tell person apart from a moving phone from RSSI alone.
