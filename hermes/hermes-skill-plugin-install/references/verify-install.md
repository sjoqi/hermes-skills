# Verify a Hermes skill/plugin install actually loaded

Don't trust the install command's "✓ Installed" banner — confirm discovery.

## 1. CLI discovery (cheap, first check)
```bash
hermes skills list | grep -i omh          # shows: name | category | source | state | enabled
hermes plugins list | grep -i omh         # shows: name | enabled | version | description | source
```
Skills should show `enabled`. Plugin should show `enabled` and a non-zero
tools/hooks count (e.g. `tools=2, hooks=3`).

## 2. Definitive load check (loads the real PluginManager)
Run via Hermes's venv Python so you hit the same code the agent uses:
```bash
/Users/you/.hermes/hermes-agent/venv/bin/python - <<'PY'
import sys
sys.path.insert(0, "/Users/you/.hermes/hermes-agent")
from hermes_cli.plugins import PluginManager
pm = PluginManager()
pm.discover_and_load()
for p in pm._plugins.values():
    if "omh" in p.manifest.name:
        print(p.manifest.name, "| enabled=", p.enabled,
              "| tools=", p.tools_registered, "| hooks=", p.hooks_registered)
PY
```
Expected output for a healthy OMH install:
```
omh | enabled=True | tools=['omh_gather_evidence', 'omh_state'] | hooks=['pre_llm_call', 'on_session_end', 'pre_tool_call']
```

## 3. Skill tree sanity (auto-discovery path)
```bash
/Users/you/.hermes/hermes-agent/venv/bin/python - <<'PY'
from pathlib import Path
base = Path.home() / ".hermes" / "skills"
omh = sorted(p.parent.name for p in base.rglob("SKILL.md") if p.parent.name.startswith("omh-"))
print(omh, "count:", len(omh))
PY
```
OMH ships 10: omh-autopilot, omh-deep-interview, omh-deep-research, omh-ralph,
omh-ralph-driver, omh-ralph-task, omh-ralplan, omh-ralplan-driver, omh-triage,
omh-triage-driver.

## 4. Config persistence
```bash
grep -n "plugins:" -A4 ~/.hermes/config.yaml
```
Expect:
```yaml
plugins:
  enabled:
    - omh
  disabled: []
```
