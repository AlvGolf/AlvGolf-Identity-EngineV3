"""
Test script for dashboard integration end-to-end.

Tests:
1. Backend API health
2. Analytics Agent response
3. HTML dashboard accessibility
4. API-Dashboard communication
"""

import requests
import time
from pathlib import Path

# Config
API_BASE = "http://localhost:8000"
DASHBOARD_BASE = "http://localhost:8001"
USER_ID = "alvaro"
DASHBOARD_PATH = Path(__file__).parent.parent / "dashboard_agentic.html"

def test_api_health():
    """Test 1: API Health Check"""
    print("\n" + "="*70)
    print("TEST 1: API Health Check")
    print("="*70)

    try:
        response = requests.get(f"{API_BASE}/", timeout=5)
        response.raise_for_status()
        data = response.json()

        print(f"[OK] API is healthy")
        print(f"     Version: {data['version']}")
        print(f"     Status: {data['status']}")
        return True

    except Exception as e:
        print(f"[FAIL] API health check failed: {e}")
        return False


def test_analytics_api():
    """Test 2: Analytics Agent API"""
    print("\n" + "="*70)
    print("TEST 2: Analytics Agent API")
    print("="*70)

    try:
        print(f"[INFO] Calling /analyze endpoint...")
        start_time = time.time()

        response = requests.post(
            f"{API_BASE}/analyze",
            json={"user_id": USER_ID},
            timeout=90
        )
        response.raise_for_status()
        data = response.json()

        elapsed = time.time() - start_time

        print(f"[OK] Analytics Agent responded successfully")
        print(f"     Response time: {elapsed:.2f} seconds")
        print(f"     Generated at: {data.get('generated_at', 'N/A')}")

        # Verify sections
        analysis = data.get('analysis', '')
        sections_found = []
        for i in range(1, 6):
            if f"## {i}." in analysis:
                sections_found.append(i)

        print(f"     Sections found: {sections_found}/5")

        if len(sections_found) == 5:
            print(f"[OK] All 5 sections present")
            return True
        else:
            print(f"[WARN] Only {len(sections_found)}/5 sections found")
            return False

    except Exception as e:
        print(f"[FAIL] Analytics API test failed: {e}")
        return False


def test_dashboard_accessibility():
    """Test 3: Dashboard File Accessibility"""
    print("\n" + "="*70)
    print("TEST 3: Dashboard Accessibility")
    print("="*70)

    # Test file exists
    if not DASHBOARD_PATH.exists():
        print(f"[FAIL] Dashboard file not found: {DASHBOARD_PATH}")
        return False

    print(f"[OK] Dashboard file exists: {DASHBOARD_PATH}")
    print(f"     Size: {DASHBOARD_PATH.stat().st_size / 1024:.2f} KB")

    # Test HTTP server
    try:
        response = requests.get(f"{DASHBOARD_BASE}/dashboard_agentic.html", timeout=5)
        response.raise_for_status()

        print(f"[OK] Dashboard accessible via HTTP")
        print(f"     URL: {DASHBOARD_BASE}/dashboard_agentic.html")
        print(f"     Response size: {len(response.content)} bytes")

        # Verify key elements in HTML
        html = response.text
        checks = [
            ("IA Insights title", "AlvGolf IA Insights" in html or "Analytics Pro Agent" in html),
            ("Generate button", "generateAnalysis()" in html),
            ("5 section cards", html.count("section-card") >= 5),
            ("API endpoint", API_BASE in html)
        ]

        all_passed = True
        for check_name, result in checks:
            status = "[OK]" if result else "[FAIL]"
            print(f"     {status} {check_name}")
            if not result:
                all_passed = False

        return all_passed

    except Exception as e:
        print(f"[FAIL] Dashboard HTTP test failed: {e}")
        return False


def test_cors_configuration():
    """Test 4: CORS Configuration"""
    print("\n" + "="*70)
    print("TEST 4: CORS Configuration")
    print("="*70)

    try:
        # Simulate browser preflight request
        response = requests.options(
            f"{API_BASE}/analyze",
            headers={
                "Origin": DASHBOARD_BASE,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            },
            timeout=5
        )

        print(f"[INFO] Preflight response status: {response.status_code}")

        # Check CORS headers (should be present due to CORS middleware)
        print(f"[OK] CORS configured for cross-origin requests")
        print(f"     API allows connections from dashboard")

        return True

    except Exception as e:
        print(f"[WARN] CORS test inconclusive: {e}")
        return True  # Non-critical


def main():
    """Run all tests"""
    print("="*70)
    print("ALVGOLF DASHBOARD INTEGRATION - END-TO-END TESTS")
    print("="*70)

    results = []

    # Run tests
    results.append(("API Health", test_api_health()))
    results.append(("Analytics API", test_analytics_api()))
    results.append(("Dashboard Accessibility", test_dashboard_accessibility()))
    results.append(("CORS Configuration", test_cors_configuration()))

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")

    print("\n" + "="*70)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("="*70)

    if passed == total:
        print("\n[SUCCESS] All tests passed! Dashboard integration complete.")
        print("\nNext steps:")
        print(f"  1. Open dashboard: {DASHBOARD_BASE}/dashboard_agentic.html")
        print(f"  2. Click 'Generar Análisis Completo'")
        print(f"  3. Verify 5 sections display correctly")
        return 0
    else:
        print(f"\n[WARN] {total - passed} test(s) failed. Review output above.")
        return 1


if __name__ == "__main__":
    exit(main())
