#!/usr/bin/env python3
import os
import sys

port = os.getenv('PORT', 'NOT SET')
print(f"PORT environment variable: {port}", file=sys.stderr)

if port != 'NOT SET':
    print(f"Railway expects the app to listen on port {port}", file=sys.stderr)
else:
    print("PORT not set - using default 8000", file=sys.stderr)