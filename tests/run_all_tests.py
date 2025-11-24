#!/usr/bin/env python3
"""
Main test runner for FHIR API tests
Runs all test suites and provides comprehensive reporting
"""
import sys
import time
from test_utils import Colors, TestResults
from test_organization import run_organization_tests
from test_practitioner import run_practitioner_tests
from test_patient import run_patient_tests
from config import BASE_URL


def print_header():
    """Print test suite header"""
    print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}FHIR API Test Suite{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"\nTesting against: {Colors.BLUE}{BASE_URL}{Colors.RESET}\n")


def print_separator():
    """Print separator between test suites"""
    print(f"\n{Colors.BOLD}{'-'*70}{Colors.RESET}\n")


def aggregate_results(all_results: list) -> TestResults:
    """Aggregate results from multiple test suites"""
    total = TestResults()
    for results in all_results:
        total.passed += results.passed
        total.failed += results.failed
        total.skipped += results.skipped
        total.failures.extend(results.failures)
    return total


def main():
    """Run all test suites"""
    print_header()

    start_time = time.time()
    all_results = []

    # Run Organization tests
    try:
        org_results = run_organization_tests()
        all_results.append(org_results)
        print_separator()
    except Exception as e:
        print(f"{Colors.RED}Organization tests failed with exception: {e}{Colors.RESET}")
        sys.exit(1)

    # Run Practitioner/PractitionerRole tests
    try:
        pract_results = run_practitioner_tests()
        all_results.append(pract_results)
        print_separator()
    except Exception as e:
        print(f"{Colors.RED}Practitioner tests failed with exception: {e}{Colors.RESET}")
        sys.exit(1)

    # Run Patient tests
    try:
        patient_results = run_patient_tests()
        all_results.append(patient_results)
        print_separator()
    except Exception as e:
        print(f"{Colors.RED}Patient tests failed with exception: {e}{Colors.RESET}")
        sys.exit(1)

    # Aggregate and print final results
    elapsed_time = time.time() - start_time
    total_results = aggregate_results(all_results)

    print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}Overall Test Results{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"\nTest Suites Run: {len(all_results)}")
    print(f"Time Elapsed: {elapsed_time:.2f} seconds")

    total_results.print_summary()

    # Exit with appropriate code
    exit_code = 0 if total_results.failed == 0 else 1

    if exit_code == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All tests passed!{Colors.RESET}\n")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ Some tests failed{Colors.RESET}\n")

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
