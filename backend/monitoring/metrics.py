"""
KAVAN v6.0 — Metrics Foundation
============================================================
Defines in-memory counters, gauges, and histograms for metrics.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass
class MetricCounter:
    """Simple in-memory counter."""
    name: str
    description: str
    value: int = 0
    labels: Dict[str, str] = field(default_factory=dict)

    def increment(self, amount: int = 1) -> None:
        self.value += amount

    def reset(self) -> None:
        self.value = 0


@dataclass
class MetricGauge:
    """Simple in-memory gauge."""
    name: str
    description: str
    value: float = 0.0

    def set(self, value: float) -> None:
        self.value = value

    def increment(self, amount: float = 1.0) -> None:
        self.value += amount

    def decrement(self, amount: float = 1.0) -> None:
        self.value -= amount


@dataclass
class MetricHistogram:
    """
    Simple in-memory histogram for tracking value distributions (like latencies).
    """
    name: str
    description: str
    buckets: List[float] = field(default_factory=lambda: [5.0, 10.0, 25.0, 50.0, 100.0, 250.0, 500.0, 1000.0, 2500.0, 5000.0])
    sum: float = 0.0
    count: int = 0
    counts: Dict[float, int] = field(default_factory=dict)

    def __post_init__(self):
        self.counts = {bucket: 0 for bucket in self.buckets}
        self.counts[float("inf")] = 0

    def observe(self, value: float) -> None:
        """
        Record a new observation.
        """
        self.sum += value
        self.count += 1
        for bucket in self.buckets:
            if value <= bucket:
                self.counts[bucket] += 1
        self.counts[float("inf")] += 1

    def get_summary(self) -> Dict[str, Any]:
        """
        Returns a dictionary summary.
        """
        return {
            "sum": self.sum,
            "count": self.count,
            "avg": (self.sum / self.count) if self.count > 0 else 0.0,
            "buckets": self.counts,
        }


class MetricsCollector:
    """
    Application-level metrics collector.
    """

    def __init__(self):
        # HTTP Metrics
        self.http_requests_total = MetricCounter(
            name="kavan_http_requests_total",
            description="Total number of HTTP requests",
        )
        self.http_requests_duration = MetricGauge(
            name="kavan_http_request_duration_ms",
            description="Last HTTP request duration in milliseconds",
        )
        self.http_requests_latency = MetricHistogram(
            name="kavan_http_requests_latency_ms",
            description="HTTP requests latency distribution",
        )
        self.http_errors_total = MetricCounter(
            name="kavan_http_errors_total",
            description="Total number of HTTP errors",
        )

        # Database Metrics
        self.db_queries_total = MetricCounter(
            name="kavan_db_queries_total",
            description="Total number of database queries",
        )
        self.db_query_duration = MetricGauge(
            name="kavan_db_query_duration_ms",
            description="Last database query duration in milliseconds",
        )
        self.db_queries_latency = MetricHistogram(
            name="kavan_db_queries_latency_ms",
            description="Database queries latency distribution",
        )

        # Cache Metrics
        self.cache_hits_total = MetricCounter(
            name="kavan_cache_hits_total",
            description="Total number of cache hits",
        )
        self.cache_misses_total = MetricCounter(
            name="kavan_cache_misses_total",
            description="Total number of cache misses",
        )

        # Celery Metrics
        self.celery_tasks_total = MetricCounter(
            name="kavan_celery_tasks_total",
            description="Total number of Celery tasks",
        )
        self.celery_tasks_latency = MetricHistogram(
            name="kavan_celery_tasks_latency_ms",
            description="Celery tasks execution latency distribution",
        )

    def get_summary(self) -> dict:
        """Return a summary of all collected metrics."""
        return {
            "http": {
                "requests_total": self.http_requests_total.value,
                "errors_total": self.http_errors_total.value,
                "last_duration_ms": self.http_requests_duration.value,
                "latency_distribution": self.http_requests_latency.get_summary(),
            },
            "database": {
                "queries_total": self.db_queries_total.value,
                "last_query_duration_ms": self.db_query_duration.value,
                "latency_distribution": self.db_queries_latency.get_summary(),
            },
            "cache": {
                "hits_total": self.cache_hits_total.value,
                "misses_total": self.cache_misses_total.value,
                "hit_rate": (
                    self.cache_hits_total.value
                    / max(self.cache_hits_total.value + self.cache_misses_total.value, 1)
                    * 100
                ),
            },
            "celery": {
                "tasks_total": self.celery_tasks_total.value,
                "latency_distribution": self.celery_tasks_latency.get_summary(),
            },
        }


# Singleton metrics collector instance
metrics = MetricsCollector()
