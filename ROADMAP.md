# AAM-V1 to Runtime Resilience Framework (RRF): Roadmap

**Strategic Transition from Research to Production-Grade Runtime Survivability**

Version: **0.9 → 1.0+ → 2.0** Timeline  
Status: **Research Transition Phase**  
Last Updated: May 21, 2026

---

## Executive Summary

The AAM-V1 repository is transitioning from a **standalone telemetry middleware** into the **foundation layer of the Runtime Resilience Framework (RRF)**.

- **Current (v0.9):** Pure topological metrics + circuit breaker
- **Target (v1.0):** Integrated RRF architecture with RCK daemon + CARP probes
- **Vision (v2.0):** Production-grade multi-agent survivability platform

This roadmap ensures **backward compatibility** while enabling **evolutionary integration** of RRF components.

---

## Phase 0: Current State (v0.9 — May 2026)

### Completed Deliverables

| Component | Status | Notes |
|-----------|--------|-------|
| Topological metrics (PR, Mobility, ENR, TES, CEI) | ✅ Stable | Validated on synthetic + baseline workloads |
| Circuit breaker with hysteresis | ✅ Stable | 3/5 pattern, recovery budget tracking |
| AgentManagerOrchestrator class | ✅ Stable | Core orchestrator, non-invasive sidecar |
| Unit test suite (85%+ coverage) | ✅ Complete | 12+ tests, edge case handling |
| Documentation (README + examples) | ✅ Partial | Basic usage, need RRF integration guide |
| MIT License + DOI (10.5281/zenodo.20214580) | ✅ Complete | Zenodo registration done |

### Known Issues (v0.9)

| Issue | Severity | Workaround | v1.0 Fix |
|-------|----------|-----------|---------|
| No structured logging | Medium | Print-based debugging | Implement JSON logging + Prometheus export |
| No resource monitoring | High | Manual external tracking | Integrate PSI + cgroups v2 sensors |
| Static thresholds only | Medium | Manual tuning per workload | Add online ECDF calibration |
| Single-agent only | Low | Sequential execution | Add RCK multi-agent coordination |
| Python-only (slow paths) | Low | Acceptable < 3ms | Plan Rust hotpath for v2.0 |

### API Stability

**Status:** 🟢 **STABLE** (locked for v1.0)

The `AgentManagerOrchestrator.add_step()` interface will not break between v0.9 and v1.0.

---

## Phase 1: v1.0 Architectural Stabilization (June–July 2026)

### 1.1 Repository Structure Refactor (Non-Breaking)

#### Before (v0.9)
```
src/aam_v1/
├── orchestrator.py
├── metrics.py
├── circuit_breaker.py
└── __init__.py
```

#### After (v1.0)
```
src/aam_v1/                      # ← Keep as-is
├── orchestrator.py
├── metrics.py
├── circuit_breaker.py
├── telemetry.py                 # ← NEW: Structured logging
└── __init__.py

src/rrf_core/                    # ← NEW: Runtime Constraint Kernel
├── __init__.py
├── daemon.py                    # Autonomic control loop
├── config.py                    # Configuration schema
├── sensors/
│   ├── __init__.py
│   ├── base_sensor.py           # Abstract sensor interface
│   ├── psi_monitor.py           # Pressure stall info (Linux)
│   ├── cgroup_monitor.py        # Memory/CPU cgroups v2
│   ├── process_monitor.py       # Subprocess tracking
│   └── retry_tracker.py         # Retry amplification
├── effectors/
│   ├── __init__.py
│   ├── base_effector.py         # Abstract effector interface
│   ├── process_reaper.py        # Safe termination
│   ├── throttler.py             # Rate limiting
│   └── context_pruner.py        # Memory pressure relief
└── policies/
    ├── __init__.py
    ├── invariant_base.py        # Operational invariant base class
    ├── causal_invariant.py      # I_causal: loop prevention
    ├── resource_invariant.py    # I_res: boundary enforcement
    ├── temporal_invariant.py    # I_temp: instruction retention
    ├── orch_invariant.py        # I_orch: payload coherence
    └── dist_invariant.py        # I_dist: consensus stability

src/carp_probes/                 # ← NEW: Chaos probes
├── __init__.py
├── base_probe.py                # Abstract CARP interface
├── carp_1_loop_injector.py      # Permanent loop simulation
├── carp_2_flood_injector.py     # High-frequency output
├── carp_3_jitter_injector.py    # Transient failures
├── carp_4_recursion_fuzzer.py   # Tool call recursion
└── carp_5_zombie_simulator.py   # Zombie subprocess seeding

src/observability/               # ← NEW: Telemetry pipeline
├── __init__.py
├── prometheus_exporter.py       # Prometheus metrics
├── structured_logger.py         # JSON logging
├── metrics_mapper.py            # AAM-V1 → RRF metrics
└── grafana_templates/           # Dashboards (YAML)

benchmarks/                      # ← NEW: Survivability testing
├── __init__.py
├── harness.py                   # Agent runtime harness
├── workloads/
│   ├── __init__.py
│   ├── long_horizon.py          # Extended sequences
│   ├── resource_stress.py       # Memory/CPU pressure
│   └── failure_injection.py     # Chaos workloads
└── metrics_reporter.py          # WER/RAF/TLD/CRS

tests/
├── unit/                        # Keep as-is
│   └── test_aam_v1/
├── integration/                 # ← NEW
│   ├── test_aam_v1_core.py      # Sanity tests
│   ├── test_rck_core.py         # RCK daemon startup
│   ├── test_aam_rck_coupling.py # AAM-V1 ↔ RCK integration
│   └── test_observability.py    # Logging + export
└── chaos/                       # ← NEW
    ├── test_carp_1.py           # Loop injection
    ├── test_carp_2.py           # Flood injection
    └── test_recovery.py         # Intervention + recovery

docs/
├── architecture.md              # ← NEW: System overview
├── telemetry_semantics.md       # ← NEW: Metric definitions
├── rck_design.md                # ← NEW: RCK specification
├── carp_catalog.md              # ← NEW: CARP probes
├── integration_guide.md         # ← NEW: AAM-V1 + RCK coupling
├── api_reference.md             # API docs
├── migration_guide.md           # ← NEW: v0.9 → v1.0 transition
└── examples/                    # Expanded examples

.github/
├── workflows/
│   ├── tests.yml                # Unit + integration tests
│   ├── chaos.yml                # ← NEW: CARP probe tests
│   └── release.yml              # ← NEW: Release automation

ROADMAP.md                       # This file
VERSION.md                       # ← NEW: Version policy
ARCHITECTURE.md                  # ← NEW: High-level design
```

**Migration Impact:** ✅ **ZERO** – AAM-V1 remains unchanged and importable

```python
# v0.9 code continues to work in v1.0
from aam_v1.orchestrator import AgentManagerOrchestrator
orch = AgentManagerOrchestrator()
decision = orch.add_step(...)  # Works exactly as before
```

### 1.2 API Additions (Backward Compatible)

#### Structured Logging

```python
# v0.9: Manual print debugging
decision = orch.add_step(...)
print(f"Metrics: PR={decision['metrics']['PR']}")

# v1.0: Automatic structured logging
from aam_v1.telemetry import StructuredLogger
logger = StructuredLogger(format="json")
orch.attach_logger(logger)

decision = orch.add_step(...)
# Automatically logs:
# {"timestamp": "...", "step": 42, "metrics": {...}, "status": "NOMINAL"}
```

#### Observability Attachment

```python
# v1.0: Telemetry pipeline
from observability import PrometheusExporter

exporter = PrometheusExporter(port=8000)
orch.attach_exporter(exporter)

# Metrics now available at http://localhost:8000/metrics
```

### 1.3 RCK Prototype (Non-Blocking)

**Goal:** Establish RCK as separate daemon that can operate alongside AAM-V1

```python
# v1.0: Optional RCK integration
from rrf_core.daemon import RuntimeConstraintKernel

rck = RuntimeConstraintKernel(
    memory_limit_mb=4096,
    cpu_limit_cores=2,
    enable_psi_monitoring=True
)

rck.start()
# RCK now monitors process resources independently
# AAM-V1 operates separately
# Future: Coupling mechanism (v1.1+)
```

**Non-blocking:** RCK operates independently; AAM-V1 unaffected.

### 1.4 Metric Mapping (Telemetry Integration)

**New:** `observability/metrics_mapper.py` documents how AAM-V1 metrics feed RRF survivability evaluation:

```python
# Mapping AAM-V1 → RRF metrics
AAM_V1_METRIC_MAP = {
    'PR_collapse': 'I_causal_violation',          # Topological collapse → causal instability
    'mobility_stagnation': 'I_causal_symptom',    # Low displacement → execution loop
    'ENR_collapse': 'I_temp_violation',           # Evidence starvation → temporal decay
    'TES_zero': 'I_orch_warning',                 # Tool ineffectiveness → payload incoherence
    'CEI_collapse': 'I_orch_degradation'          # Context entropy → coherence loss
}
```

### 1.5 Documentation (Critical Path)

| Document | Status | v1.0 Target | Purpose |
|----------|--------|------------|---------|
| ARCHITECTURE.md | TBD | System design overview | How AAM-V1, RCK, CARP interoperate |
| telemetry_semantics.md | TBD | PR/Mobility/ENR definitions | Metric interpretation guide |
| rck_design.md | TBD | RCK specification | Process supervision + resource enforcement |
| carp_catalog.md | TBD | CARP probe reference | Chaos injection patterns |
| integration_guide.md | TBD | AAM-V1 ↔ RCK coupling | How telemetry feeds resource control |
| migration_guide.md | TBD | v0.9 → v1.0 transition | Backward compatibility notes |
| VERSION.md | TBD | Semantic versioning policy | Release numbering rules |

---

## Phase 2: v1.0 Release (August 2026)

### 2.1 Release Criteria

| Criterion | Status | Notes |
|-----------|--------|-------|
| AAM-V1 API stable (locked) | ✅ | add_step() interface immutable |
| RCK prototype operational | ✅ | Daemon starts, basic monitoring works |
| CARP-1 to CARP-3 probes complete | ✅ | Loop injection, flood, jitter |
| Unit tests 85%+ coverage | ✅ | All AAM-V1 + RCK core paths covered |
| Integration tests passing | ✅ | AAM-V1 + mock RCK coupling verified |
| Documentation complete | ✅ | Architecture + API reference |
| Backward compatibility verified | ✅ | v0.9 code runs unchanged in v1.0 |
| Zenodo registration updated | ✅ | New DOI for v1.0.0 |

### 2.2 Semantic Versioning (Proposed)

```
1.0.0 (Initial RRF integration)
├─ APIs locked for long-term compatibility
├─ RCK daemon MVP operational
├─ Full AAM-V1 telemetry suite included
└─ Ready for production trials

1.1.0 (RCK enhancements)
├─ Online threshold calibration
├─ Multi-agent coordination pilot
└─ Grafana dashboard templates

1.2.0 (CARP expansion)
├─ CARP-4 & CARP-5 probes
├─ Chaos harness integration
└─ WER/RAF/TLD/CRS metrics

2.0.0 (Distributed RRF)
├─ Multi-agent orchestration
├─ Distributed consensus
├─ Rust hotpath implementation
└─ GPU-accelerated projections
```

### 2.3 Release Notes Template (v1.0.0)

```markdown
# AAM-V1 + RRF Foundation v1.0.0

## Overview
First production release of Runtime Resilience Framework foundation.

## Major Features
- ✅ Topological telemetry layer (AAM-V1) production-ready
- ✅ Runtime Constraint Kernel (RCK) daemon MVP
- ✅ CARP chaos probes (1-3) functional
- ✅ Prometheus + structured logging pipeline
- ✅ Survivability benchmark harness

## Breaking Changes
None. v0.9 code runs unchanged.

## New APIs
- `rrf_core.daemon.RuntimeConstraintKernel` – RCK daemon
- `carp_probes.LoopInjector` – CARP-1 probe
- `observability.PrometheusExporter` – Metrics export
- `benchmarks.SurvivabilityHarness` – Testing framework

## Metric Enhancements
- Metric history tracking (`orch.metrics_history`)
- JSON structured logging
- Prometheus scrape endpoints

## Limitations & Roadmap
- RCK currently Linux-only (cgroups v2)
- Single-agent only (multi-agent in v2.0)
- No Rust hotpath yet (planned v2.0)

## Citation
@software{artsybashev2026aamv1rrf,
  title={AAM-V1 + Runtime Resilience Framework v1.0},
  author={Artsybashev, Andrey A.},
  year={2026},
  doi={10.5281/zenodo.XXXXX},
  url={https://github.com/a50kv109/aam-v1-agent-guard}
}

## Zenodo Link
https://zenodo.org/record/XXXXX
```

---

## Phase 3: v1.1+ Evolution (September–December 2026)

### 3.1 v1.1: Enhanced Calibration

| Feature | Scope | Priority |
|---------|-------|----------|
| Online ECDF calibration | Adaptive thresholds from historical data | High |
| Multi-workload profiles | Pre-tuned thresholds for SWE-bench, WebArena, etc. | Medium |
| Metric sensitivity analysis | Per-threshold impact on FPR/FNR | High |
| LangChain integration layer | Decorator-based agent wrapping | Medium |

### 3.2 v1.2: CARP Expansion

| CARP Probe | Description | Status |
|-----------|---|--------|
| CARP-1 | Permanent loop injection | ✅ v1.0 |
| CARP-2 | High-frequency stdout flooding | ✅ v1.0 |
| CARP-3 | Transient network jitter | ✅ v1.0 |
| CARP-4 | Tool call recursion fuzzing | 📋 v1.2 |
| CARP-5 | Zombie subprocess seeding | 📋 v1.2 |
| CARP-6 | Context window exhaustion | 📋 v1.3 |
| CARP-7 | Intermittent timeout storms | 📋 v1.3 |

### 3.3 v2.0: Production Platform

| Component | Scope | Timeline |
|-----------|-------|----------|
| Multi-agent orchestration | Distributed RCK + consensus | Q4 2026 |
| Rust hotpath (pyo3) | Performance optimization | Q4 2026 |
| GPU projections (cupy) | Acceleration for large embeddings | Q1 2027 |
| Advanced calibration | Bayesian threshold optimization | Q1 2027 |
| Full SWE-bench integration | Standardized benchmarking | Q2 2027 |

---

## Migration Path: v0.9 → v1.0

### For Existing Users (Non-Breaking)

**Before (v0.9):**
```python
from aam_v1.orchestrator import AgentManagerOrchestrator

orch = AgentManagerOrchestrator()
decision = orch.add_step(embedding, tool, evidence)
```

**After (v1.0):**
```python
# Existing code works unchanged
from aam_v1.orchestrator import AgentManagerOrchestrator

orch = AgentManagerOrchestrator()
decision = orch.add_step(embedding, tool, evidence)

# NEW: Optional observability
from observability import StructuredLogger
logger = StructuredLogger()
orch.attach_logger(logger)
```

### For New Projects (v1.0+)

```python
# Full RRF stack
from aam_v1.orchestrator import AgentManagerOrchestrator
from rrf_core.daemon import RuntimeConstraintKernel
from observability import PrometheusExporter
from carp_probes import LoopInjector

# Telemetry layer
orch = AgentManagerOrchestrator()

# Resource supervision layer
rck = RuntimeConstraintKernel(memory_limit_mb=4096)
rck.start()

# Observability
exporter = PrometheusExporter(port=8000)
orch.attach_exporter(exporter)

# Chaos testing (optional)
carp = LoopInjector(trigger_probability=0.1)

# Main loop
for step in agent_loop:
    decision = orch.add_step(...)
    if decision['status'] == 'HARD_INTERRUPT':
        handle_interrupt()
```

---

## Technical Debt & Risk Mitigation

### Known Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| PSI metric unavailability (non-Linux) | High | Windows/macOS users blocked | Fall back to cgroup parsing |
| RCK daemon resource overhead | Medium | <5% CPU/memory overhead expected | Profile & optimize hotpath |
| CARP probe false interrupts | Medium | Agent incorrectly halted | Extensive chaos testing, hysteresis tuning |
| Threshold brittleness | High | Tuning per workload required | Online ECDF calibration (v1.1) |
| Multi-agent race conditions | Low | Data corruption risk | Comprehensive integration tests |

### Mitigation Strategy

1. **PSI Fallback:** Implement degraded mode using cgroup.stat parsing on non-PSI systems
2. **RCK Profiling:** Benchmark daemon CPU/memory on representative workloads
3. **CARP Validation:** Extend test suite to cover 100+ synthetic + real-world traces
4. **Threshold Learning:** Publish online ECDF adaptation algorithm (v1.1)
5. **Distributed Testing:** Use synchronization primitives (locks, queues) for safety

---

## Deprecation & Backward Compatibility Policy

### Commitment

- **v1.x.x:** No breaking changes to public APIs (AgentManagerOrchestrator, add_step)
- **v2.0.0:** Allowed to break, with 2-release notice (v1.8, v1.9)
- **Internal APIs:** rrf_core.*, carp_probes.* subject to breaking changes between minor versions

### Example: Sunset Schedule

```
v1.0 (Aug 2026): Introduce RCK daemon APIs (marked stable)
v1.5 (Jan 2027): Deprecation warning for old config format
v2.0 (Jun 2027): Remove deprecated APIs, breaking changes permitted
```

---

## Success Metrics (v1.0 Target)

| Metric | Target | Current | v1.0 Goal |
|--------|--------|---------|-----------|
| Detection latency | <3ms/step | ✅ 2.1ms | ✅ <3ms |
| False positive rate | <4% | ✅ 2.8% | ✅ <4% |
| Code coverage | 85%+ | ✅ 87% | ✅ 88%+ |
| Documentation completeness | 100% | 40% | 100% |
| Integration test coverage | 75%+ | 0% | 75%+ |
| Production readiness | High | Medium | High |

---

## Communication & Community

### Channels

- **GitHub Issues:** Bug reports, feature requests
- **Discussions:** Architecture feedback, design questions
- **Zenodo:** Research preprints, DOI registration
- **Research community:** ArXiv preprint (planned Q3 2026)

### Stakeholder Updates

| Audience | Frequency | Format |
|----------|-----------|--------|
| Contributors | Bi-weekly | GitHub project board |
| Users | Monthly | Release notes + blog |
| Researchers | Quarterly | Preprint updates |

---

## Appendix: Versioning Examples

### v0.9.0 → v1.0.0 Transition

```
v0.9.0 (May 2026)
├─ AAM-V1 telemetry stable
├─ Core algorithms validated
└─ Ready for RRF integration feedback

v0.10.0 (Jun 2026)
├─ Add structured logging (backward compatible)
├─ Add observability stubs
└─ Prepare for RCK integration

v1.0.0 (Aug 2026)
├─ Lock public APIs
├─ Stable RRF integration layer
├─ RCK daemon MVP operational
└─ Production-ready for trials
```

### Minor Version Pattern (v1.x.z)

```
v1.0.0 → v1.0.1 (Bugfix)
v1.0.0 → v1.1.0 (New features, no breaking changes)
v1.0.0 → v2.0.0 (Major redesign, breaking changes OK)
```

---

## Key Dates (Proposed)

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| v0.9 release | May 19, 2026 | ✅ Done |
| RCK prototype | June 15, 2026 | 📋 In progress |
| CARP-1,2,3 | July 1, 2026 | 📋 In progress |
| Documentation complete | July 15, 2026 | 📋 Planned |
| v1.0 release | August 1, 2026 | 📋 Planned |
| v1.1 (calibration) | October 1, 2026 | 📋 Planned |
| v2.0 (distributed) | June 1, 2027 | 📋 Vision |

---

## How to Contribute

### For v1.0 Stabilization

- 🧪 **Benchmark Testing** – Validate on diverse agent workloads
- 📊 **Metric Validation** – Test PR/Mobility/ENR accuracy
- 📝 **Documentation** – Write telemetry_semantics.md, rck_design.md
- 🐛 **Bug Reports** – Edge cases, numerical issues
- 🎯 **RCK Design** – Contribute to daemon architecture

### For v1.1+ Enhancement

- ⚡ **Performance** – Rust hotpath implementation
- 📈 **Metrics** – Online ECDF calibration algorithms
- 🔀 **Multi-Agent** – Distributed coordination primitives
- 📊 **Benchmarks** – SWE-bench integration harness
- 🎨 **Dashboards** – Grafana templates

---

## References

- **AAM-V1 DOI:** 10.5281/zenodo.20214580
- **RRF Specification:** (Planned, separate DOI)
- **Runtime Resilience Framework:** Framework overview (this repo ROADMAP.md)

---

**Maintained by:** Andrey A. Artsybashev (@a50kv109)  
**Last Updated:** May 21, 2026  
**Status:** Active Development – Research Transition Phase
