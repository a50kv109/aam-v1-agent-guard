import os
import psutil # Требуется добавить в requirements.txt
from typing import Dict, List

class KernelAudit:
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.process = psutil.Process(os.getpid())

    def get_resource_metrics(self) -> Dict[str, float]:
        """
        L1: Сбор данных о физическом здоровье (RSS, CPU Stall).
        """
        mem_info = self.process.memory_info()
        # RSS - Resident Set Size (реальная память в RAM)
        rss_mb = mem_info.rss / (1024 * 1024)
        
        # PSI (Pressure Stall Information) - имитация считывания из /proc/pressure/
        # Если Linux, можно читать /proc/pressure/memory
        psi_avg10 = 0.0
        try:
            with open('/proc/pressure/memory', 'r') as f:
                line = f.readline()
                psi_avg10 = float(line.split('avg10=')[1].split(' ')[0])
        except:
            psi_avg10 = 0.0 # Fallback для других ОС
            
        return {"rss_mb": rss_mb, "memory_psi": psi_avg10}

    def audit_step(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        phys = self.get_resource_metrics()
        logic_audit = super().audit_step(metrics) # Вызов логического аудита
        
        # Добавляем жесткий порог безопасности по физике (L0)
        physical_status = "CRITICAL" if phys['rss_mb'] > 2048 or phys['memory_psi'] > 20.0 else "NOMINAL"
        
        logic_audit.update({
            "physical_status": physical_status,
            "resources": phys,
            "audit_status": "CRITICAL" if (logic_audit["audit_status"] == "CRITICAL" or physical_status == "CRITICAL") else "NOMINAL"
        })
        return logic_audit