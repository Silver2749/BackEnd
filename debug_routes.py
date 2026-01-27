from app import create_app

app = create_app()

print("Routes registered:")
for route in app.routes:
    print(f"  {route.path} - {getattr(route, 'methods', 'static')}")

print("\nMounts:")
for route in app.routes:
    if hasattr(route, 'path') and route.path == '/static':
        print(f"  Static mount at: {route.path}")
