# RuView Docker runbook (simulated, no hardware)

Verified working on macOS (Apple Silicon), Docker 27.4, RuView image `ruvnet/wifi-densepose:latest`
(multi-arch amd64+arm64). Repo `ruvnet/wifi-densepose` redirects to `ruvnet/RuView`.

## Prereqs
- Docker Desktop installed AND running. If `docker pull` fails with
  "Cannot connect to the Docker daemon at unix://...", run `open -a Docker` and
  poll `docker info` until it returns 0 (takes ~5-10s).

## Start the simulated demo (loopback-safe)
```bash
TOKEN=$(openssl rand -hex 32)
echo -n "$TOKEN" > .ruview_token && chmod 600 .ruview_token

docker run -d --name ruview-demo \
  -e RUVIEW_BIND_ADDR=0.0.0.0 \
  -e RUVIEW_API_TOKEN=$TOKEN \
  -p 127.0.0.1:3000:3000 -p 5005:5005/udp \
  ruvnet/wifi-densepose:latest
```
Notes:
- Bind `0.0.0.0` INSIDE the container (so the port map works) + token; publish the
  host port as `127.0.0.1:3000` (host-side loopback only) so it is NOT LAN-exposed.
  Do NOT set `RUVIEW_BIND_ADDR=127.0.0.1` — that binds loopback *inside* the
  container and makes `-p 3000:3000` silently useless.
- Drop `-p 127.0.0.1:3001:3001` if port 3001 is already taken (e.g. a `flowise`
  container). The REST demo works without it; only the live-CSI WebSocket needs 3001.

## Verify the pipeline is live
```bash
T=$(cat .ruview_token)
curl -s -H "Authorization: Bearer $T" http://localhost:3000/health
# {"status":"ok","source":"simulated","tick":N,...}
curl -s -H "Authorization: Bearer $T" http://localhost:3000/api/v1/sensing/latest
# presence:true, motion, mean_rssi, breathing_band_power, nodes[].amplitude[]
curl -s -H "Authorization: Bearer $T" http://localhost:3000/api/v1/vital-signs
# breathing_rate_bpm, heart_rate_bpm (SIMULATED)
curl -s -H "Authorization: Bearer $T" http://localhost:3000/api/v1/model/info
# {"status":"no_model"}  (expected; pose head needs an RVF model)
```
A 200 with JSON = running. Simulated mode auto-promotes to live CSI the instant a
real frame hits UDP :5005.

## Endpoints (real ones; landing page lists a wrong WS port)
- UI:              http://localhost:3000/ui/index.html
- REST root:       http://localhost:3000/            (HTTP 200, lists links)
- Health:          /health
- Sensing latest:  /api/v1/sensing/latest
- Vitals:          /api/v1/vital-signs
- Model info:      /api/v1/model/info
- Live CSI WS:     ws://localhost:3001/ws/sensing   (NOT :8765 as the root HTML claims)

All `/api/v1/*` require `Authorization: Bearer <token>`.

## Manage it
```bash
docker stop ruview-demo      # pause
docker start ruview-demo     # resume (same token persists in container)
docker logs -f ruview-demo   # tail
docker rm -f ruview-demo     # destroy (token file remains; re-read after a re-run)
```
After `rm`+`run` the token is regenerated — `cat .ruview_token` for the new one.

## Gotchas observed
- Entrypoint guard (issue #864): refuses non-loopback bind without a token. Fix above.
- `Empty reply from server` (curl 52) = you set the in-container bind to 127.0.0.1. Re-run with 0.0.0.0.
- Host-header validation is ON but loopback names are always allowed; `localhost`/`127.0.0.1` work.
