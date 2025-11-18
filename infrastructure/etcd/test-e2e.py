#!/usr/bin/env python3
"""
End-to-End Integration Test: etcd Registry + GitOps Sync + Heartbeat

Tests the complete v5.2.0 productization stack:
- etcd 3-node cluster health
- GitOps sync populating capability metadata
- Heartbeat service writing health status
- Data persistence and updates

Exit codes:
  0 - All tests passed
  1 - One or more tests failed
  2 - Setup error (dependencies missing, can't connect, etc.)
"""

import json
import sys
import time
from datetime import datetime

try:
    import etcd3
except ImportError:
    print("ERROR: etcd3 not installed. Run: pip install etcd3")
    sys.exit(2)

# Test configuration
ETCD_HOST = 'localhost'
ETCD_PORT = 2379
TEST_NAMESPACE = 'chora.awareness.sap_self_evaluation'  # Known Service-type capability


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_header(text):
    """Print a section header"""
    print(f"\n{Colors.BLUE}{'=' * 80}{Colors.END}")
    print(f"{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BLUE}{'=' * 80}{Colors.END}")


def print_test(name):
    """Print test name"""
    print(f"\n{Colors.YELLOW}► {name}{Colors.END}")


def print_pass(message):
    """Print success message"""
    print(f"  {Colors.GREEN}[PASS] {message}{Colors.END}")


def print_fail(message):
    """Print failure message"""
    print(f"  {Colors.RED}[FAIL] {message}{Colors.END}")


def print_info(message):
    """Print info message"""
    print(f"    {message}")


class E2ETest:
    """End-to-end integration test for etcd registry infrastructure"""

    def __init__(self):
        self.etcd = None
        self.passed = 0
        self.failed = 0

    def connect(self):
        """Connect to etcd cluster"""
        print_header("Setup: Connecting to etcd")
        try:
            self.etcd = etcd3.client(host=ETCD_HOST, port=ETCD_PORT)
            self.etcd.status()
            print_pass(f"Connected to etcd at {ETCD_HOST}:{ETCD_PORT}")
            return True
        except Exception as e:
            print_fail(f"Failed to connect to etcd: {e}")
            return False

    def test_etcd_cluster_health(self):
        """Test 1: Verify etcd cluster is healthy"""
        print_header("Test 1: etcd Cluster Health")

        try:
            # Get cluster status
            status = self.etcd.status()
            print_pass(f"etcd cluster responding")
            print_info(f"Version: {status.version}")
            # db_size attribute name varies by etcd3 version
            db_size = getattr(status, 'db_size_in_use', getattr(status, 'db_size', 0))
            if db_size > 0:
                print_info(f"DB size: {db_size:,} bytes")
            self.passed += 1
            return True
        except Exception as e:
            print_fail(f"Cluster health check failed: {e}")
            self.failed += 1
            return False

    def test_gitops_sync_data(self):
        """Test 2: Verify GitOps sync has populated capability data"""
        print_header("Test 2: GitOps Sync - Capability Metadata")

        try:
            # Check for capability metadata
            metadata_key = f"/chora/capabilities/{TEST_NAMESPACE}/metadata"
            value, meta = self.etcd.get(metadata_key)

            if not value:
                print_fail(f"No metadata found at {metadata_key}")
                print_info("GitOps sync may not have run yet")
                self.failed += 1
                return False

            metadata = json.loads(value.decode('utf-8'))
            print_pass(f"Capability metadata found: {metadata_key}")
            print_info(f"Namespace: {metadata.get('dc_identifier')}")
            print_info(f"Title: {metadata.get('dc_title')}")
            print_info(f"Type: {metadata.get('type')}")

            # Check for other standard keys
            for key_suffix in ['type', 'version', 'dependencies']:
                key = f"/chora/capabilities/{TEST_NAMESPACE}/{key_suffix}"
                value, _ = self.etcd.get(key)
                if value:
                    print_pass(f"Key exists: {key_suffix}")
                else:
                    print_fail(f"Key missing: {key_suffix}")
                    self.failed += 1
                    return False

            self.passed += 1
            return True

        except Exception as e:
            print_fail(f"GitOps sync data check failed: {e}")
            self.failed += 1
            return False

    def test_heartbeat_health_data(self):
        """Test 3: Verify heartbeat service is writing health data"""
        print_header("Test 3: Heartbeat Service - Health Status")

        try:
            # Check for health key
            health_key = f"/chora/capabilities/{TEST_NAMESPACE}/health"

            # Get initial health data
            value1, meta1 = self.etcd.get(health_key)
            if not value1:
                print_fail(f"No health data found at {health_key}")
                print_info("Heartbeat service may not be running")
                self.failed += 1
                return False

            health1 = json.loads(value1.decode('utf-8'))
            print_pass(f"Health data found: {health_key}")
            print_info(f"Status: {health1.get('status')}")
            print_info(f"Timestamp: {health1.get('timestamp')}")
            print_info(f"Heartbeat count: {health1.get('heartbeat_count')}")

            # Wait for next heartbeat (interval is 10s)
            print_info("Waiting 12 seconds for next heartbeat...")
            time.sleep(12)

            # Get updated health data
            value2, meta2 = self.etcd.get(health_key)
            if not value2:
                print_fail("Health data disappeared (lease may have expired)")
                self.failed += 1
                return False

            health2 = json.loads(value2.decode('utf-8'))

            # Verify heartbeat count increased
            count1 = health1.get('heartbeat_count', 0)
            count2 = health2.get('heartbeat_count', 0)

            if count2 > count1:
                print_pass(f"Heartbeat count increased: {count1} -> {count2}")
                self.passed += 1
                return True
            else:
                print_fail(f"Heartbeat count did not increase: {count1} -> {count2}")
                print_info("Heartbeat service may have stopped")
                self.failed += 1
                return False

        except Exception as e:
            print_fail(f"Heartbeat health check failed: {e}")
            self.failed += 1
            return False

    def test_data_persistence(self):
        """Test 4: Verify data persists correctly with lease renewals"""
        print_header("Test 4: Data Persistence - Lease Management")

        try:
            health_key = f"/chora/capabilities/{TEST_NAMESPACE}/health"

            # Get initial data
            value1, meta1 = self.etcd.get(health_key)
            if not value1:
                print_fail("No health data to test persistence")
                self.failed += 1
                return False

            health1 = json.loads(value1.decode('utf-8'))
            timestamp1 = health1.get('timestamp')

            # Wait beyond original lease TTL (30s) + buffer
            print_info("Waiting 35 seconds to test lease renewal...")
            time.sleep(35)

            # Data should still exist due to lease renewals
            value2, meta2 = self.etcd.get(health_key)
            if not value2:
                print_fail("Health data expired - lease renewal failed")
                self.failed += 1
                return False

            health2 = json.loads(value2.decode('utf-8'))
            timestamp2 = health2.get('timestamp')

            print_pass("Health data persists beyond original lease TTL")
            print_info(f"Timestamp updated: {timestamp1} -> {timestamp2}")
            print_pass("Lease renewal is working correctly")

            self.passed += 1
            return True

        except Exception as e:
            print_fail(f"Data persistence test failed: {e}")
            self.failed += 1
            return False

    def run_all_tests(self):
        """Run all E2E tests"""
        print_header(f"E2E Integration Test - v5.2.0 Registry Infrastructure")
        print_info(f"Test started: {datetime.utcnow().isoformat()}Z")
        print_info(f"Target: {ETCD_HOST}:{ETCD_PORT}")
        print_info(f"Test namespace: {TEST_NAMESPACE}")

        # Connect to etcd
        if not self.connect():
            print_fail("Setup failed - cannot connect to etcd")
            return False

        # Run all tests
        self.test_etcd_cluster_health()
        self.test_gitops_sync_data()
        self.test_heartbeat_health_data()
        self.test_data_persistence()

        # Print summary
        print_header("Test Summary")
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0

        print(f"\nTests passed: {Colors.GREEN}{self.passed}/{total}{Colors.END}")
        print(f"Tests failed: {Colors.RED}{self.failed}/{total}{Colors.END}")
        print(f"Pass rate: {pass_rate:.1f}%")

        if self.failed == 0:
            print(f"\n{Colors.GREEN}[SUCCESS] All tests passed!{Colors.END}")
            print(f"{Colors.GREEN}The registry infrastructure is working correctly.{Colors.END}\n")
            return True
        else:
            print(f"\n{Colors.RED}[ERROR] {self.failed} test(s) failed{Colors.END}")
            print(f"{Colors.RED}Please review the errors above.{Colors.END}\n")
            return False


def main():
    """Main entry point"""
    test = E2ETest()

    try:
        success = test.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Test interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}")
        sys.exit(2)


if __name__ == '__main__':
    main()
