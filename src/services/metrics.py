from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

inference_latency = Histogram("fr_inference_seconds", "Embedding inference latency")
requests_total = Counter("fr_requests_total", "Total API requests", ["route", "method", "status"])


def metrics_endpoint():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
