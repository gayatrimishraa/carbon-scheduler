import json
import time
import hashlib
import os

# This flag is True only on a cold start (first invocation after Lambda container starts)
_cold_start = True

def lambda_handler(event, context):
    global _cold_start

    was_cold = _cold_start
    _cold_start = False  # all future invocations in this container are warm

    # Simulate ~100ms of real work: hash a string 50,000 times
    start = time.time()
    data = "carbon-aware-scheduler"
    for _ in range(50000):
        data = hashlib.sha256(data.encode()).hexdigest()
    duration_ms = round((time.time() - start) * 1000, 2)

    response = {
        "region": os.environ.get("AWS_REGION", "unknown"),
        "cold_start": was_cold,
        "duration_ms": duration_ms,
        "memory_mb": int(context.memory_limit_in_mb),
        "request_id": context.aws_request_id
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }