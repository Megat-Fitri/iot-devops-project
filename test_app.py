import requests
import sys

# Set to 5001 to match the Jenkins test container port
BASE_URL = "http://localhost:5001"
failed = 0

def test(name, url, expected_status=200, check_body=None):
    global failed
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != expected_status:
            print(f"❌ {name}: Expected status {expected_status}, got {r.status_code}")
            failed += 1
            return
        if check_body:
            result = check_body(r)
            if not result:
                print(f"❌ {name}: Body check failed")
                failed += 1
                return
        print(f"✅ {name}: PASSED")
    except Exception as e:
        print(f"❌ {name}: Exception - {e}")
        failed += 1

# Test 1: Temperature endpoint
def check_temperature(r):
    try:
        data = r.json()
        temp = float(data.get("value", data)) if isinstance(data, dict) else float(r.text)
        return 20.0 <= temp <= 30.0
    except:
        return False

test("Temperature Endpoint", f"{BASE_URL}/temperature", check_body=check_temperature)

# Test 2: Status endpoint
def check_status(r):
    return r.text.strip() == "OK"

test("Status Endpoint", f"{BASE_URL}/status", check_body=check_status)

# Test 3: Health endpoint
def check_health(r):
    return r.text.strip() == "healthy"

test("Health Endpoint", f"{BASE_URL}/health", check_body=check_health)

# Exit with failure if any test failed
if failed > 0:
    print(f"\n❌ {failed} test(s) FAILED!")
    sys.exit(1)
else:
    print("\n✅ All tests PASSED!")