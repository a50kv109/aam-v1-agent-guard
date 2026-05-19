# Contributing to AAM-V1

Thank you for your interest in contributing! This document provides guidelines and instructions.

## Code of Conduct

Be respectful, inclusive, and professional. We're all here to make LLM agents more reliable.

## Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/aam-v1-agent-guard.git
cd aam-v1-agent-guard
git remote add upstream https://github.com/a50kv109/aam-v1-agent-guard.git
```

### 2. Set Up Development Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -e ".[dev,all]"
```

### 3. Run Tests

```bash
pytest tests/ -v --cov=src/aam_v1
```

## Development Workflow

### Creating a Feature Branch

```bash
git checkout -b feature/my-feature
```

### Code Style

We follow PEP 8 with Black formatting (100 char line length):

```bash
black src/ tests/
isort src/ tests/
flake8 src/ tests/
```

### Type Hints

Use type hints for all public functions:

```python
def add_step(self,
             thought_embedding: np.ndarray,
             tool_name: str,
             new_evidence_tokens: int) -> Dict[str, Any]:
    """..."""
```

### Documentation

- Docstrings in Google style
- Update README.md if adding user-facing features
- Add examples in `examples/` directory

### Testing

Write tests for new features:

```python
def test_my_feature():
    """Test description."""
    orch = AgentManagerOrchestrator()
    # ... test code
    assert result == expected
```

Min coverage target: **85%**

## Commit Guidelines

```
[FEATURE/FIX/DOCS] Brief description

- Detailed explanation
- Additional context if needed
```

Examples:
- `[FEATURE] Add adaptive threshold learning`
- `[FIX] Handle zero-dimension embeddings`
- `[DOCS] Update calibration guide`

## Pull Request Process

1. **Create PR** with clear title and description
2. **Link related issues** using `Closes #123`
3. **Ensure tests pass**: GitHub Actions will run automatically
4. **Address review comments** professionally
5. **Keep commits clean** (squash if needed)

### PR Template

```markdown
## Description
Brief summary of changes.

## Related Issues
Closes #123

## Changes
- Change 1
- Change 2

## Testing
How was this tested?

## Checklist
- [ ] Tests pass locally
- [ ] Code style passes (black, isort)
- [ ] Type hints added
- [ ] Docstrings updated
- [ ] No breaking changes
```

## Reporting Issues

### Bug Report Template

```markdown
## Description
Clear description of the bug.

## Reproduction
Steps to reproduce:
1. ...
2. ...

## Expected Behavior
What should happen?

## Actual Behavior
What actually happens?

## Environment
- Python version: 3.11
- AAM-V1 version: 1.0.0
- OS: Ubuntu 22.04
```

### Feature Request Template

```markdown
## Description
What feature would you like?

## Motivation
Why is this needed?

## Proposed Solution
How should it work?

## Examples
Usage examples if applicable.
```

## Areas for Contribution

### High Priority

- [ ] Rust hotpath implementation (pyo3)
- [ ] GPU acceleration for projections
- [ ] Adaptive threshold learning
- [ ] Multi-agent orchestration

### Medium Priority

- [ ] Extended integrations (Claude, Gemini)
- [ ] Real-time dashboard
- [ ] Performance benchmarks
- [ ] Documentation improvements

### Low Priority

- [ ] Example scripts
- [ ] Type hint improvements
- [ ] Code cleanup

## Project Structure

```
src/aam_v1/
├── orchestrator.py      # Main class
├── metrics.py           # Metric computations
├── circuit_breaker.py   # Control logic
└── integrations/        # Third-party integrations

tests/
├── test_orchestrator.py
├── test_metrics.py
└── test_simulations.py

examples/
└── *.py                 # Usage examples
```

## Performance Considerations

- Target: < 3ms latency per `add_step()` call
- Memory: O(window_size * embedding_dim) + O(1) other state
- Avoid blocking operations in main loop
- Prefer numpy vectorization over Python loops

## Documentation Standards

- Code examples should be runnable
- Document edge cases
- Explain the "why" not just the "how"
- Keep README.md updated

## Licensing

By contributing, you agree that your contributions are licensed under the MIT License.

## Questions?

Open a discussion or issue on GitHub. We're here to help!

---

**Happy contributing!**  
**Authors:** Andrey A. Artsybashev & Community
