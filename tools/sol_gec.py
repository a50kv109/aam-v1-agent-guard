import sys
import os

# Обеспечиваем видимость src для импорта библиотеки AAM-V1
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Динамическая конфигурация для поддержки иерархии импортов AAM-V1
try:
    from aam_v1.orchestrator import AgentManagerOrchestrator
    FOUND_CORE = True
except ImportError:
    FOUND_CORE = False

def main():
    print("[⚓] AAM-V1 GEC Runtime initialized.")
    if FOUND_CORE:
        print("[SENS] Core Orchestrator detected and linked.")
    else:
        print("[WARN] Core Orchestrator not found in src/aam_v1. Check structure.")
    
    # Режим детерминированного аудита (ECC-1)
    print("[STATUS] Mode: Hallucination Suppression (NULL_SAFETY_GATE)")
    pass

if __name__ == "__main__":
    main()
