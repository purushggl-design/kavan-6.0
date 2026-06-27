"""
KAVAN v6.0 — System Metrics Collectors
============================================================
Collects host system usage (CPU, memory, disk) and process stats.
"""

import os
import psutil
from typing import Dict, Any

class SystemMetricsCollector:
    """
    Gathers metrics from the operating system and Django process.
    """

    def collect(self) -> Dict[str, Any]:
        """
        Gathers system resource usage.
        """
        try:
            # CPU utilization (non-blocking)
            cpu_percent = psutil.cpu_percent(interval=None)
            cpu_count = psutil.cpu_count()

            # Virtual memory details
            virtual_mem = psutil.virtual_memory()
            memory_percent = virtual_mem.percent

            # Disk usage for project root
            disk_usage = psutil.disk_usage("/")
            disk_percent = disk_usage.percent

            # Django process details
            process = psutil.Process(os.getpid())
            process_memory = process.memory_info().rss
            process_threads = process.num_threads()
            process_cpu = process.cpu_percent(interval=None)
            
            return {
                "system": {
                    "cpu_percent": cpu_percent,
                    "cpu_count": cpu_count,
                    "memory_percent": memory_percent,
                    "memory_used_bytes": virtual_mem.used,
                    "memory_total_bytes": virtual_mem.total,
                    "disk_percent": disk_percent,
                    "disk_used_bytes": disk_usage.used,
                    "disk_total_bytes": disk_usage.total,
                },
                "process": {
                    "memory_rss_bytes": process_memory,
                    "thread_count": process_threads,
                    "cpu_percent": process_cpu,
                }
            }
        except Exception as e:
            return {
                "error": str(e),
                "system": {
                    "cpu_percent": 0.0,
                    "cpu_count": 1,
                    "memory_percent": 0.0,
                    "memory_used_bytes": 0,
                    "memory_total_bytes": 0,
                    "disk_percent": 0.0,
                    "disk_used_bytes": 0,
                    "disk_total_bytes": 0,
                },
                "process": {
                    "memory_rss_bytes": 0,
                    "thread_count": 1,
                    "cpu_percent": 0.0,
                }
            }
