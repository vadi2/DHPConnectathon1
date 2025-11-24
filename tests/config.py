"""
Configuration for FHIR API tests
"""
import os

# Base URL for FHIR server - can be overridden with environment variable
BASE_URL = os.environ.get('FHIR_BASE_URL', 'https://playground.dhp.uz/fhir')

# Test data cleanup - if True, delete test resources after running
CLEANUP_AFTER_TESTS = os.environ.get('CLEANUP_AFTER_TESTS', 'false').lower() == 'true'

# Verbose output
VERBOSE = os.environ.get('VERBOSE', 'true').lower() == 'true'

# Timeout for requests in seconds
REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', '30'))

# Test identifiers to avoid conflicts
TEST_IDENTIFIER_PREFIX = os.environ.get('TEST_IDENTIFIER_PREFIX', 'test-')
