# Обнаружение возможностей сервера

## Обзор

Цель: Научиться получать и использовать CapabilityStatement для понимания того, какие ресурсы и операции доступны на сервере, позволяя вашему приложению динамически адаптироваться.

- Ресурсы: CapabilityStatement
- Навыки: GET-запросы, навигация по JSON
- Базовый URL: `https://playground.dhp.uz/fhir`
  - **Примечание:** Это временный URL, который будет заменён на финальный ближе к коннектафону
- Полезные ссылки:
  - [FHIR CapabilityStatement](http://hl7.org/fhir/R5/capabilitystatement.html)
  - [DHPCapabilityStatement](https://dhp.uz/fhir/core/en/CapabilityStatement-DHPCapabilityStatement.html)

**Обратная связь:** Поделитесь своим опытом, проблемами и успехами в [документе коннектафона](https://docs.google.com/document/d/1PdQ8zBI9xkISP3tAqIK8-TGMql3kVVZ4UNoHVYqCy4Y/edit?usp=sharing).

## Что такое CapabilityStatement?

CapabilityStatement описывает, что может делать FHIR-сервер. Он сообщает вам:
- Какие ресурсы FHIR поддерживаются (Patient, Practitioner, ValueSet и т.д.)
- Какие операции вы можете выполнять (read, search, create, update, delete)
- Какие параметры поиска доступны
- Какие операции поддерживаются ($expand, $validate-code и т.д.)

Это необходимо для создания адаптивных приложений, которые работают с различными FHIR-серверами.

## Получение CapabilityStatement

### Базовый запрос

- HTTP метод: GET
- Endpoint: `/metadata`

Пример:
```
GET /metadata
```

Это возвращает CapabilityStatement сервера в формате JSON.

### Ключевые элементы в ответе

**1. Информация о сервере:**
```json
{
  "resourceType": "CapabilityStatement",
  "status": "active",
  "date": "2024-11-24",
  "publisher": "Digital Health Platform",
  "kind": "instance",
  "fhirVersion": "5.0.0"
}
```

**2. Поддерживаемые ресурсы:**
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

**3. Поддерживаемые операции:**
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

## Использование CapabilityStatement

### Проверить, поддерживается ли ресурс

Перед использованием ресурса проверьте, поддерживается ли он:

```javascript
function isResourceSupported(capability, resourceType) {
  const rest = capability.rest.find(r => r.mode === 'server');
  return rest.resource.some(r => r.type === resourceType);
}

// Использование
if (isResourceSupported(capability, 'ValueSet')) {
  // Вы можете использовать ресурсы ValueSet
}
```

### Проверить, поддерживается ли операция

Перед вызовом операции убедитесь, что она доступна:

```javascript
function isOperationSupported(capability, resourceType, operationName) {
  const rest = capability.rest.find(r => r.mode === 'server');
  const resource = rest.resource.find(r => r.type === resourceType);

  if (!resource || !resource.operation) return false;

  return resource.operation.some(op => op.name === operationName);
}

// Использование
if (isOperationSupported(capability, 'ValueSet', 'expand')) {
  // Вы можете использовать операцию $expand
}
```

### Получить доступные параметры поиска

Узнайте, какие параметры поиска вы можете использовать:

```javascript
function getSearchParams(capability, resourceType) {
  const rest = capability.rest.find(r => r.mode === 'server');
  const resource = rest.resource.find(r => r.type === resourceType);

  if (!resource || !resource.searchParam) return [];

  return resource.searchParam.map(sp => sp.name);
}

// Использование
const params = getSearchParams(capability, 'ValueSet');
console.log('Доступные параметры поиска:', params);
// Вывод: ['url', 'name', 'status', 'version', ...]
```

## Практический пример

Вот полный пример получения и использования CapabilityStatement:

```javascript
async function checkServerCapabilities() {
  // Получить CapabilityStatement
  const response = await fetch('https://playground.dhp.uz/fhir/metadata');
  const capability = await response.json();

  console.log('Сервер:', capability.publisher);
  console.log('Версия FHIR:', capability.fhirVersion);

  // Проверить поддержку терминологии
  const hasValueSet = isResourceSupported(capability, 'ValueSet');
  const hasExpand = isOperationSupported(capability, 'ValueSet', 'expand');
  const hasValidate = isOperationSupported(capability, 'ValueSet', 'validate-code');

  console.log('Ресурс ValueSet:', hasValueSet ? '✓' : '✗');
  console.log('Операция $expand:', hasExpand ? '✓' : '✗');
  console.log('Операция $validate-code:', hasValidate ? '✓' : '✗');

  // Включить/отключить функции в вашем приложении
  if (hasExpand) {
    enableValueSetExpansion();
  }

  if (hasValidate) {
    enableCodeValidation();
  }
}
```

## Лучшие практики

1. **Кэшируйте CapabilityStatement**: Возможности не меняются часто. Кэшируйте ответ и обновляйте периодически.

2. **Постепенная деградация**: Если операция не поддерживается, предоставьте альтернативную функциональность или понятные сообщения об ошибках.

3. **Проверяйте при запуске**: Получайте CapabilityStatement при запуске приложения для настройки доступных функций.

4. **Учитывайте версию**: Проверяйте поле `fhirVersion` для обеспечения совместимости с вашим приложением.

## Упражнение

**Задача:** Получите CapabilityStatement с сервера playground и ответьте на эти вопросы:

1. Какую версию FHIR поддерживает сервер?
2. Какие ресурсы терминологии поддерживаются? (CodeSystem, ValueSet, ConceptMap)
3. Какие операции доступны для ValueSet?
4. Можете ли вы искать ValueSet по имени?

```
GET https://playground.dhp.uz/fhir/metadata
```

Изучите ответ и напишите код для программной проверки этих возможностей.
