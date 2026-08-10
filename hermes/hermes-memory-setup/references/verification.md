# Holographic provider — E2E verification recipe

Run against the Hermes VENV Python (NOT system python3). On this Mac:
- system `python3` = 3.9 (plugins use 3.10+ syntax → import fails there)
- real runtime = `/Users/<you>/.hermes/hermes-agent/venv/bin/python3` (3.11.x)

Prereq: `pip install numpy` into that venv (HRR algebra is numpy-gated).

```bash
VENV_PY=/Users/<you>/.hermes/hermes-agent/venv/bin/python3
$VENV_PY - <<'PY'
import sys, os
sys.path.insert(0, "/Users/<you>/.hermes/hermes-agent")
from plugins.memory.holographic.store import MemoryStore
from plugins.memory.holographic.retrieval import FactRetriever

db = "/tmp/holo_verify.db"
if os.path.exists(db): os.remove(db)
s = MemoryStore(db_path=db)
s.add_fact("G prefers free, local, zero-dependency tooling", category="preference", tags="G,cost")
s.add_fact("Hermes routing uses provider nous for free and paid", category="routing", tags="hermes")
s.add_fact("G runs solo-dev microSaaS build, cap $50/mo", category="project", tags="G,build")
r = FactRetriever(s)
assert len(r.search("G tooling")) >= 1, "FTS5 search failed"
assert len(r.probe("G")) >= 2, "probe failed"
assert len(r.reason(["G","cost"])) >= 1, "reason failed"
row = s._conn.execute("SELECT hrr_vector IS NOT NULL AS v FROM facts WHERE fact_id=1").fetchone()
assert bool(row["v"]), "hrr_vector null — numpy missing"
s.close(); os.remove(db)
print("HOLOGRAPHIC E2E: PASS")
PY
```

Expected output: `HOLOGRAPHIC E2E: PASS`
If `hrr_vector null` → numpy not in the venv. If import `TypeError: str | None` →
running under wrong python. If `RuntimeError: numpy is required` → HRR path hit
without numpy (tool layer swallows it as error-JSON, so the provider still shows
"available" but probe/reason are dead).

Also confirm config wiring:
```bash
hermes memory status        # Provider: holographic, installed ✓, available ✓
grep -n hermes-memory-store ~/.hermes/config.yaml   # block at lines ~228-232
```
