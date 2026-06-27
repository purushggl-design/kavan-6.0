"""
KAVAN v6.0 — Metrics Registry
============================================================
Singleton registry class aggregating all application and system collectors.
"""

from typing import Dict, Any
from monitoring.collectors import SystemMetricsCollector
from monitoring.metrics import metrics as app_metrics

class MetricsRegistry:
    """
    Unified manager for accessing all metrics across the system.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MetricsRegistry, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.system_collector = SystemMetricsCollector()
        self.app_metrics = app_metrics

    def collect_all(self) -> Dict[str, Any]:
        """
        Gathers a snapshot of all system resources and custom application metrics.
        """
        return {
            "app_metrics": self.app_metrics.get_summary(),
            "system_metrics": self.system_collector.collect(),
        }

# Global registry instance
metrics_registry = MetricsRegistry()
