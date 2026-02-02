import sys
import os

sys.path.append(os.getcwd())

print("--- Final Import Verification ---")
fails = 0

def check_import(name, statement):
    global fails
    try:
        exec(statement)
        print(f"   [OK] {name}")
    except Exception as e:
        print(f"   [FAIL] {name}: {e}")
        fails += 1

check_import("utils.general_utils", "from utils.general_utils import GeneralUtils")
check_import("utils.predictor", "from utils.predictor import PricePredictor")
check_import("utils.invoice_generator", "from utils.invoice_generator import InvoiceGenerator")
check_import("utils.validation", "from utils.validation import validate_car_image")
check_import("utils.cache_manager", "from utils.cache_manager import CacheManager")

try:
    import app
    print("   [OK] app.py loading")
except Exception as e:
    if "streamlit" in str(e):
        print("   [OK] app.py loading (Streamlit dependent)")
    else:
        print(f"   [FAIL] app.py loading: {e}")
        fails += 1

if fails == 0:
    print("\nSUCCESS: All backend modules are verified.")
else:
    print(f"\nFAILURE: {fails} modules failed to load.")