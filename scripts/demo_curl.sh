#!/usr/bin/env bash
set -euo pipefail

# Enroll example:
# curl -X POST "http://localhost:8000/enroll" \
#   -F "file=@/path/to/face.jpg" \
#   -F "name=Alice" \
#   -F "email=alice@example.com"

# Verify example:
# curl -X POST "http://localhost:8000/verify/<person_id>" \
#   -F "file=@/path/to/face.jpg"

# Search example:
# curl -X POST "http://localhost:8000/search?k=3" \
#   -F "file=@/path/to/unknown.jpg"
