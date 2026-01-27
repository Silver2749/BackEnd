#!/usr/bin/env python3
import sys
from app import create_app

app = create_app()
print("SUCCESS: App created")
print("Routes:")
for route in app.routes:
    path = getattr(route, 'path', 'N/A')
    methods = getattr(route, 'methods', set())
    print(f"  {path} - {methods}")
