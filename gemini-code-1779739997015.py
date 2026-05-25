import numpy as np
from typing import Dict, Any
from sklearn.linear_model import LinearRegression

class KernelAudit:
    """
    Core Resilience Kernel: вычисление индексов стабильности и целостности.
    Обеспечивает L1-уровень (Telemetry/Observability).
    """
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.adaptive_margins = []
        self.drift_velocities = []

    def compute_stability_index(self, margin_history: List[float], drift_history: List[float]) -> float:
        """
        S_i = Integral(Adaptive_Margin) / Integral(Drift_Velocity)
        Используем простую аппроксимацию интеграла через среднее значение окна.
        """
        if len(margin_history) < self.window_size:
            return 1.0
        
        # Вычисляем тренды через линейную регрессию для фильтрации шума
        x = np.arange(self.window_size).reshape(-1, 1)
        
        m_reg = LinearRegression().fit(x, margin_history[-self.window_size:])
        d_reg = LinearRegression().fit(x, drift_history[-self.window_size:])
        
        integral_margin = max(m_reg.predict(x).sum(), 1e-9)
        integral_drift = max(d_reg.predict(x).sum(), 1e-9)
        
        return float(integral_margin / integral_drift)

    def compute_semantic_integrity(self, observed: Dict[str, Any], inferred: Dict[str, Any]) -> float:
        """
        Omega = Observed_Telemetry / Inferred_Model_State
        Определяет риск галлюцинации.
        """
        # Сравнение фактов из логов инструментов (Observed) с "уверенностью" модели (Inferred)
        obs_val = observed.get("success_rate", 0.0)
        inf_val = inferred.get("confidence_score", 1.0)
        
        # Если модель уверена (inf=1), а факты говорят об ошибках (obs=0) -> Omega стремится к 0
        return float(obs_val / max(inf_val, 1e-9))

    def audit_step(self, metrics: Dict[str, Any]) -> Dict[str, float]:
        """
        Выполнение полного аудита текущего шага.
        """
        si = self.compute_stability_index(metrics['margins'], metrics['drifts'])
        omega = self.compute_semantic_integrity(metrics['obs'], metrics['inf'])
        
        return {
            "stability_index": si,
            "semantic_integrity": omega,
            "audit_status": "CRITICAL" if (si < 0.5 or omega < 0.7) else "NOMINAL"
        }