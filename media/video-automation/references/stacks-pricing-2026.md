# Stacks, Pricing & Licensing — verified 2026-08-08

Condensed data bank for DIY programmatic video rendering. Re-verify every price
against the cited source before any budget commitment; cloud/API prices drift.

## Render stacks

| Option | Compositing | ~Speed (1080p30) | $/min video (compute) | License | Build complexity |
|---|---|---|---|---|---|
| FFmpeg `filter_complex`+DSL | pixel graph | 5–15× RT (GPU) | ~$0.001 | GPL/LGPL (free) | High (build DSL) |
| editly | FFmpeg wrapper | 1–5× RT | ~$0.001 | MIT | Low |
| Remotion+Lambda | DOM/Chrome | minutes→pennies* | $0.01/render + AWS | BSL (paid auto tier) | High |
| Revideo | Canvas/Chrome | ~1× RT | EC2 only | MIT | Med-High |
| Motion Canvas | Canvas/Chrome | ~1× RT | EC2 only | MIT | High (no farm) |
| Chromium capture | web platform | 0.2–1× RT | EC2 | BSD (Chromium) | Medium |
| Blender/Manim | 3D/vector | 0.1–1× RT | EC2/GPU | GPL/MIT | High (niche) |

\* Remotion AWS cost is pennies; the **$0.01/render Automators fee** is the real
per-render business line item.

### Remotion (https://www.remotion.dev)
- Free License: individuals / companies **≤ 3 people**, unlimited commercial use.
- Companies **4+** need a license. For batch/automated products:
  **"Remotion for Automators" = $0.01/render + $100/mo minimum** (devs don't need a seat).
  Company License seats $25/seat/mo; Enterprise from $500/mo.
  Source: https://www.remotion.dev/docs/license/pricing , /docs/license/faq
- Lambda official cost examples (us-east-1): hello-world $0.001 warm; 1-min video
  ~$0.017 warm / $0.021 cold; 10-min HD ~$0.103 warm. Most users: "multiple
  minutes of video for just a few pennies."
- BSL non-compete: don't fork to sell a competing video product; using it as a
  dependency in your own service is fine.
- Escape hatch for MIT server-side React-style: **Revideo** (https://github.com/revideo/revideo).

### FFmpeg core
- CPU c6i.2xlarge (8 vCPU): ~1–3× RT for 1080p30 + overlays.
- GPU g4dn.xlarge (T4, NVENC): ~5–15× RT. On-demand ≈ $0.526/hr us-east-1
  (https://aws.amazon.com/ec2/pricing/on-demand/). At 10× RT: ~$0.0009/min compute.
- ⚠️ If shipping a *closed-source* product, build FFmpeg avoiding GPL-only
  components or keep rendering server-side (legal review advised).

### Revideo / Motion Canvas / editly
- Revideo (https://github.com/revideo/revideo, MIT): server-side Node API
  (`@revideo/renderer`, `renderVideo()`), REST-exposable. Fork of Motion Canvas.
- Motion Canvas (https://github.com/motion-canvas/motion-canvas, MIT): browser-only,
  no managed farm — self-host Playwright workers.
- editly (https://github.com/mifi/editly, MIT): declarative NLE on FFmpeg;
  low-complexity MVP, then graduate to custom DSL.

### Blender / Manim
- Blender (https://www.blender.org, GPL): 3D, Python (`bpy`); render to frames →
  FFmpeg. GPU nodes g4dn/g5.
- Manim (https://github.com/ManimCommunity/manim, MIT): math/diagram animation
  (3Blue1Brown style); PNG frames → ffmpeg. CPU-heavy, niche.

## Cloud render cost basis (us-east-1, on-demand)
- **Lambda**: x86 ≈ $0.0000133334/GB-second + $0.20/1M requests.
  Free tier: 400k GB-seconds + 1M requests/mo.
  Source: https://aws.amazon.com/lambda/pricing/
- **EC2 G4 (T4 GPU)**: g4dn.xlarge on-demand ≈ $0.526/hr (lowest-cost cloud GPU
  for inference/rendering). Spot ≈ 30% of on-demand (~$0.16/hr).
  Source: https://aws.amazon.com/ec2/instance-types/g4/
- **SQS**: Standard $0.40/1M requests; FIFO $0.50/1M; 1M free/mo.
  Source: https://aws.amazon.com/sqs/pricing/
- **S3 Standard**: $0.023/GB first 50TB (us-east-1). 100 GB free egress/mo.
  Source: https://aws.amazon.com/s3/pricing/

## Asset / AI layer pricing

### TTS
| Provider | Model | Price | Source |
|---|---|---|---|
| Kokoro | Kokoro-82M | $0 (compute only, Apache-2.0) | https://github.com/hexgrad/kokoro |
| OpenAI | tts-1 | $15 / 1M chars | https://platform.openai.com/docs/pricing |
| OpenAI | tts-1-hd | $30 / 1M chars | (same) |
| OpenAI | gpt-4o-mini-tts | $0.60/1M in + $12/1M audio tok (~$0.015/min) | https://platform.openai.com/docs/models/gpt-4o-mini-tts |
| ElevenLabs | V2/V2.5 | ~1 credit = 1 char; ~$0.15–0.20/1M at scale; Auto ~$5/min (Business) | https://elevenlabs.io/pricing |
| Azure | Standard Neural | $15 / 1M chars | https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/ |
| Azure | Custom Pro | $24/1M (Neural HD $48/1M); $52/compute-hr training | (same) |
| Azure | Free F0 | 0.5M chars/mo free | (same) |

Sanity: 1000 × 30s videos ≈ 500k chars → Kokoro $0, OpenAI/Azure ~$7.50,
ElevenLabs ~$0.09 at scale. TTS ≈ free vs. render compute.

### Image generation
- FLUX on Replicate: schnell $0.003/img, dev $0.030/img, pro $0.055/img
  (https://replicate.com/blog/flux-state-of-the-art-image-generation). FLUX 1.1
  Pro $0.04/img (https://replicate.com/pricing).
- Self-host FLUX (g5/g4dn, diffusers): EC2 only, ~$0.001–0.005/img amortized.
- OpenAI gpt-image-1: ~$0.011–0.080/img by size (Standard).

### Generative video (cost bomb — keep opt-in)
- OpenAI Sora 2: $0.10/sec (720p), $0.30/sec pro, up to $0.70/sec (1080p);
  Batch ½ price. Source: https://platform.openai.com/docs/pricing
  → 30s clip = $3.00; 1000 clips = $3,000.

## Stock / assets
- Footage/images: Pexels, Pixabay, Unsplash (CC0, REST APIs). Production:
  Storyblocks, Shutterstock, Getty. Cache in S3/GCS.
- Music/SFX: Artlist, Epidemic Sound, YouTube Audio Library, Pixabay Music.
- Fonts: Google Fonts (OFL), Fontsource (self-host via npm).
- Brand kit (colors/fonts/logo/lower-thirds/motion presets) as JSON = anti-slop moat.
