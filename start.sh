#!/bin/bash
set -e
echo "Starting Decentralized Finance Dashboard with Smart Contract Analytics..."
uvicorn app:app --host 0.0.0.0 --port 9056 --workers 1
