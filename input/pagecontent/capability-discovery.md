# Discovering server capabilities

## Overview

Goal: Learn how to retrieve and use the CapabilityStatement to understand what resources and operations are available on the server, enabling your application to adapt dynamically.

- Resources: CapabilityStatement
- Skills: GET requests, JSON navigation
- Base URL: `https://playground.dhp.uz/fhir`
  - **Note:** This is a temporary URL that will be replaced with the final one closer to the connectathon
- Useful links:
  - [FHIR CapabilityStatement](http://hl7.org/fhir/R5/capabilitystatement.html)
  - [DHPCapabilityStatement](https://dhp.uz/fhir/core/en/CapabilityStatement-DHPCapabilityStatement.html)

**Feedback:** Share your experience, issues and successes in the [connectathon document](https://docs.google.com/document/d/1PdQ8zBI9xkISP3tAqIK8-TGMql3kVVZ4UNoHVYqCy4Y/edit?usp=sharing).

## What is a CapabilityStatement?

A CapabilityStatement describes what a FHIR server can do. It tells you:
- Which FHIR resources are supported (Patient, Practitioner, ValueSet, etc.)
- What operations you can perform (read, search, create, update, delete)
- Which search parameters are available
- Which operations are supported ($expand, $validate-code, etc.)

This is essential for building adaptive applications that work with different FHIR servers.

## Retrieving the CapabilityStatement

### Basic request

- HTTP method: GET
- Endpoint: `/metadata`

Example:
```
GET /metadata
```

This returns the server's CapabilityStatement in JSON format.

### Key elements in the response

**1. Server information:**
```json
{
  "resourceType": "CapabilityStatement",
  "status": "active",
  "date": "2025-11-10T11:23:12+05:00",
  "kind": "instance",
  "fhirVersion": "5.0.0",
  "implementation": {
    "description": "FHIR R5 Server",
    "url": "https://playground.dhp.uz/fhir"
  }
}
```

**2. Supported resources:**
```json
{
  "rest": [
    {
      "mode": "server",
      "resource": [
        {
          "type": "ValueSet",
          "profile": "http://hl7.org/fhir/StructureDefinition/ValueSet",
          "interaction": [
            { "code": "read" },
            { "code": "search-type" }
          ]
        }
      ]
    }
  ]
}
```

**3. Supported operations:**
```json
{
  "resource": [
    {
      "type": "ValueSet",
      "operation": [
        {
          "name": "expand",
          "definition": "http://hl7.org/fhir/OperationDefinition/ValueSet-expand"
        },
        {
          "name": "validate-code",
          "definition": "http://hl7.org/fhir/OperationDefinition/ValueSet-validate-code"
        }
      ]
    }
  ]
}
```

## Using the CapabilityStatement

### Check if a resource is supported

Before using a resource, check if it's supported:

```javascript
function isResourceSupported(capability, resourceType) {
  const rest = capability.rest.find(r => r.mode === 'server');
  return rest.resource.some(r => r.type === resourceType);
}

// Usage
if (isResourceSupported(capability, 'ValueSet')) {
  // You can use ValueSet resources
}
```

### Check if an operation is supported

Before calling an operation, verify it's available:

```javascript
function isOperationSupported(capability, resourceType, operationName) {
  const rest = capability.rest.find(r => r.mode === 'server');
  const resource = rest.resource.find(r => r.type === resourceType);

  if (!resource || !resource.operation) return false;

  return resource.operation.some(op => op.name === operationName);
}

// Usage
if (isOperationSupported(capability, 'ValueSet', 'expand')) {
  // You can use $expand operation
}
```

### Get available search parameters

Find out which search parameters you can use:

```javascript
function getSearchParams(capability, resourceType) {
  const rest = capability.rest.find(r => r.mode === 'server');
  const resource = rest.resource.find(r => r.type === resourceType);

  if (!resource || !resource.searchParam) return [];

  return resource.searchParam.map(sp => sp.name);
}

// Usage
const params = getSearchParams(capability, 'ValueSet');
console.log('Available search params:', params);
// Output: ['url', 'name', 'status', 'version', ...]
```

## Practical example

Here's a complete example of fetching and using the CapabilityStatement:

```javascript
async function checkServerCapabilities() {
  // Fetch CapabilityStatement
  const response = await fetch('https://playground.dhp.uz/fhir/metadata');
  const capability = await response.json();

  console.log('Server:', capability.implementation?.description || 'Unknown');
  console.log('FHIR Version:', capability.fhirVersion);

  // Check terminology support
  const hasValueSet = isResourceSupported(capability, 'ValueSet');
  const hasExpand = isOperationSupported(capability, 'ValueSet', 'expand');
  const hasValidate = isOperationSupported(capability, 'ValueSet', 'validate-code');

  console.log('ValueSet resource:', hasValueSet ? '✓' : '✗');
  console.log('$expand operation:', hasExpand ? '✓' : '✗');
  console.log('$validate-code operation:', hasValidate ? '✓' : '✗');

  // Enable/disable features in your app
  if (hasExpand) {
    enableValueSetExpansion();
  }

  if (hasValidate) {
    enableCodeValidation();
  }
}
```

## Best practices

1. **Cache the CapabilityStatement**: The capabilities don't change often. Cache the response and refresh periodically.

2. **Graceful degradation**: If an operation isn't supported, provide alternative functionality or clear error messages.

3. **Check on startup**: Retrieve the CapabilityStatement when your application starts to configure available features.

4. **Version awareness**: Check the `fhirVersion` field to ensure compatibility with your application.

## Exercise

**Task:** Retrieve the CapabilityStatement from the playground server and answer these questions:

1. What FHIR version does the server support?
2. Which terminology resources are supported? (CodeSystem, ValueSet, ConceptMap)
3. Which operations are available for ValueSet?
4. Can you search ValueSets by name?

```
GET https://playground.dhp.uz/fhir/metadata
```

Explore the response and write code to programmatically check these capabilities.
