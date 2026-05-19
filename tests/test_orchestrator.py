"""
Unit tests for AgentManagerOrchestrator
"""

import pytest
import numpy as np
from aam_v1.orchestrator import AgentManagerOrchestrator


class TestAgentManagerOrchestrator:
    """Test suite for core orchestrator functionality."""
    
    @pytest.fixture
    def orchestrator(self):
        return AgentManagerOrchestrator(
            window_size=8,
            recovery_budget=3,
            pr_threshold=0.32,
            mobility_threshold=0.09,
            enr_threshold=0.07
        )
    
    def test_initialization(self, orchestrator):
        """Test orchestrator initializes correctly."""
        assert orchestrator.window_size == 8
        assert orchestrator.recovery_budget == 3
        assert orchestrator.critical_streak == 0
        assert len(orchestrator.embedding_window) == 0
    
    def test_cold_start_protection(self, orchestrator):
        """Test that cold start returns COLD_START status."""
        embedding = np.random.randn(512).astype(np.float32)
        
        decision = orchestrator.add_step(
            thought_embedding=embedding,
            tool_name="test_tool",
            new_evidence_tokens=10
        )
        
        assert decision["status"] == "COLD_START"
        assert decision["allow"] is True
    
    def test_accumulation_to_nominal(self, orchestrator):
        """Test transition from cold start to nominal operation."""
        # Fill window
        for i in range(8):
            embedding = np.random.randn(512).astype(np.float32)
            decision = orchestrator.add_step(
                thought_embedding=embedding,
                tool_name="search_tool",
                new_evidence_tokens=50,
                verification_score=0.8
            )
            
            if i < 7:
                assert decision["status"] == "COLD_START"
            else:
                # At window size, should transition to nominal
                assert decision["status"] == "NOMINAL"
                assert "metrics" in decision
    
    def test_metrics_computation(self, orchestrator):
        """Test that metrics are properly computed."""
        # Fill window with diverse embeddings
        for i in range(8):
            embedding = np.random.randn(512).astype(np.float32)
            orchestrator.add_step(
                thought_embedding=embedding,
                tool_name="tool_" + str(i % 3),
                new_evidence_tokens=100,
                verification_score=0.9
            )
        
        # Get metrics
        decision = orchestrator.add_step(
            thought_embedding=np.random.randn(512).astype(np.float32),
            tool_name="test",
            new_evidence_tokens=100
        )
        
        assert "metrics" in decision
        metrics = decision["metrics"]
        assert all(key in metrics for key in ["PR", "Mobility", "ENR", "TES", "CEI"])
        assert all(isinstance(v, float) for v in metrics.values())
    
    def test_hard_interrupt_detection(self, orchestrator):
        """Test detection of rabbit hole (hard interrupt)."""
        # Generate stagnant trajectory (low PR, low mobility)
        base_embedding = np.random.randn(512).astype(np.float32)
        
        for _ in range(10):
            # Keep embeddings nearly identical
            noisy = base_embedding + np.random.randn(512).astype(np.float32) * 0.001
            
            decision = orchestrator.add_step(
                thought_embedding=noisy,
                tool_name="search",
                new_evidence_tokens=1,  # Very low evidence
                verification_score=0.2  # Poor progress
            )
        
        # Should trigger HARD_INTERRUPT
        assert decision["status"] == "HARD_INTERRUPT"
        assert decision["action"] == "ORTHOGONAL_RESET"
    
    def test_recovery_budget_exhaustion(self, orchestrator):
        """Test escalation when recovery budget is exhausted."""
        orchestrator.recovery_budget = 0  # Exhaust budget immediately
        
        # Trigger criticality
        base_embedding = np.random.randn(512).astype(np.float32)
        
        for _ in range(10):
            decision = orchestrator.add_step(
                thought_embedding=base_embedding + np.random.randn(512) * 0.001,
                tool_name="search",
                new_evidence_tokens=1,
                verification_score=0.1
            )
        
        assert decision["status"] == "ESCALATE"
        assert "exhausted" in decision["reason"].lower()
    
    def test_reset_state(self, orchestrator):
        """Test that reset_state clears internal buffers."""
        # Fill state
        for i in range(8):
            orchestrator.add_step(
                thought_embedding=np.random.randn(512),
                tool_name="tool",
                new_evidence_tokens=10
            )
        
        assert len(orchestrator.embedding_window) > 0
        
        # Reset
        orchestrator.reset_state()
        
        assert len(orchestrator.embedding_window) == 0
        assert len(orchestrator.tools_history) == 0
        assert orchestrator.critical_streak == 0
        assert orchestrator.evidence_bytes == 0
    
    def test_get_state(self, orchestrator):
        """Test state getter."""
        state = orchestrator.get_state()
        
        assert "window_size" in state
        assert "critical_streak" in state
        assert "recovery_budget" in state
        assert state["critical_streak"] == 0
        assert state["recovery_budget"] == 3


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_embedding_type_conversion(self):
        """Test that various embedding types are handled."""
        orch = AgentManagerOrchestrator()
        
        # List input
        decision = orch.add_step(
            thought_embedding=[0.1, 0.2, 0.3],
            tool_name="test",
            new_evidence_tokens=10
        )
        assert decision["status"] == "COLD_START"
        
        # Already numpy
        decision = orch.add_step(
            thought_embedding=np.array([0.1, 0.2, 0.3]),
            tool_name="test",
            new_evidence_tokens=10
        )
        assert decision["status"] == "COLD_START"
    
    def test_zero_evidence_handling(self):
        """Test handling of zero new evidence."""
        orch = AgentManagerOrchestrator()
        
        for i in range(8):
            decision = orch.add_step(
                thought_embedding=np.random.randn(512),
                tool_name="read_only",
                new_evidence_tokens=0  # No new evidence
            )
        
        # ENR should be very low
        assert decision["status"] == "NOMINAL"
        assert decision["metrics"]["ENR"] < 0.1
    
    def test_high_verification_score_prevents_interrupt(self):
        """Test that high verification scores prevent interrupts."""
        orch = AgentManagerOrchestrator()
        
        base = np.random.randn(512).astype(np.float32)
        
        for i in range(20):
            decision = orch.add_step(
                thought_embedding=base + np.random.randn(512) * 0.001,
                tool_name="tool",
                new_evidence_tokens=1,
                verification_score=0.95  # Very high score
            )
        
        # Should NOT interrupt despite low metrics
        assert decision["status"] == "NOMINAL"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
