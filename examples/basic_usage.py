"""
Basic usage example of AAM-V1 orchestrator
"""

import numpy as np
from aam_v1.orchestrator import AgentManagerOrchestrator


def simulate_healthy_agent():
    """Simulate a healthy agent with good progress."""
    print("\n=== Simulating Healthy Agent ===\n")
    
    orch = AgentManagerOrchestrator()
    
    for step in range(20):
        # Healthy embedding: diverse, moving forward
        embedding = np.random.randn(512).astype(np.float32) + (step * 0.1)
        
        decision = orch.add_step(
            thought_embedding=embedding,
            tool_name=["search", "read", "analyze", "write"][step % 4],
            new_evidence_tokens=50 + step * 5,  # Increasing evidence
            verification_score=0.7 + (step * 0.01)  # Improving
        )
        
        if decision["status"] != "COLD_START":
            print(f"Step {step:2d}: {decision['status']:10s} | "
                  f"PR={decision['metrics']['PR']:.3f} | "
                  f"ENR={decision['metrics']['ENR']:.3f} | "
                  f"TES={decision['metrics']['TES']:.3f}")


def simulate_rabbit_hole():
    """Simulate agent stuck in rabbit hole."""
    print("\n=== Simulating Rabbit Hole ===\n")
    
    orch = AgentManagerOrchestrator()
    
    # Create a "stuck" embedding
    base_embedding = np.random.randn(512).astype(np.float32)
    
    for step in range(25):
        # Nearly identical embeddings (stagnation)
        noise = np.random.randn(512).astype(np.float32) * 0.0001
        embedding = base_embedding + noise
        
        decision = orch.add_step(
            thought_embedding=embedding,
            tool_name="search",  # Only searching
            new_evidence_tokens=1 if step > 5 else 20,  # Drying up
            verification_score=0.3  # Poor progress
        )
        
        print(f"Step {step:2d}: {decision['status']:15s} | "
              f"PR={decision['metrics'].get('PR', 0):.3f} | "
              f"ENR={decision['metrics'].get('ENR', 0):.3f}")
        
        if decision["status"] == "HARD_INTERRUPT":
            print(f"\n⚠️  HARD INTERRUPT TRIGGERED at step {step}")
            print(f"   Reason: {decision['message']}")
            print(f"   Recovery budget remaining: {decision['recovery_budget_remaining']}")
            break


def simulate_with_recovery():
    """Simulate recovery from rabbit hole."""
    print("\n=== Simulating Recovery from Rabbit Hole ===\n")
    
    orch = AgentManagerOrchestrator(recovery_budget=3)
    
    phase = "healthy"
    base_embedding = np.random.randn(512).astype(np.float32)
    
    for step in range(40):
        # Phase 1: healthy
        if step < 10:
            phase = "healthy"
            embedding = np.random.randn(512).astype(np.float32) + (step * 0.15)
            tool = ["search", "analyze", "write"][step % 3]
            evidence = 100
            score = 0.8
        
        # Phase 2: stuck
        elif step < 25:
            phase = "stuck"
            embedding = base_embedding + np.random.randn(512) * 0.0001
            tool = "search"
            evidence = 1
            score = 0.2
        
        # Phase 3: reset (after interrupt)
        else:
            phase = "recovery"
            embedding = np.random.randn(512).astype(np.float32) + (step * 0.1)
            tool = ["analyze", "write", "execute"][step % 3]
            evidence = 150
            score = 0.7
        
        decision = orch.add_step(
            thought_embedding=embedding,
            tool_name=tool,
            new_evidence_tokens=evidence,
            verification_score=score
        )
        
        if decision["status"] != "COLD_START":
            print(f"Step {step:2d} [{phase:8s}]: {decision['status']:15s} | "
                  f"EN={orch.evidence_bytes:6d}")
        
        # Simulate reset after interrupt
        if decision["status"] == "HARD_INTERRUPT":
            print(f"\n  → Resetting agent...\n")
            orch.reset_state()


if __name__ == "__main__":
    print("=" * 60)
    print("AAM-V1 Basic Usage Examples")
    print("=" * 60)
    
    simulate_healthy_agent()
    simulate_rabbit_hole()
    simulate_with_recovery()
    
    print("\n" + "=" * 60)
    print("Examples completed successfully!")
    print("=" * 60)
