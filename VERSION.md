# AAM-V1 / RRF Semantic Versioning & Release Policy

**Official Version Strategy for AAM-V1 and Runtime Resilience Framework Integration**

Version: 1.0  
Effective: May 21, 2026  
Governed by: [Semantic Versioning 2.0.0](https://semver.org/)

---

## Quick Reference

| Version Range | Phase | Breaking Changes | API Stability | Upgrade Risk |
|---|---|---|---|---|
| **0.y.z** | Research | Allowed | Volatile | High |
| **1.y.z** | Stable | Disallowed (except 1→2) | Locked | Low |
| **2.y.z** | Production+ | Allowed (with notice) | Evolving | Medium |

---

## Core Versioning Scheme

### Semantic Version: `MAJOR.MINOR.PATCH`

```
1.2.3
│ │ └─ PATCH: Bugfixes, internal optimization, docs
│ └──── MINOR: New features, deprecations, non-breaking changes
└────── MAJOR: Breaking changes, architectural shifts
```

### Application to AAM-V1 / RRF

| Component | Version | Stability | Lock Status |
|-----------|---------|-----------|---|
| **AAM-V1** (Telemetry Layer) | 0.9 → 1.0 → 1.x | Stable from v1.0 | Locked in v1.x |
| **RRF Framework** (Meta-Architecture) | 0.1 → 1.0 → 2.0 | Stable from v1.0 | Locked in v1.x |
| **RCK** (Runtime Constraint Kernel) | 0.1 → 1.0+ | Evolving (v1.x) | Flexible |
| **CARP** (Chaos Probes) | 0.1 → 1.0+ | Evolving (v1.x) | Flexible |

---

## Phase-Based Rules

### Phase 0: Research (v0.y.z)

**Duration:** Pre-production research phase  
**Current:** May 2026 (v0.9)  
**Ends:** August 1, 2026 (→ v1.0)

**Rules:**
- ✅ Breaking changes allowed with notice
- ✅ Experimental APIs encouraged
- ⚠️ Not recommended for production
- ⚠️ Frequent API changes expected
- 📝 Release notes **must** call out migration paths

**Example:** v0.9 → v0.10 may change `AgentManagerOrchestrator.__init__()` signature

### Phase 1: Stable (v1.y.z)

**Duration:** Production-ready, API-locked phase  
**Start:** August 1, 2026 (v1.0)  
**Duration:** ~2 years (until v2.0)

**Rules:**
- 🔒 **NO breaking changes** to public APIs
- ✅ New features via backward-compatible additions
- ✅ Deprecations with warnings (3-release grace period)
- ✅ Internal refactoring allowed
- 📋 Changelog **must** note any deprecations

**Locked APIs in v1.x:**
```python
# These signatures MUST NOT change until v2.0
from aam_v1.orchestrator import AgentManagerOrchestrator

orch = AgentManagerOrchestrator(
    window_size=8,
    recovery_budget=3,
    pr_threshold=0.32,
    mobility_threshold=0.09,
    enr_threshold=0.07
)

decision = orch.add_step(
    thought_embedding: np.ndarray,
    tool_name: str,
    new_evidence_tokens: int,
    verification_score: float = 1.0
) -> Dict[str, Any]
```

**Flexible APIs in v1.x** (may change):
```python
from rrf_core.daemon import RuntimeConstraintKernel  # NEW in v1.0
from carp_probes import LoopInjector                  # NEW in v1.0
# These are internal/new; backward compatibility NOT guaranteed
```

### Phase 2: Production (v2.y.z)

**Duration:** Long-term support, multi-agent platform  
**Target:** June 2027 (v2.0)  
**Duration:** ~5+ years (until v3.0)

**Rules:**
- 🔒 **NO breaking changes** to public APIs (same as v1.y.z)
- ✅ Deprecations must have 4-release notice before removal
- ✅ Major architectural changes allowed with major version bump
- 📊 Full SWE-bench + WebArena integration expected

---

## Specific Rules by Component

### AAM-V1 (Telemetry Layer)

| Aspect | Rule | Rationale |
|--------|------|-----------|
| `orchestrator.py` | Locked in v1.x | Core public API |
| `metrics.py` | Locked in v1.x | Metric definitions |
| `circuit_breaker.py` | Locked in v1.x | Control flow logic |
| Metric definitions (PR, ENR, etc.) | Locked in v1.x | Research dependencies |
| Threshold defaults (0.32, 0.09, etc.) | May tune in v1.x | Empirical calibration OK |

**Exception:** New optional parameters allowed if backward-compatible
```python
# v1.0
orch = AgentManagerOrchestrator(window_size=8, recovery_budget=3)

# v1.1 (OK: backward compatible)
orch = AgentManagerOrchestrator(
    window_size=8,
    recovery_budget=3,
    enable_metrics_history=True  # NEW, default False for compat
)

# v2.0 WOULD NOT (breaks existing code)
def __init__(self, config: Config):  # Changed signature!
    ...
```

### RCK (Runtime Constraint Kernel)

| Aspect | Rule | Rationale |
|--------|------|-----------|
| Daemon startup interface | Experimental in v1.x | Still evolving |
| Sensor types | May add in v1.x | Extensible design |
| Effector policies | May refactor in v1.x | Optimization phase |
| Public daemon API | Should stabilize by v1.5 | Before v2.0 lock |

**Recommendation:** Use via high-level `rrf_core.config.Config` to buffer changes

### CARP Probes (Chaos Engineering)

| Aspect | Rule | Rationale |
|--------|------|-----------|
| Probe interfaces | May evolve in v1.x | Experimental |
| CARP-1 through CARP-3 | Stabilize by v1.2 | Core probes |
| CARP-4 through CARP-7 | Research in v1.x | May not ship |
| Injection patterns | May refactor in v1.x | Still learning |

---

## Deprecation Lifecycle

### Example: Deprecating Old API (v1.5 → v2.0)

```python
# v1.4 (works, no warning)
orch = AgentManagerOrchestrator()
old_method_name()

# v1.5 (works, DEPRECATED warning)
import warnings
warnings.warn(
    "old_method_name() is deprecated, use new_method_name()",
    DeprecationWarning,
    stacklevel=2
)

# v1.9 (works, stronger warning)
warnings.warn(
    "old_method_name() will be removed in v2.0",
    PendingDeprecationWarning,
    stacklevel=2
)

# v2.0 (removed entirely)
# AttributeError: ... has no attribute 'old_method_name'
```

**Grace Period:** 4 releases minimum (v1.5 → v1.6 → v1.7 → v1.8 → v1.9)

---

## Breaking Changes: Policy & Exception Process

### Definition: What is "Breaking"?

**Breaking (forbidden in v1.x):**
- ❌ Changing function signature (required params, types)
- ❌ Moving/renaming public classes
- ❌ Changing return type of public methods
- ❌ Removing public APIs without deprecation period
- ❌ Changing metric calculation logic (PR, ENR, etc.)

**Not Breaking (allowed in v1.x):**
- ✅ Adding optional parameters (with defaults)
- ✅ Adding new public methods/classes
- ✅ Internal code refactoring
- ✅ Bug fixes that align behavior with documentation
- ✅ Tuning threshold defaults (0.32 → 0.30, documented)
- ✅ Adding dependencies (if optional)

### Exception Process

If a breaking change is **critical for security/correctness**:

1. **Proposal:** Issue with `[BREAKING]` tag, detailed justification
2. **Community Comment:** 2-week comment period
3. **Steering Review:** (if applicable) Approve or request mitigation
4. **Deprecation Path:** Plan 4-release deprecation cycle
5. **Release as v2.0:** Document in migration guide

---

## Release Cadence

### Patch Releases (v1.x.z)

**Trigger:** Bugfix, security patch, documentation update  
**Frequency:** As needed (typically monthly)  
**Timeline:** 1-2 weeks from merge to release  
**Scope:** No new features

**Example:**
- v1.0.0 (Aug 1) → v1.0.1 (Aug 15, fixes numerical edge case)
- v1.0.1 → v1.0.2 (Sep 5, improves error message)

### Minor Releases (v1.y.0)

**Trigger:** New feature, optimization, deprecation  
**Frequency:** Every 6-8 weeks (2–3 per year)  
**Timeline:** 4-6 weeks of development + QA  
**Scope:** New features, backward-compatible improvements

**Example:**
- v1.0.0 (Aug) → v1.1.0 (Oct): Online ECDF calibration
- v1.1.0 → v1.2.0 (Dec): CARP-4 + CARP-5 probes

### Major Releases (v2.0.0)

**Trigger:** Architectural overhaul, breaking changes justified  
**Frequency:** Every 18–24 months  
**Timeline:** 6+ months of planning + development  
**Scope:** Disruptive changes allowed (with migration guide)

**Example:**
- v1.y.z (2026–2027) → v2.0.0 (June 2027): Multi-agent RRF, distributed coordination

---

## Release Process

### 1. Pre-Release (2 weeks before)

- [ ] Create `release/v1.x.y` branch
- [ ] Update version in `src/aam_v1/__init__.py`
- [ ] Update CHANGELOG.md (from Git history)
- [ ] Update ROADMAP.md (next milestones)
- [ ] Run full test suite + coverage
- [ ] Create prerelease tag `v1.x.y-rc1` if major

### 2. Release Candidate (if major)

- [ ] Announce RC on GitHub + community channels
- [ ] Gather feedback (1 week)
- [ ] Apply fixes → create RC2, RC3 as needed
- [ ] Finalize → create release tag

### 3. Release

- [ ] Create GitHub Release (auto-generate notes from PRs)
- [ ] Build + test wheel package
- [ ] Update PyPI (when v1.0+)
- [ ] Update Zenodo metadata (new DOI)
- [ ] Announce release across channels

### 4. Post-Release

- [ ] Pin docs to released version
- [ ] Create summary blog post (for major)
- [ ] Monitor for urgent issues
- [ ] Plan patch if needed

---

## Example Release Notes Template

### v1.0.0 Release Notes

```markdown
# AAM-V1 + Runtime Resilience Framework v1.0.0

**Released:** August 1, 2026

## Summary
First production release of AAM-V1 telemetry layer + RRF foundation architecture.

## What's New in v1.0.0

### Features
- ✅ Production-hardened `AgentManagerOrchestrator` class
- ✅ RCK daemon prototype (Linux cgroups v2)
- ✅ CARP-1, CARP-2, CARP-3 chaos probes
- ✅ Prometheus metrics export
- ✅ Structured JSON logging
- ✅ Full RRF integration documentation

### Metrics & Performance
- Detection latency: **< 3ms/step** on CPU
- False positive rate: **< 4%** on baseline workloads
- Test coverage: **88%** of core paths
- Memory overhead: **O(window_size × embedding_dim)**, typically < 50MB

### Backward Compatibility ✅
v0.9 code runs unchanged:
```python
from aam_v1.orchestrator import AgentManagerOrchestrator
orch = AgentManagerOrchestrator()
decision = orch.add_step(...)  # Works exactly as before
```

## Breaking Changes
**None.** All v0.9 APIs preserved with full compatibility.

## New APIs
- `rrf_core.daemon.RuntimeConstraintKernel` – RCK daemon
- `carp_probes.LoopInjector` – CARP-1 probe
- `observability.PrometheusExporter` – Prometheus export
- `src.aam_v1.telemetry.StructuredLogger` – JSON logging

## Documentation
- 📖 **Architecture Guide:** docs/architecture.md
- 📖 **Integration Guide:** docs/integration_guide.md
- 📖 **API Reference:** docs/api_reference.md
- 📖 **Migration from v0.9:** docs/migration_guide.md

## Limitations & Roadmap
- RCK currently Linux-only (cgroups v2 required)
- Single-agent orchestration (multi-agent in v2.0)
- Python implementation (Rust hotpath planned v2.0)
- See ROADMAP.md for v1.1–v2.0 priorities

## Citation
```
@software{artsybashev2026aamv1rrf,
  title={AAM-V1: Topological Telemetry + Runtime Resilience Framework v1.0},
  author={Artsybashev, Andrey A.},
  year={2026},
  doi={10.5281/zenodo.XXXXX},
  url={https://github.com/a50kv109/aam-v1-agent-guard}
}
```

## Thank You 🙏
Thanks to all contributors and early adopters for feedback on v0.9!

---

**Changelog:** See CHANGELOG.md for detailed commit history  
**Documentation:** https://github.com/a50kv109/aam-v1-agent-guard  
**Issues:** https://github.com/a50kv109/aam-v1-agent-guard/issues
```

---

## Version Support Matrix

### Active Support

| Version | Released | Status | Until |
|---------|----------|--------|-------|
| v1.0.x | Aug 2026 | Maintenance | v1.5 |
| v1.1.x | Oct 2026 | Active | v1.6 |
| v1.2.x | Dec 2026 | Active | v1.7 |
| v1.3.x | Feb 2027 | Active | v1.8 |
| v1.4.x | Apr 2027 | Active | v1.9 |
| v1.5.x | Jun 2027 | Active | v2.0 |

### EOL Schedule

- **v0.9.z:** EOL immediately upon v1.0 release
- **v1.x.z:** EOL 6 months after v2.0 release
- **v2.x.z:** EOL 12 months after v3.0 release

---

## Governance

### Who Decides Version Numbers?

- **Patch (v1.x.Z):** Maintainer discretion
- **Minor (v1.Y.z):** Maintainer + contributor consensus
- **Major (v2.0.0):** Maintainer + steering committee (if exists)

### Version Review Checklist

Before releasing v1.0.0 or major releases:

- [ ] All tests passing (100% of CI)
- [ ] Code coverage ≥ 85%
- [ ] CHANGELOG.md complete
- [ ] ROADMAP.md updated
- [ ] Migration guide (if breaking)
- [ ] Documentation reviewed
- [ ] Zenodo DOI prepared
- [ ] Release notes drafted
- [ ] Community notified

---

## Frequently Asked Questions

### Q: Will AAM-V1 public APIs break before v2.0?
**A:** No. v1.x locks public APIs; breaking changes forbidden until v2.0 (June 2027+).

### Q: Can I rely on threshold defaults (0.32, 0.09)?
**A:** Yes. These are part of the public API contract and won't change without major version bump.

### Q: How do I migrate from v0.9?
**A:** No migration needed! v1.0 is 100% backward compatible. Just `pip install --upgrade aam-v1-agent-guard`.

### Q: When will RRF be "production ready"?
**A:** v1.0.0 is production-ready for **telemetry layer only** (AAM-V1). RCK daemon is MVP; full production support targets v2.0.

### Q: Can RCK/CARP APIs change in v1.x?
**A:** Yes. They're experimental. Lock targets v1.5+ before v2.0 freeze.

### Q: What if I find a critical bug that requires breaking change?
**A:** Follow exception process: propose on GitHub, discuss, plan deprecation cycle (4 releases min).

---

## References

- **Semantic Versioning 2.0.0:** https://semver.org/
- **Python PEPs:** PEP 440 (Version Scheme), PEP 387 (Backward Compat)
- **RRF Roadmap:** ROADMAP.md (this repo)
- **Changelog:** CHANGELOG.md

---

**Effective:** May 21, 2026  
**Last Reviewed:** May 21, 2026  
**Maintained by:** Andrey A. Artsybashev (@a50kv109)
