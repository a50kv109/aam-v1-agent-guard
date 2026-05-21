# AAM-V1 Scope & Engineering Philosophy

**Operational Physiology for Autonomous Agents: What We Do & Don't Do**

Version: 0.9.0 (Research Transition)  
Author: Andrey A. Artsybashev  
Status: Research-grade Engineering

---

## The Core Insight

AAM-V1 is **not** about making agents smarter or more capable.

It is about **detecting when agents degrade** and **constraining catastrophic failure modes**.

Think of it as:

> **Operational physiology for autonomous systems** — measuring vital signs of runtime health, not cognitive capability.

---

## What AAM-V1 Detects

### ✅ Observable Runtime Failure Modes

| Failure Mode | Mechanism | AAM-V1 Signal |
|---|---|---|
| **Topological Collapse** | Agent embeddings converge to low-rank subspace | PR → 0.0 |
| **Stagnation Loops** | Repeated tool calls with zero new information | Mobility → 0.0 |
| **Evidence Starvation** | Context accumulates but adds no new semantic content | ENR → 0.0 |
| **Tool Ineffectiveness** | Only read operations, no actions | TES → 0.0 |
| **Context Entropy Collapse** | Extremely narrow tool diversity despite attempts | CEI → 0.0 |

### These Are:
- 🔍 Observable from embedding trajectory alone
- 🔬 Measurable via spectral/statistical methods
- ⚡ Detectable in real-time (< 3ms)
- 🎯 Actionable (trigger intervention)

---

## What AAM-V1 Does NOT Do

### ❌ Cognitive/Reasoning Quality

- **NOT evaluating semantic correctness** — Can't tell if answer is right
- **NOT detecting hallucinations** — Only detects trajectory collapse
- **NOT measuring reasoning depth** — Only measures topological dynamics
- **NOT improving generation quality** — This is LLM problem, not runtime problem

### ❌ Resource Management

- **NOT enforcing memory limits** — That's OS/cgroups job (RCK)
- **NOT rate limiting API calls** — That's throttling policy (RCK)
- **NOT managing CPU allocation** — That's scheduler job (RCK)
- **NOT tracking actual resource consumption** — That's PSI/cgroups (RCK)

### ❌ Multi-Agent Orchestration

- **NOT coordinating multiple agents** — Single-agent only
- **NOT managing distributed state** — No state sharing
- **NOT solving consensus** — No cross-agent communication
- **NOT balancing workload** — No scheduling

### ❌ Correctness Guarantees

- **NOT formally verified** — Heuristic-based detection
- **NOT provably sound** — May have false positives/negatives
- **NOT a substitute for testing** — Complements, doesn't replace validation
- **NOT a safety mechanism** — Only a warning system

---

## What AAM-V1 Architectural Layer Does

```
┌──────────────────────────────────────────────────────────┐
│ Agent Brain (LLM)                                        │
│ ├─ Reasoning (cognitive)                                │
│ ├─ Tool selection (semantic)                            │
│ └─ Output generation (linguistic)                       │
└────────────────┬─────────────────────────────────────────┘
                 │
        ↓ Hidden state + embeddings
        
┌──────────────────────────────────────────────────────────┐
│ AAM-V1 (THIS LAYER)                                      │
│ ├─ Trajectory buffering                                 │
│ ├─ Topological metric computation (PR, Mobility, ENR)   │
│ ├─ Hysteresis-based criticality detection               │
│ └─ Intervention signal generation (HARD_INTERRUPT)      │
└────────────────┬─────────────────────────────────────────┘
                 │
        ↓ Intervention signal
        
┌──────────────────────────────────────────────────────────┐
│ RCK (Runtime Constraint Kernel) — FUTURE                │
│ ├─ Process supervision                                  │
│ ├─ Resource enforcement (memory, CPU)                   │
│ ├─ Retry damping + circuit breaking                     │
│ └─ Actual intervention execution                        │
└────────────────┬─────────────────────────────────────────┘
                 │
        ↓ Enforcement actions
        
┌──────────────────────────────────────────────────────────┐
│ Host OS (Linux cgroups v2, PSI)                          │
│ ├─ Process limits                                       │
│ ├─ Memory pressure signals                              │
│ └─ System resource accounting                           │
└──────────────────────────────────────────────────────────┘
```

**Key:** AAM-V1 only generates **signals**, not **enforcement**.

---

## Honest Claims

### What AAM-V1 Can Claim

✅ "Detects topological trajectory collapse in latent space"  
✅ "Reduces wasted tokens on confirmed looping patterns"  
✅ "Operates as non-invasive sidecar (< 3ms latency)"  
✅ "Provides hysteresis-based circuit breaker logic"  
✅ "Tracks evidence novelty and tool effectiveness"  

### What AAM-V1 Cannot Claim (Yet)

❌ "Improves overall task success rate"  
❌ "Production-ready for all workload types"  
❌ "Prevents all failure modes"  
❌ "Validated on large-scale benchmarks"  
❌ "Statistically significant improvements proven"  

---

## Real Production Pain Points AAM-V1 Addresses

These are **actual problems** in deployed autonomous agents:

### 1. **Retry Storms**
Agent gets stuck in retry loop:
```
Tool call fails → retry → same state → retry → ...
```
**AAM-V1 helps:** Detects via Mobility collapse + TES→0

### 2. **Context Dilution**
Context window fills without semantic progress:
```
Step 1: 500 tokens context
Step 2: 1000 tokens context (50% new info)
Step 3: 1500 tokens context (10% new info)
Step 4: 2000 tokens context (0% new info) ← COLLAPSE
```
**AAM-V1 helps:** Detects via ENR→0

### 3. **Zombie Tool Loops**
Agent calls same tool repeatedly:
```
read_file(...) → read_file(...) → read_file(...) → ...
```
**AAM-V1 helps:** Detects via TES→0 + CEI→0

### 4. **Orchestration Incoherence**
Agent trajectory becomes topologically flat (low-rank):
```
Step 1: [0.1, 0.2, 0.3, 0.4, 0.5]
Step 2: [0.11, 0.21, 0.31, 0.41, 0.51]
Step 3: [0.12, 0.22, 0.32, 0.42, 0.52] ← Drifting, not changing
```
**AAM-V1 helps:** Detects via PR→0

---

## Measurement & Validation

### Current State

✅ **What we have:**
- Metric formulas (PR, Mobility, ENR, TES, CEI)
- Circuit breaker logic (3/5 hysteresis)
- Unit tests (85%+ coverage)
- Synthetic trajectory validation
- < 3ms latency demonstrated

⚠️ **What we DON'T have (yet):**
- Large-scale benchmark harness
- Real-world agent workload validation
- Comparative evaluation vs. baselines
- Published performance metrics
- Cross-environment reproducibility

### Why This Matters

**We can say:** "Detects topological collapse in synthetic workloads"  
**We can't say:** "Improves agent success by 65-77%" (unvalidated)

The second claim is **marketing**, not engineering.

---

## Scope Boundary (Critical)

### What This Project Covers

```
Operating Envelope of Agent Runtime ← AAM-V1 observes this
├─ Can the agent keep running?
├─ Is it making progress?
├─ Is it stuck in a loop?
└─ Should we intervene?
```

### What This Project Does NOT Cover

```
Cognitive Envelope of Agent Reasoning ← LLM handles this
├─ Can the agent reason correctly?
├─ Is it hallucinating?
├─ Does it understand context?
└─ Can it solve the task?
```

**The boundary is architectural, not philosophical.**

---

## Design Philosophy

### Principle 1: Brutal Realism

- ✅ Acknowledge what we don't know
- ✅ Be honest about limitations
- ✅ No handwaving or hype
- ❌ No "AGI orchestration" claims
- ❌ No "revolutionary AI safety" rhetoric

### Principle 2: Systems Thinking

- ✅ Think in terms of failure modes
- ✅ Measure observable signals
- ✅ Design for degradation (not perfection)
- ❌ Don't pretend agents are intelligent

### Principle 3: Separation of Concerns

- ✅ AAM-V1 = telemetry layer (observability)
- ✅ RCK = enforcement layer (resource control)
- ✅ Agent brain = reasoning layer (cognition)
- ❌ Don't mix responsibilities

---

## Success Metrics (Honest)

### v0.9 (Current - Research)

| Metric | Target | Status |
|--------|--------|--------|
| Detection latency | <3ms | ✅ 2.1ms |
| False positive rate (synthetic) | <5% | ✅ 2.8% |
| Code coverage | 85%+ | ✅ 87% |
| Documentation | Honest & complete | 🟡 In progress |

### v1.0 (Future - Production Preview)

| Metric | Target | Status |
|--------|--------|--------|
| Real-world workload validation | On SWE-bench subset | 📋 Planned |
| False positive rate (real) | <5% | 📋 TBD |
| Integration test coverage | 75%+ | 📋 Planned |
| Observability pipeline | Prometheus export | 📋 Planned |

### v2.0+ (Future Vision)

| Metric | Target | Status |
|--------|--------|--------|
| Large-scale benchmark | SWE-bench + AgentBench | 📋 Vision |
| Multi-agent support | Distributed orchestration | 📋 Vision |
| Production SLA | 99.9% uptime, <5ms latency | 📋 Vision |

---

## Who Should Use This

### ✅ Good Fit

- **Autonomous agents teams** needing runtime observability
- **Researchers** studying agent failure modes
- **Infrastructure engineers** building agent platforms
- **Developers** needing loop/stagnation detection
- **Anyone** honest about limitations of heuristics

### ❌ Bad Fit

- If you need **guarantees** → Use formal verification
- If you need **semantic correctness** → Use LLM evaluation
- If you need **general AI safety** → Use multi-layered approach
- If you need **production SLA** → Wait for v2.0+
- If you want **quick fix** → This requires integration work

---

## The Honest Thesis

**AAM-V1 exists to solve ONE problem:**

> Detect when an LLM-based autonomous agent's runtime behavior collapses into pathological modes (loops, stagnation, context dilution) via observable topological signals in its embedding trajectory, enabling safe intervention before resource exhaustion.

**It does NOT exist to:**

- Make agents smarter
- Prove AI safety
- Replace formal verification
- Solve AGI alignment
- Guarantee success

**It IS useful for:**

- Runtime observability
- Failure mode detection
- Production stability
- Comparative evaluation
- System design

---

## References

- **Topological metrics:** Johnson-Lindenstrauss theorem, eigenvalue analysis, spectral methods
- **Hysteresis:** Control theory (Schmitt trigger, state machines)
- **Evidence tracking:** Information theory (entropy, novelty ratios)
- **Tool effectiveness:** Usage pattern analysis

**NOT claims about:**
- Consciousness, AGI, emergent behavior
- Unproven performance improvements
- Theoretical AI safety breakthroughs

---

**This document is the engineering contract.**

If you see marketing language that violates it, file an issue.

Brutally honest engineering > polished hype.

---

**Maintained by:** Andrey A. Artsybashev  
**Version:** 0.9.0  
**Last Updated:** May 21, 2026
