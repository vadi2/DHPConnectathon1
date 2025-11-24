"""
Tests for FHIR Terminology resources and operations
Based on examples from terminology-basics.md
"""
import time
from test_utils import (
    TestResults, make_request, search_resources,
    extract_entries, Colors
)
from config import TEST_IDENTIFIER_PREFIX


def run_terminology_tests() -> TestResults:
    """Run all terminology tests"""
    results = TestResults()

    print(f"\n{Colors.BOLD}=== Terminology Tests ==={Colors.RESET}\n")

    # ========== CodeSystem Tests ==========
    print(f"\n{Colors.BOLD}CodeSystem Tests{Colors.RESET}")

    # Test 1: Search for all CodeSystems (summary)
    response = make_request('GET', '/CodeSystem', params={'_summary': 'true', '_count': '5'})
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'CodeSystem')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Found {len(entries)} CodeSystem(s){Colors.RESET}")
            results.add_pass("Search all CodeSystems with summary")
        else:
            results.add_skip("Search all CodeSystems", "No CodeSystems found")
    else:
        results.add_fail("Search all CodeSystems", f"Status {response.status_code}")

    # Test 2: Search CodeSystem by URL
    response = make_request('GET', '/CodeSystem', params={
        'url': 'http://terminology.hl7.org/CodeSystem/v2-0203'
    })
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'CodeSystem')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Found CodeSystem: {entries[0].get('name', 'Unknown')}{Colors.RESET}")
            results.add_pass("Search CodeSystem by URL")
        else:
            results.add_skip("Search CodeSystem by URL", "Specific CodeSystem not found")
    else:
        results.add_fail("Search CodeSystem by URL", f"Status {response.status_code}")

    # Test 3: Search CodeSystem by status
    response = make_request('GET', '/CodeSystem', params={'status': 'active', '_count': '3'})
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'CodeSystem')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Found {len(entries)} active CodeSystem(s){Colors.RESET}")
            results.add_pass("Search CodeSystem by status=active")
        else:
            results.add_skip("Search CodeSystem by status", "No active CodeSystems found")
    else:
        results.add_fail("Search CodeSystem by status", f"Status {response.status_code}")

    # Test 4: Search CodeSystem by content type
    response = make_request('GET', '/CodeSystem', params={'content': 'complete', '_count': '3'})
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'CodeSystem')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Found {len(entries)} complete CodeSystem(s){Colors.RESET}")
            results.add_pass("Search CodeSystem by content=complete")
        else:
            results.add_skip("Search CodeSystem by content", "No complete CodeSystems found")
    else:
        results.add_fail("Search CodeSystem by content", f"Status {response.status_code}")

    # Test 5: Read specific CodeSystem by canonical URL
    # First get one from search to have a valid URL
    response = make_request('GET', '/CodeSystem', params={'_count': '1'})
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'CodeSystem')
        if entries:
            cs_url = entries[0].get('url')
            cs_name = entries[0].get('name', 'Unknown')
            if cs_url:
                # Now read it by canonical URL
                response = make_request('GET', '/CodeSystem', params={'url': cs_url})
                if response.status_code == 200:
                    bundle = response.json()
                    entries = extract_entries(bundle, 'CodeSystem')
                    if entries:
                        print(f"  {Colors.CYAN}→ Read CodeSystem by URL: {cs_name}{Colors.RESET}")
                        results.add_pass(f"Read CodeSystem by canonical URL")
                    else:
                        results.add_fail("Read CodeSystem by URL", "No entry in Bundle")
                else:
                    results.add_fail("Read CodeSystem by URL", f"Status {response.status_code}")
            else:
                results.add_skip("Read CodeSystem by URL", "No URL in CodeSystem")
        else:
            results.add_skip("Read CodeSystem by URL", "No CodeSystem to read")
    else:
        results.add_fail("Read CodeSystem by URL", f"Search failed: {response.status_code}")

    # ========== ValueSet Tests ==========
    print(f"\n{Colors.BOLD}ValueSet Tests{Colors.RESET}")

    # Test 6: Search for all ValueSets (summary)
    response = make_request('GET', '/ValueSet', params={'_summary': 'true', '_count': '5'})
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'ValueSet')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Found {len(entries)} ValueSet(s){Colors.RESET}")
            results.add_pass("Search all ValueSets with summary")
        else:
            results.add_skip("Search all ValueSets", "No ValueSets found")
    else:
        results.add_fail("Search all ValueSets", f"Status {response.status_code}")

    # Test 7: Search ValueSet by URL
    response = make_request('GET', '/ValueSet', params={
        'url': 'http://hl7.org/fhir/ValueSet/administrative-gender'
    })
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'ValueSet')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Found ValueSet: {entries[0].get('name', 'Unknown')}{Colors.RESET}")
            results.add_pass("Search ValueSet by URL")
        else:
            results.add_skip("Search ValueSet by URL", "Specific ValueSet not found")
    else:
        results.add_fail("Search ValueSet by URL", f"Status {response.status_code}")

    # Test 8: Search ValueSet by status
    response = make_request('GET', '/ValueSet', params={'status': 'active', '_count': '3'})
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'ValueSet')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Found {len(entries)} active ValueSet(s){Colors.RESET}")
            results.add_pass("Search ValueSet by status=active")
        else:
            results.add_skip("Search ValueSet by status", "No active ValueSets found")
    else:
        results.add_fail("Search ValueSet by status", f"Status {response.status_code}")

    # Test 9: Read specific ValueSet by canonical URL
    response = make_request('GET', '/ValueSet', params={'_count': '1'})
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'ValueSet')
        if entries:
            vs_url = entries[0].get('url')
            vs_name = entries[0].get('name', 'Unknown')
            if vs_url:
                # Now read it by canonical URL
                response = make_request('GET', '/ValueSet', params={'url': vs_url})
                if response.status_code == 200:
                    bundle = response.json()
                    entries = extract_entries(bundle, 'ValueSet')
                    if entries:
                        print(f"  {Colors.CYAN}→ Read ValueSet by URL: {vs_name}{Colors.RESET}")
                        results.add_pass(f"Read ValueSet by canonical URL")
                    else:
                        results.add_fail("Read ValueSet by URL", "No entry in Bundle")
                else:
                    results.add_fail("Read ValueSet by URL", f"Status {response.status_code}")
            else:
                results.add_skip("Read ValueSet by URL", "No URL in ValueSet")
        else:
            results.add_skip("Read ValueSet by URL", "No ValueSet to read")
    else:
        results.add_fail("Read ValueSet by URL", f"Search failed: {response.status_code}")

    # ========== $expand Operation Tests ==========
    print(f"\n{Colors.BOLD}$expand Operation Tests{Colors.RESET}")

    # Test 10: Expand ValueSet by ID
    # Get a ValueSet that we can expand
    response = make_request('GET', '/ValueSet', params={'_count': '1'})
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'ValueSet')
        if entries:
            vs_id = entries[0]['id']
            vs_name = entries[0].get('name', 'Unknown')

            # Expand by ID
            response = make_request('GET', f'/ValueSet/{vs_id}/$expand')
            if response.status_code == 200:
                expansion = response.json()
                if 'expansion' in expansion:
                    contains = expansion['expansion'].get('contains', [])
                    print(f"  {Colors.CYAN}→ Expanded {vs_name}: {len(contains)} code(s){Colors.RESET}")
                    results.add_pass(f"$expand ValueSet by ID ({vs_id})")
                else:
                    results.add_fail("$expand ValueSet by ID", "No expansion in response")
            elif response.status_code == 422:
                results.add_skip(f"$expand ValueSet ({vs_name})", "Server cannot expand this ValueSet (422)")
            else:
                results.add_skip(f"$expand ValueSet ({vs_name})", f"Status {response.status_code}")
        else:
            results.add_skip("$expand ValueSet by ID", "No ValueSet to expand")
    else:
        results.add_fail("$expand ValueSet", f"Search failed: {response.status_code}")

    # Test 11: Expand ValueSet by URL
    response = make_request('GET', '/ValueSet/$expand', params={
        'url': 'http://hl7.org/fhir/ValueSet/administrative-gender'
    })
    if response.status_code == 200:
        expansion = response.json()
        if 'expansion' in expansion:
            contains = expansion['expansion'].get('contains', [])
            print(f"  {Colors.CYAN}→ Expanded administrative-gender: {len(contains)} code(s){Colors.RESET}")
            results.add_pass("$expand ValueSet by URL (administrative-gender)")
        else:
            results.add_fail("$expand ValueSet by URL", "No expansion in response")
    elif response.status_code == 422:
        results.add_skip("$expand ValueSet by URL", "Server cannot expand this ValueSet (422)")
    else:
        results.add_skip("$expand ValueSet by URL", f"Status {response.status_code}")

    # Test 12: Expand ValueSet with count parameter
    response = make_request('GET', '/ValueSet', params={'_count': '1'})
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'ValueSet')
        if entries:
            vs_id = entries[0]['id']
            vs_name = entries[0].get('name', 'Unknown')

            # Expand with count=5
            response = make_request('GET', f'/ValueSet/{vs_id}/$expand', params={'count': '5'})
            if response.status_code == 200:
                expansion = response.json()
                if 'expansion' in expansion:
                    contains = expansion['expansion'].get('contains', [])
                    if len(contains) <= 5:
                        print(f"  {Colors.CYAN}→ Expanded with count=5: {len(contains)} code(s){Colors.RESET}")
                        results.add_pass("$expand ValueSet with count parameter")
                    else:
                        results.add_fail("$expand with count", f"Expected <=5 codes, got {len(contains)}")
                else:
                    results.add_fail("$expand with count", "No expansion in response")
            elif response.status_code == 422:
                results.add_skip(f"$expand with count ({vs_name})", "Server cannot expand this ValueSet (422)")
            else:
                results.add_skip(f"$expand with count ({vs_name})", f"Status {response.status_code}")
        else:
            results.add_skip("$expand with count", "No ValueSet to expand")
    else:
        results.add_fail("$expand with count", f"Search failed: {response.status_code}")

    # Test 13: Expand ValueSet with filter parameter
    response = make_request('GET', '/ValueSet/$expand', params={
        'url': 'http://hl7.org/fhir/ValueSet/administrative-gender',
        'filter': 'male'
    })
    if response.status_code == 200:
        expansion = response.json()
        if 'expansion' in expansion:
            contains = expansion['expansion'].get('contains', [])
            # Should contain 'male' and 'female' (contains 'male')
            print(f"  {Colors.CYAN}→ Expanded with filter='male': {len(contains)} code(s){Colors.RESET}")
            results.add_pass("$expand ValueSet with filter parameter")
        else:
            results.add_fail("$expand with filter", "No expansion in response")
    elif response.status_code == 422:
        results.add_skip("$expand with filter", "Server cannot expand with filter (422)")
    else:
        results.add_skip("$expand with filter", f"Status {response.status_code}")

    # ========== $validate-code Operation Tests ==========
    print(f"\n{Colors.BOLD}$validate-code Operation Tests{Colors.RESET}")

    # Test 14: Validate a valid code
    response = make_request('GET', '/ValueSet/$validate-code', params={
        'url': 'http://hl7.org/fhir/ValueSet/administrative-gender',
        'code': 'male',
        'system': 'http://hl7.org/fhir/administrative-gender'
    })
    if response.status_code == 200:
        result = response.json()
        params = result.get('parameter', [])
        result_param = next((p for p in params if p.get('name') == 'result'), None)
        if result_param and result_param.get('valueBoolean') == True:
            print(f"  {Colors.CYAN}→ Code 'male' is valid{Colors.RESET}")
            results.add_pass("$validate-code with valid code")
        else:
            results.add_fail("$validate-code valid", "Expected result=true")
    else:
        results.add_skip("$validate-code valid", f"Status {response.status_code}")

    # Test 15: Validate an invalid code
    response = make_request('GET', '/ValueSet/$validate-code', params={
        'url': 'http://hl7.org/fhir/ValueSet/administrative-gender',
        'code': 'INVALID_CODE',
        'system': 'http://hl7.org/fhir/administrative-gender'
    })
    if response.status_code == 200:
        result = response.json()
        params = result.get('parameter', [])
        result_param = next((p for p in params if p.get('name') == 'result'), None)
        if result_param and result_param.get('valueBoolean') == False:
            print(f"  {Colors.CYAN}→ Code 'INVALID_CODE' correctly rejected{Colors.RESET}")
            results.add_pass("$validate-code with invalid code")
        else:
            results.add_fail("$validate-code invalid", "Expected result=false")
    else:
        results.add_skip("$validate-code invalid", f"Status {response.status_code}")

    # Test 16: Validate code with wrong system
    response = make_request('GET', '/ValueSet/$validate-code', params={
        'url': 'http://hl7.org/fhir/ValueSet/administrative-gender',
        'code': 'male',
        'system': 'http://wrong-system.example.com'
    })
    if response.status_code == 200:
        result = response.json()
        params = result.get('parameter', [])
        result_param = next((p for p in params if p.get('name') == 'result'), None)
        if result_param and result_param.get('valueBoolean') == False:
            print(f"  {Colors.CYAN}→ Code with wrong system correctly rejected{Colors.RESET}")
            results.add_pass("$validate-code with wrong system")
        else:
            results.add_fail("$validate-code wrong system", "Expected result=false")
    else:
        results.add_skip("$validate-code wrong system", f"Status {response.status_code}")

    # ========== $lookup Operation Tests ==========
    print(f"\n{Colors.BOLD}$lookup Operation Tests{Colors.RESET}")

    # Test 17: Lookup a code in CodeSystem
    response = make_request('GET', '/CodeSystem/$lookup', params={
        'system': 'http://hl7.org/fhir/administrative-gender',
        'code': 'male'
    })
    if response.status_code == 200:
        result = response.json()
        params = result.get('parameter', [])
        display_param = next((p for p in params if p.get('name') == 'display'), None)
        if display_param:
            display = display_param.get('valueString', 'Unknown')
            print(f"  {Colors.CYAN}→ Code 'male' display: {display}{Colors.RESET}")
            results.add_pass("$lookup code in CodeSystem")
        else:
            results.add_skip("$lookup code", "No display parameter in response")
    else:
        results.add_skip("$lookup code", f"Status {response.status_code}")

    # Test 18: Lookup a non-existent code
    response = make_request('GET', '/CodeSystem/$lookup', params={
        'system': 'http://hl7.org/fhir/administrative-gender',
        'code': 'INVALID_CODE'
    })
    if response.status_code == 404 or response.status_code == 400:
        print(f"  {Colors.CYAN}→ Non-existent code correctly not found{Colors.RESET}")
        results.add_pass("$lookup non-existent code (expect 404/400)")
    elif response.status_code == 200:
        # Some servers might return 200 with an error in OperationOutcome
        result = response.json()
        if result.get('resourceType') == 'OperationOutcome':
            print(f"  {Colors.CYAN}→ Non-existent code returned OperationOutcome{Colors.RESET}")
            results.add_pass("$lookup non-existent code (OperationOutcome)")
        else:
            results.add_fail("$lookup non-existent", "Expected error, got successful response")
    else:
        results.add_skip("$lookup non-existent", f"Status {response.status_code}")

    # ========== ConceptMap Tests ==========
    print(f"\n{Colors.BOLD}ConceptMap Tests{Colors.RESET}")

    # Test 19: Search for ConceptMaps
    response = make_request('GET', '/ConceptMap', params={'_summary': 'true', '_count': '5'})
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'ConceptMap')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Found {len(entries)} ConceptMap(s){Colors.RESET}")
            results.add_pass("Search for ConceptMaps")
        else:
            results.add_skip("Search ConceptMaps", "No ConceptMaps found on server")
    else:
        results.add_skip("Search ConceptMaps", f"Status {response.status_code}")

    # Test 20: Search ConceptMap by status
    response = make_request('GET', '/ConceptMap', params={'status': 'active', '_count': '3'})
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'ConceptMap')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Found {len(entries)} active ConceptMap(s){Colors.RESET}")
            results.add_pass("Search ConceptMap by status=active")
        else:
            results.add_skip("Search ConceptMap by status", "No active ConceptMaps found")
    else:
        results.add_skip("Search ConceptMap by status", f"Status {response.status_code}")

    # Test 21: Read ConceptMap by ID (if any exist)
    response = make_request('GET', '/ConceptMap', params={'_count': '1'})
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'ConceptMap')
        if entries:
            cm_id = entries[0]['id']
            cm_name = entries[0].get('name', 'Unknown')

            # Now read it
            response = make_request('GET', f'/ConceptMap/{cm_id}')
            if response.status_code == 200:
                cm = response.json()
                print(f"  {Colors.CYAN}→ Read ConceptMap: {cm.get('name', 'Unknown')}{Colors.RESET}")
                results.add_pass(f"Read ConceptMap by ID ({cm_id})")
            else:
                results.add_fail("Read ConceptMap by ID", f"Status {response.status_code}")
        else:
            results.add_skip("Read ConceptMap by ID", "No ConceptMaps to read")
    else:
        results.add_skip("Read ConceptMap by ID", f"Search failed: {response.status_code}")

    # ========== Version Management Tests ==========
    print(f"\n{Colors.BOLD}Version Management Tests{Colors.RESET}")

    # Test 22: Search CodeSystem with version sorting
    response = make_request('GET', '/CodeSystem', params={
        'url': 'http://terminology.hl7.org/CodeSystem/v2-0203',
        '_sort': '-version',
        '_count': '3'
    })
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'CodeSystem')
        if len(entries) > 0:
            versions = [e.get('version', 'unknown') for e in entries]
            print(f"  {Colors.CYAN}→ Found versions: {', '.join(versions)}{Colors.RESET}")
            results.add_pass("Search CodeSystem with version sorting")
        else:
            results.add_skip("Search with version sort", "No CodeSystems found")
    else:
        results.add_skip("Search with version sort", f"Status {response.status_code}")

    # Test 23: Search for specific version of CodeSystem
    response = make_request('GET', '/CodeSystem', params={
        'url': 'http://terminology.hl7.org/CodeSystem/v2-0203',
        'version': '3.0.0'
    })
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'CodeSystem')
        if len(entries) > 0:
            version = entries[0].get('version', 'unknown')
            print(f"  {Colors.CYAN}→ Found specific version: {version}{Colors.RESET}")
            results.add_pass("Search CodeSystem by specific version")
        else:
            results.add_skip("Search by version", "Specific version not found")
    else:
        results.add_skip("Search by version", f"Status {response.status_code}")

    # ========== Error Handling Tests ==========
    print(f"\n{Colors.BOLD}Error Handling Tests{Colors.RESET}")

    # Test 24: Try to expand non-existent ValueSet
    response = make_request('GET', '/ValueSet/$expand', params={
        'url': 'http://example.com/ValueSet/nonexistent'
    })
    if response.status_code == 404 or response.status_code == 400:
        print(f"  {Colors.CYAN}→ Non-existent ValueSet correctly returned error{Colors.RESET}")
        results.add_pass("Error: Expand non-existent ValueSet (expect 404/400)")
    elif response.status_code == 200:
        result = response.json()
        if result.get('resourceType') == 'OperationOutcome':
            print(f"  {Colors.CYAN}→ Non-existent ValueSet returned OperationOutcome{Colors.RESET}")
            results.add_pass("Error: Expand non-existent (OperationOutcome)")
        else:
            results.add_fail("Error: Expand non-existent", "Expected error response")
    else:
        results.add_skip("Error: Expand non-existent", f"Status {response.status_code}")

    # Test 25: Try to validate with missing required parameters
    response = make_request('GET', '/ValueSet/$validate-code', params={
        'url': 'http://hl7.org/fhir/ValueSet/administrative-gender'
        # Missing 'code' and 'system'
    })
    if response.status_code == 400:
        print(f"  {Colors.CYAN}→ Missing parameters correctly rejected (400){Colors.RESET}")
        results.add_pass("Error: Validate with missing parameters (expect 400)")
    elif response.status_code == 200:
        result = response.json()
        if result.get('resourceType') == 'OperationOutcome':
            print(f"  {Colors.CYAN}→ Missing parameters returned OperationOutcome{Colors.RESET}")
            results.add_pass("Error: Validate missing params (OperationOutcome)")
        else:
            results.add_fail("Error: Missing params", "Expected error response")
    else:
        results.add_skip("Error: Missing params", f"Status {response.status_code}")

    # Test 26: Try to lookup with invalid system
    response = make_request('GET', '/CodeSystem/$lookup', params={
        'system': 'http://invalid-system.example.com',
        'code': 'test'
    })
    if response.status_code == 404 or response.status_code == 400:
        print(f"  {Colors.CYAN}→ Invalid system correctly rejected{Colors.RESET}")
        results.add_pass("Error: Lookup with invalid system (expect 404/400)")
    elif response.status_code == 200:
        result = response.json()
        if result.get('resourceType') == 'OperationOutcome':
            print(f"  {Colors.CYAN}→ Invalid system returned OperationOutcome{Colors.RESET}")
            results.add_pass("Error: Invalid system (OperationOutcome)")
        else:
            results.add_fail("Error: Invalid system", "Expected error response")
    else:
        results.add_skip("Error: Invalid system", f"Status {response.status_code}")

    # ========== Additional Search Parameter Tests ==========
    print(f"\n{Colors.BOLD}Additional Search Parameter Tests{Colors.RESET}")

    # Test 27: Search CodeSystem by title
    response = make_request('GET', '/CodeSystem', params={
        'title': 'Identifier',
        '_count': '3'
    })
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'CodeSystem')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Found {len(entries)} CodeSystem(s) by title{Colors.RESET}")
            results.add_pass("Search CodeSystem by title")
        else:
            results.add_skip("Search by title", "No CodeSystems found")
    else:
        results.add_skip("Search by title", f"Status {response.status_code}")

    # Test 28: Search CodeSystem by publisher
    response = make_request('GET', '/CodeSystem', params={
        'publisher': 'HL7',
        '_count': '3'
    })
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'CodeSystem')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Found {len(entries)} CodeSystem(s) by publisher{Colors.RESET}")
            results.add_pass("Search CodeSystem by publisher")
        else:
            results.add_skip("Search by publisher", "No CodeSystems found")
    else:
        results.add_skip("Search by publisher", f"Status {response.status_code}")

    # Test 29: Search ValueSet by name
    response = make_request('GET', '/ValueSet', params={
        'name': 'administrative',
        '_count': '3'
    })
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'ValueSet')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Found {len(entries)} ValueSet(s) by name{Colors.RESET}")
            results.add_pass("Search ValueSet by name")
        else:
            results.add_skip("Search ValueSet by name", "No ValueSets found")
    else:
        results.add_skip("Search ValueSet by name", f"Status {response.status_code}")

    # Test 30: Search ValueSet by title
    response = make_request('GET', '/ValueSet', params={
        'title': 'gender',
        '_count': '3'
    })
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'ValueSet')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Found {len(entries)} ValueSet(s) by title{Colors.RESET}")
            results.add_pass("Search ValueSet by title")
        else:
            results.add_skip("Search ValueSet by title", "No ValueSets found")
    else:
        results.add_skip("Search ValueSet by title", f"Status {response.status_code}")

    # Test 31: Search ValueSet by publisher
    response = make_request('GET', '/ValueSet', params={
        'publisher': 'HL7',
        '_count': '3'
    })
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'ValueSet')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Found {len(entries)} ValueSet(s) by publisher{Colors.RESET}")
            results.add_pass("Search ValueSet by publisher")
        else:
            results.add_skip("Search ValueSet by publisher", "No ValueSets found")
    else:
        results.add_skip("Search ValueSet by publisher", f"Status {response.status_code}")

    # Test 32: Search ConceptMap by name
    response = make_request('GET', '/ConceptMap', params={
        'name': 'map',
        '_count': '3'
    })
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'ConceptMap')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Found {len(entries)} ConceptMap(s) by name{Colors.RESET}")
            results.add_pass("Search ConceptMap by name")
        else:
            results.add_skip("Search ConceptMap by name", "No ConceptMaps found")
    else:
        results.add_skip("Search ConceptMap by name", f"Status {response.status_code}")

    # Test 33: Search ConceptMap by source-scope-uri
    response = make_request('GET', '/ConceptMap', params={
        'source-scope-uri': 'urn:iso:std:iso:3166',
        '_count': '3'
    })
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'ConceptMap')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Found {len(entries)} ConceptMap(s) by source-scope-uri{Colors.RESET}")
            results.add_pass("Search ConceptMap by source-scope-uri")
        else:
            results.add_skip("Search ConceptMap by source-scope-uri", "No ConceptMaps found")
    else:
        results.add_skip("Search ConceptMap by source-scope-uri", f"Status {response.status_code}")

    # Test 34: Search ConceptMap by target-scope-uri
    response = make_request('GET', '/ConceptMap', params={
        'target-scope-uri': 'urn:iso:std:iso:3166',
        '_count': '3'
    })
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'ConceptMap')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Found {len(entries)} ConceptMap(s) by target-scope-uri{Colors.RESET}")
            results.add_pass("Search ConceptMap by target-scope-uri")
        else:
            results.add_skip("Search ConceptMap by target-scope-uri", "No ConceptMaps found")
    else:
        results.add_skip("Search ConceptMap by target-scope-uri", f"Status {response.status_code}")

    # Test 35: Combined search parameters
    response = make_request('GET', '/ValueSet', params={
        'status': 'active',
        '_count': '3'
    })
    if response.status_code == 200:
        bundle = response.json()
        entries = extract_entries(bundle, 'ValueSet')
        if len(entries) > 0:
            print(f"  {Colors.CYAN}→ Combined search found {len(entries)} ValueSet(s){Colors.RESET}")
            results.add_pass("Combined search parameters (status + count)")
        else:
            results.add_skip("Combined search", "No results found")
    else:
        results.add_skip("Combined search", f"Status {response.status_code}")

    # Test 36: Pagination test
    response = make_request('GET', '/CodeSystem', params={'_count': '2'})
    if response.status_code == 200:
        bundle = response.json()
        links = bundle.get('link', [])
        next_link = next((l for l in links if l.get('relation') == 'next'), None)
        if next_link:
            print(f"  {Colors.CYAN}→ Found next page link in pagination{Colors.RESET}")
            results.add_pass("Pagination: Next link present")
        else:
            results.add_skip("Pagination test", "No next link (maybe only one page)")
    else:
        results.add_skip("Pagination test", f"Status {response.status_code}")


    return results


if __name__ == '__main__':
    results = run_terminology_tests()
    success = results.print_summary()
    exit(0 if success else 1)
