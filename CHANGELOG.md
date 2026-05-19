# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-19

### Added

- **Initial release** of AAM-V1: Topological Telemetry and Evidence-Based Runtime
- Core `AgentManagerOrchestrator` class with:
  - Participation Ratio (PR) metric via spectral analysis
  - Mobility metric (centroid displacement)
  - Evidence Novelty Ratio (ENR) tracking
  - Tool Effectiveness Score (TES) computation
  - Context Entropy Index (CEI) calculation
  - Hysteresis-based circuit breaker (3/5 pattern)
  - Cold-start protection (window accumulation)
  - Recovery budget management
  - Hard interrupt for trajectory collapse detection

- Comprehensive metrics engine (`MetricEngine` class)
- Circuit breaker implementation with state machine
- Full unit test suite (8+ test cases)
- Production-ready documentation
- Example integration patterns
- MIT License
- DOI registration: 10.5281/zenodo.20214580

### Features

- **Lightweight**: < 3ms latency per step
- **Non-invasive**: Works as sidecar to any agent
- **Numerically stable**: EPS handling, float32 precision
- **Cold-start safe**: Requires window accumulation before metrics
- **Hysteresis**: 3 critical cycles to open, 5 nominal to close
- **Evidence-based**: Tracks progress and resource consumption
- **Configurable**: All thresholds and parameters tunable

### Benchmarks

- 65–77% reduction in looping session duration
- < 4% false positive rate
- 14–16% improvement in synthetic data purity (RLAIF)
- 68–77% token savings on looping workloads

---

## Future Roadmap

### [1.1.0] - Planned

- Rust hotpath implementation (pyo3)
- GPU acceleration for projection matrices
- Extended integration suite (Claude, Gemini, local LLMs)
- Real-time dashboard (Grafana templates)
- Distributed orchestration (multi-agent support)
- ONNX export for edge deployment

### [1.2.0] - Planned

- Adaptive threshold learning (online ECDF calibration)
- Hierarchical monitoring (multi-level agents)
- Temporal pattern analysis (trajectory forensics)
- Streaming mode (reduce memory footprint)

---

## Known Limitations

- Requires embedding access (not suitable for black-box APIs)
- Assumes typical LLM agent behavior patterns
- Thresholds optimized for general workloads (may need tuning for niche domains)

## Support

For issues, feature requests, or contributions, please see [CONTRIBUTING.md](CONTRIBUTING.md).

---

**Version:** 1.0.0  
**Release Date:** May 19, 2026  
**Author:** Andrey A. Artsybashev (Kharkiv, Ukraine)  
**DOI:** 10.5281/zenodo.20214580
