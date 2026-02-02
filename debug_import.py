import sys
import traceback

try:
    import app
    print("Import successful")
except Exception:
    traceback.print_exc()
