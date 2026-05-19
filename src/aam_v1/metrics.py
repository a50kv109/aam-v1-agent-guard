"""
Metric computation utilities for AAM-V1
"""

import numpy as np
from typing import Tuple, List


class MetricEngine:
    """Compute and track AAM-V1 metrics over time."""
    
    def __init__(self, window_size: int = 8):
        self.window_size = window_size
        self.metrics_history: List[dict] = []
        self.EPS = 1e-9
    
    def compute_participation_ratio(self, embeddings: np.ndarray) -> float:
        """
        Compute Participation Ratio.
        Higher values indicate more dimensions being used.
        
        Args:
            embeddings: (window_size, embedding_dim) array
        
        Returns:
            PR value in [0, 1]
        """
        if embeddings.shape[0] < 2:
            return 0.0
        
        cov = np.cov(embeddings.T)
        eigenvalues = np.abs(np.linalg.eigvalsh(cov))
        eigenvalues = eigenvalues[eigenvalues > self.EPS]
        
        if len(eigenvalues) == 0:
            return 0.0
        
        sum_eig = np.sum(eigenvalues)
        pr = (sum_eig ** 2) / (np.sum(eigenvalues ** 2) + self.EPS)
        
        return float(np.clip(pr, 0.0, 1.0))
    
    def compute_mobility(self, embeddings: np.ndarray) -> float:
        """
        Compute trajectory mobility (displacement between consecutive points).
        
        Args:
            embeddings: (window_size, embedding_dim) array
        
        Returns:
            Mobility value (distance)
        """
        if embeddings.shape[0] < 2:
            return 1.0
        
        centroids = np.mean(embeddings, axis=1)
        if len(centroids) < 2:
            return 1.0
        
        mobility = np.linalg.norm(centroids[-1] - centroids[-2]) + self.EPS
        return float(mobility)
    
    def compute_enr(self, evidence_bytes: int, total_pressure: float) -> float:
        """
        Compute Evidence Novelty Ratio.
        
        Args:
            evidence_bytes: Cumulative new evidence
            total_pressure: Weighted cumulative pressure
        
        Returns:
            ENR in [0, 1]
        """
        enr = evidence_bytes / (total_pressure + self.EPS)
        return float(np.clip(enr, 0.0, 1.0))
    
    def compute_tes(self, tools_history: List[str], recent_window: int = 12) -> float:
        """
        Compute Tool Effectiveness Score (write/read asymmetry).
        
        Args:
            tools_history: Chronological tool invocations
            recent_window: Recent steps to consider
        
        Returns:
            TES in [0, 1]
        """
        if len(tools_history) == 0:
            return 0.0
        
        recent = tools_history[-recent_window:]
        
        write_tools = {
            "file_editor", "code_execution", "bash_write",
            "git_commit", "reasoning_step", "plan", "execute"
        }
        
        write_count = sum(1 for t in recent if t in write_tools)
        tes = write_count / max(len(recent), 1)
        
        return float(np.clip(tes, 0.0, 1.0))
    
    def compute_cei(self, tools_history: List[str], enr: float, 
                   recent_window: int = 12) -> float:
        """
        Compute Context Entropy Index.
        
        Args:
            tools_history: Chronological tool invocations
            enr: Evidence Novelty Ratio
            recent_window: Recent steps to consider
        
        Returns:
            CEI in [0, 1]
        """
        if len(tools_history) == 0:
            return 0.0
        
        recent = tools_history[-recent_window:]
        unique_tools = len(set(recent))
        tool_diversity = unique_tools / max(len(recent), 1)
        
        cei = tool_diversity * (1.0 - enr)
        return float(np.clip(cei, 0.0, 1.0))
    
    def store_metrics(self, metrics: dict) -> None:
        """Store metrics snapshot for analysis."""
        self.metrics_history.append(metrics)
    
    def get_metrics_summary(self) -> dict:
        """Get summary statistics of stored metrics."""
        if not self.metrics_history:
            return {}
        
        keys = self.metrics_history[0].keys()
        summary = {}
        
        for key in keys:
            values = [m[key] for m in self.metrics_history if isinstance(m.get(key), (int, float))]
            if values:
                summary[key] = {
                    "mean": float(np.mean(values)),
                    "std": float(np.std(values)),
                    "min": float(np.min(values)),
                    "max": float(np.max(values))
                }
        
        return summary
