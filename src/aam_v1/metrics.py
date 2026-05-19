"""Metric computation utilities for AAM-V1.

Author: Andrey A. Artsybashev
Version: 1.0
"""

import numpy as np
from typing import Tuple, Optional


class MetricEngine:
    """Compute and cache topological metrics."""
    
    EPS = 1e-9
    
    @staticmethod
    def participation_ratio(embeddings: np.ndarray) -> float:
        """Participation Ratio via spectral analysis.
        
        Args:
            embeddings: Array of shape (n_samples, embedding_dim)
            
        Returns:
            PR score (0 to 1)
        """
        if len(embeddings) < 2:
            return 1.0
        
        cov = np.cov(embeddings.T)
        
        if cov.ndim == 0:
            return 1.0
        
        eigenvalues = np.abs(np.linalg.eigvalsh(cov))
        eigenvalues = eigenvalues[eigenvalues > MetricEngine.EPS]
        
        if len(eigenvalues) == 0:
            return 0.0
        
        sum_eig = np.sum(eigenvalues)
        return float((sum_eig ** 2) / (np.sum(eigenvalues ** 2) + MetricEngine.EPS))
    
    @staticmethod
    def mobility(embeddings: np.ndarray, split_ratio: float = 0.5) -> float:
        """Centroid mobility between temporal halves.
        
        Args:
            embeddings: Array of shape (n_samples, embedding_dim)
            split_ratio: Where to split for comparison
            
        Returns:
            Mobility score (Euclidean distance)
        """
        if len(embeddings) < 2:
            return 1.0
        
        split_idx = int(len(embeddings) * split_ratio)
        
        c_prev = np.mean(embeddings[:split_idx], axis=0)
        c_curr = np.mean(embeddings[split_idx:], axis=0)
        
        return float(np.linalg.norm(c_curr - c_prev) + MetricEngine.EPS)
    
    @staticmethod
    def evidence_novelty_ratio(evidence_bytes: int, total_pressure: float) -> float:
        """Compute evidence novelty ratio.
        
        Args:
            evidence_bytes: Amount of new evidence
            total_pressure: Total weighted context
            
        Returns:
            ENR score
        """
        return float(evidence_bytes / (total_pressure + MetricEngine.EPS))
    
    @staticmethod
    def tool_effectiveness_score(tools_history: list, write_tools: Optional[set] = None) -> float:
        """Compute tool effectiveness score.
        
        Args:
            tools_history: List of tool names
            write_tools: Set of write tool names
            
        Returns:
            TES score (0 to 1)
        """
        if write_tools is None:
            write_tools = {
                "file_editor", "code_execution", "bash_write", 
                "git_commit", "reasoning_step"
            }
        
        if len(tools_history) == 0:
            return 0.0
        
        write_count = sum(1 for t in tools_history if t in write_tools)
        return float(write_count / len(tools_history))
