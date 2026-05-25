from aam_v1.kernel_audit import KernelAudit

class AgentManagerOrchestrator:
    def __init__(self):
        self.audit = KernelAudit()
        
    def add_step(self, ...):
        # 1. Отработка AAM-V1 (детектор)
        decision = self._check_telemetry(...)
        
        # 2. Аудит ядра (L1 - Observability)
        audit_report = self.audit.audit_step(self.get_metrics())
        
        if audit_report["audit_status"] == "CRITICAL":
            return {"action": "TRIGGER_CLCC_RECOVERY", "reason": audit_report}
            
        return decision