# Reference Architecture & Cost Model — DIY Video Rendering

## Topology
```
client ──▶ API Gateway (auth, validate JSON spec vs template schema, return jobId)
        ──▶ Job Queue (SQS Standard, or Redis/BullMQ; big payloads → S3 via Extended Client)
        ──▶ Stateless Render Workers (ECS Fargate / EC2 Spot ASG; GPU g4dn for NVENC)
              • pull job → compile DSL → render (FFmpeg/Remotion) → upload MP4 to S3
              • POST webhook callback (retry w/ exp backoff) + update DynamoDB status
        ──▶ S3 output (Standard, us-east-1 $0.023/GB)
```

## Worker / scaling notes
- Stateless: no local state. One job per worker vCPU slice.
- g4dn.xlarge (T4, 4 vCPU) ≈ 2 NVENC-parallel renders.
- Fargate 2-vCPU task ≈ 1 render.
- Warm pool (min 1–2 workers) + scale on `ApproximateNumberOfMessagesVisible`.
- SQS visibility timeout > worst-case render; heartbeat via `ChangeMessageVisibility`.
- Spot instances (g4dn ≈ $0.16/hr) cut compute ~70% vs on-demand ($0.526/hr).

## Cost model — 1000 × 30-second videos (500 min of 1080p30 output)
Assumptions: g4dn.xlarge on-demand $0.526/hr, NVENC 10× RT (30s clip ≈ 3s
compute), 2 parallel renders/worker.

| Line item | Calc | Cost |
|---|---|---|
| Render compute (EC2) | 500 min ÷ 10 RT = 50 hr × $0.526 | $26.30 |
| S3 storage (output) | 1000 × 30 MB = 30 GB × $0.023 | $0.69 |
| S3 GET/PUT | ~4k reqs (free tier covers 1M) | ~$0.00 |
| SQS | ~4k reqs (free tier covers 1M) | ~$0.00 |
| Remotion Automators (if used) | 1000 × $0.01 | $10.00 |
| **FFmpeg-only total** | | **≈ $27** |
| **+ Remotion tier total** | | **≈ $37** |

Per clip: ~$0.027 (on-demand FFmpeg) → ~$0.008 on Spot → +$0.01 with Remotion.
Contrast managed APIs at $0.50–$2.00/clip (10–200×).

## Throughput example
10 GPU workers @ 10× RT: 1000×30s (500 min output) ≈ 50 min wall clock.
50 workers ≈ 10 min.

## Lambda vs EC2 decision
- **Remotion Lambda**: great for spiky / low-volume; AWS cost pennies (see
  stacks-pricing). Per-render Remotion Automators fee ($0.01) applies on top.
- **EC2/GPU**: cheaper per minute for steady bulk. Pick by workload shape.

## Phased build plan
1. MVP (2–3w): editly + thin JSON DSL + 1 Fargate worker + SQS + S3 + webhook.
2. Own the DSL (3–4w): replace editly with custom `filter_complex` compiler
   (keyframe/timeline model) — the moat.
3. GPU workers (1–2w): g4dn Spot ASG + NVENC + warm pool.
4. AI layer (2–3w): Kokoro TTS pod + asset cache (Pexels/Unsplash) + opt FLUX thumbs.
5. Premium tier (opt): Remotion Automators ($0.01/render) behind same API — watch BSL.
