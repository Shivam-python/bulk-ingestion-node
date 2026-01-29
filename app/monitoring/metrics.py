from prometheus_client import Counter, Histogram, Gauge

# Total HTTP requests
REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)

# Request processing time
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Request latency",
    ["endpoint"],
)

# Active background jobs
ACTIVE_BATCH_JOBS = Gauge(
    "active_batch_jobs",
    "Number of currently running batch jobs",
)

# Total hospitals processed
HOSPITALS_PROCESSED = Counter(
    "hospitals_processed_total",
    "Total hospitals processed",
    ["status"],  # success / failed
)
