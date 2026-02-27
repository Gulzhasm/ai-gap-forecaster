import sys
import traceback

try:
    from app import create_app
    app = create_app('production')
    print("App created successfully", file=sys.stderr, flush=True)
except Exception as e:
    print(f"STARTUP ERROR: {e}", file=sys.stderr, flush=True)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
