#!/usr/bin/env python3
"""Test script to verify environment variables are being read"""

import os
import sys

print("=== Environment Variable Test ===", file=sys.stderr)
print(f"DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT SET')}", file=sys.stderr)
print(f"ENVIRONMENT: {os.getenv('ENVIRONMENT', 'NOT SET')}", file=sys.stderr)
print(f"SECRET_KEY: {os.getenv('SECRET_KEY', 'NOT SET')}", file=sys.stderr)
print(f"GOOGLE_CLIENT_ID: {os.getenv('GOOGLE_CLIENT_ID', 'NOT SET')}", file=sys.stderr)
print(f"PORT: {os.getenv('PORT', 'NOT SET')}", file=sys.stderr)
print("=================================", file=sys.stderr)