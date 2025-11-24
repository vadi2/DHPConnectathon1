# FHIR API Test Suite

Comprehensive test suite for validating FHIR API examples from the documentation.

## Overview

This test suite validates all sample queries, searches, and CRUD operations documented in:
- `organization-management.md`
- `practitioner-practitionerrole-management.md`
- `patient-registration.md`

## Features

- ✅ Tests all documented search parameters
- ✅ Tests CRUD operations (Create, Read, Update, Delete)
- ✅ Tests positive cases (should find results)
- ✅ Tests negative cases (should not find results)
- ✅ Tests duplicate detection and patient matching logic
- ✅ Configurable for different server environments
- ✅ Colored output for easy result reading
- ✅ Comprehensive test reporting

## Requirements

```bash
pip install requests
```

## Configuration

The test suite can be configured using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `FHIR_BASE_URL` | FHIR server base URL | `https://playground.dhp.uz/fhir` |
| `CLEANUP_AFTER_TESTS` | Delete test resources after running | `false` |
| `VERBOSE` | Show detailed request/response logs | `true` |
| `REQUEST_TIMEOUT` | HTTP request timeout in seconds | `30` |
| `TEST_IDENTIFIER_PREFIX` | Prefix for test identifiers | `test-` |

## Usage

### Run All Tests

```bash
cd tests
python run_all_tests.py
```

### Run Specific Test Suite

```bash
# Organization tests only
python test_organization.py

# Practitioner/PractitionerRole tests only
python test_practitioner.py

# Patient registration tests only
python test_patient.py
```

### Run Against Different Server

```bash
# Test against playground server (default)
python run_all_tests.py

# Test against production server
FHIR_BASE_URL=https://fhir.dhp.uz python run_all_tests.py

# Test against local development server
FHIR_BASE_URL=http://localhost:8080/fhir python run_all_tests.py
```

### Enable Cleanup

By default, test resources are NOT deleted. To enable cleanup:

```bash
CLEANUP_AFTER_TESTS=true python run_all_tests.py
```

### Quiet Mode

To reduce output verbosity:

```bash
VERBOSE=false python run_all_tests.py
```

### Combined Example

```bash
FHIR_BASE_URL=https://fhir.dhp.uz \
CLEANUP_AFTER_TESTS=true \
VERBOSE=false \
python run_all_tests.py
```

## Test Structure

```
tests/
├── config.py                 # Configuration and environment variables
├── test_utils.py            # Utility functions and helpers
├── test_organization.py     # Organization resource tests
├── test_practitioner.py     # Practitioner & PractitionerRole tests
├── test_patient.py          # Patient registration & duplicate detection tests
├── run_all_tests.py         # Main test runner
└── README.md               # This file
```

## Test Coverage

### Organization Tests (14 tests)
- Search by soliq ID
- Search by name (partial and exact)
- Search by type
- Search active organizations
- Combined search parameters (AND logic)
- Multiple values (OR logic)
- Search departments by partof
- Create organization
- Read organization by ID
- Update organization with optimistic locking
- Delete organization
- Negative: Read non-existent organization
- Negative: Search non-existent organization
- Negative: Update without If-Match header

### Practitioner/PractitionerRole Tests (23 tests)
- Search by ARGOS identifier
- Search by name, given name, family name
- Search by phone and email
- Search by address city
- Search by gender
- Search by birthdate and date ranges
- Search by qualification
- Combined search parameters
- Create practitioner
- Read practitioner by ID
- Update practitioner
- Search practitioner roles
- Search by practitioner reference
- Search by organization
- Create practitioner role
- Read practitioner role
- Search with _include parameter
- Negative: Read non-existent practitioner
- Negative: Search non-existent practitioner

### Patient Registration Tests (24 tests)
- Search by PINFL identifier
- Search by name, given name, family name
- Search by phone number
- Search by birthdate and date ranges
- Search by gender
- Search by address city
- Combined demographics search
- Search by organization
- Create patient
- Read patient by ID
- Update patient with optimistic locking
- **Duplicate Detection:**
  - Search before create (prevent duplicates)
  - Search after create (verify duplicate detection)
  - Link duplicate patients
  - Search by demographics for matching
  - Search by phone for matching
- Negative: Read non-existent patient
- Negative: Search non-existent PINFL
- Negative: Search non-existent name
- Negative: Update without If-Match header

## Output

The test suite provides colored output:
- ✓ Green: Test passed
- ✗ Red: Test failed
- ⊘ Yellow: Test skipped

Example output:
```
=== Organization Tests ===

Search Tests
✓ Search organization by soliq ID
✓ Search organization by name (partial)
✓ Search organization by exact name
...

Test Summary
============================================================
Passed:  12
Failed:  0
Skipped: 2
Total:   14

✓ All tests passed!
```

## CI/CD Integration

Exit codes:
- `0`: All tests passed
- `1`: One or more tests failed

Example usage in CI:
```bash
#!/bin/bash
set -e

# Run tests against staging
FHIR_BASE_URL=https://staging.dhp.uz/fhir \
CLEANUP_AFTER_TESTS=true \
python tests/run_all_tests.py

# If tests pass, deploy to production
./deploy.sh
```

## Troubleshooting

### Connection Errors
If you get connection errors, check:
1. Base URL is correct and accessible
2. Network connectivity
3. Firewall/proxy settings
4. Request timeout settings

### Test Failures
If tests fail:
1. Check server is running and accessible
2. Verify server has expected test data
3. Check server version matches documentation
4. Review verbose output for details

### Resource Cleanup
If you want to manually clean up test resources:
```bash
# Find test resources (they all have TEST_IDENTIFIER_PREFIX)
curl "https://playground.dhp.uz/fhir/Patient?name=test-"

# Delete manually or use CLEANUP_AFTER_TESTS=true
```

## Contributing

When adding new documentation examples:
1. Add corresponding test cases to appropriate test file
2. Include both positive and negative test cases
3. Update this README with new test coverage
4. Run full test suite to ensure no regressions

## License

Part of DHPHackathon1 documentation project.
